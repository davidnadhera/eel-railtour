from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.dialects.sqlite import REAL,TIME
from sqlalchemy.ext.associationproxy import association_proxy
from dbutils import get_or_create
from sqlalchemy.ext.declarative import declarative_base
from datetime import time,datetime,timedelta
from bs4 import BeautifulSoup
from time import sleep
from scraping import proxy_servers
import requests
from lxml import etree
import csv

Base = declarative_base()

class Presun(Base):
    __tablename__ = "presuny"
    od_id = Column(ForeignKey("bod.id"), primary_key=True)
    do_id = Column(ForeignKey("bod.id"), primary_key=True)
    km = Column(REAL)
    cas = Column(Integer)
    od = relationship("Bod", back_populates="presuny_od", foreign_keys=[od_id])
    do = relationship("Bod", back_populates="presuny_do", foreign_keys=[do_id])

    def __repr__(self):
        return f"Přesun {self.od!r} -> {self.do!r}"

class Stop(Base):
    __tablename__ = 'stops'

    id = Column(Integer, primary_key=True, nullable=False)
    bod_id = Column(ForeignKey("bod.id"))
    odjezd = Column(TIME)
    prijezd = Column(TIME)
    vlak = Column(String)
    vlak_id = Column(Integer)

    stanice = relationship("Bod", back_populates="stops", foreign_keys=[bod_id])

    def __repr__(self):
        return f"Stop {self.stanice!r} {self.vlak!r}"

class Bod(Base):
    __tablename__ = 'bod'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100))
    lower_name = Column(String(100))
    type = Column(String(20))
    gps_N = Column(REAL)
    gps_E = Column(REAL)
    uzel = Column(Boolean)

    presuny_od = relationship("Presun", back_populates="od", foreign_keys=[Presun.od_id])
    presuny_do = relationship("Presun", back_populates="do", foreign_keys=[Presun.do_id])
    stops = relationship("Stop", back_populates="stanice", foreign_keys=[Stop.bod_id])

    sousede_tam = association_proxy("presuny_od", "do")
    sousede_zpet = association_proxy("presuny_do", "od")

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "bod",
    }

    def __repr__(self):
        return f"{self.id!r} {self.name!r}"

    def from_idos(self,session,datum,byarr):
        cas = datetime.strptime(datum,'%d.%m.%Y')
        prevcas = cas
        cas_max = cas + timedelta(days=1)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Accept-Encoding": "*",
            "Connection": "keep-alive"
        }
        # filename = 'prijezdy' if byarr else 'odjezdy'
        # with open(f'data/{filename}.csv', 'a+', newline='') as csvfile:
        #     fieldnames = ['bod_id', 'cas','vlak','vlak_id']
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        while cas < cas_max:
            url = f'http://idos.idnes.cz/vlaky/odjezdy/vysledky/?date={datum}&time={cas.time().isoformat(timespec="minutes")}&f={self.name}&fc=100003&byarr={str.lower(str(byarr))}'
            proxies = {"http": "socks5://152.67.188.122:1080",
                         "https": "socks5://152.67.188.122:1080"}
            print(url)
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.content.decode('utf-8','ignore'), 'html.parser')
            dom = etree.HTML(str(soup))
            rows = dom.xpath('//tr[contains(@class,"dep-row-first")]')
            if (not rows):
                break
            for row in rows:
                cas = datetime.strptime(row.attrib['data-datetime'], '%d.%m.%Y %H:%M:%S')
                if cas >= cas_max:
                    break
                vlak_id = int(row.attrib['data-train'])
                node = row.xpath('./td[2]/span/span/h3')
                vlak = node[0].text.split()
                # writer.writerow({'bod_id':self.id,'cas':cas,'vlak':vlak,'vlak_id':vlak_id})

                stop = get_or_create(session,Stop,stanice=self,vlak_id=vlak_id)
                if byarr:
                    stop.prijezd = cas.time()
                else:
                    stop.odjezd = cas.time()
                stop.vlak = ' '.join(vlak[:2])
                session.add(stop)
                session.commit()
            if prevcas == cas:
                break
            prevcas = cas
            sleep(1)
        sleep(1)

class Stanice(Bod):
    cislo = Column(Integer)
    prestup = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "stanice",
    }

class Checkpoint(Bod):
    active = Column(Boolean)
    body = Column(Integer)
    kraj = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "checkpoint",
    }



from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, ForeignKeyConstraint
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
from dateutils import add_time, make_date

Base = declarative_base()

class SpojHrany(Base):
    __tablename__ = "spoj_hrany"
    __table_args__ = (
        ForeignKeyConstraint(
            ["od_id", "do_id"], ["presuny.od_id", "presuny.do_id"]
        ),
    )
    id = Column(Integer, primary_key=True)
    hrana_id = Column(ForeignKey("hrany.id"))
    spoj_id = Column(ForeignKey("spoj.id"))
    od_id = Column(Integer)
    do_id = Column(Integer)
    odjezd = Column(TIME)
    poradi = Column(Integer)
    hrana = relationship("Hrana", back_populates="spoje", foreign_keys=[hrana_id])
    spoj = relationship("Spoj", backref=backref('spoje_hran', lazy='noload'), foreign_keys=[spoj_id])
    presun = relationship(
        "Presun",
        foreign_keys="[SpojHrany.od_id, SpojHrany.do_id]",
        back_populates="presun_spoje_hran",
    )

class Hrana(Base):
    __tablename__ = "hrany"
    id = Column(Integer, primary_key=True)
    od_id = Column(ForeignKey("bod.id"))
    do_id = Column(ForeignKey("bod.id"))
    odjezd = Column(TIME)
    ddo = Column(Boolean, default=False)
    prijezd = Column(TIME)
    ddp = Column(Boolean, default=False)
    cas = Column(Integer, default=0)
    presundo = Column(Integer, default=0)
    km = Column(REAL, default=0)
    od = relationship("Checkpoint", back_populates="hrany_od", foreign_keys=[od_id])
    do = relationship("Checkpoint", back_populates="hrany_do", foreign_keys=[do_id])

    spoje = relationship("SpojHrany", back_populates="hrana", foreign_keys=[SpojHrany.hrana_id], cascade="all, delete-orphan")

    def setDoba(self, doba):
        self.cas = doba
        self.prijezd = add_time(self.odjezd,timedelta(minutes=doba))
        self.dtprijezd = make_date(self.odjezd)+timedelta(minutes=doba)

    def __lt__(self, other):
        if self.dtprijezd != other.dtprijezd:
            return self.dtprijezd < other.dtprijezd
        elif self.do == other.do:
            return self.odjezd > other.odjezd
        else:
            return self.do.id < other.do.id

    def __repr__(self):
        return f"Hrana {self.od!r} -> {self.do!r}, Odjezd: {self.odjezd!r}, Příjezd: {self.prijezd!r}"

class Presun(Base):
    __tablename__ = "presuny"
    od_id = Column(ForeignKey("bod.id"), primary_key=True)
    do_id = Column(ForeignKey("bod.id"), primary_key=True)
    km = Column(REAL)
    cas = Column(Integer)
    od = relationship("Bod", back_populates="presuny_od", foreign_keys=[od_id])
    do = relationship("Bod", back_populates="presuny_do", foreign_keys=[do_id])

    presun_spoje_hran = relationship("SpojHrany", back_populates="presun")

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
    kategorie = Column(String)
    ddo = Column(Boolean)
    ddp = Column(Boolean)
    poradi = Column(Integer)

    stanice = relationship("Bod", back_populates="stops", foreign_keys=[bod_id])

    def __repr__(self):
        return f"Stop {self.stanice!r} {self.vlak!r}"

class Spoj(Base):
    __tablename__ = "spoj"
    id = Column(Integer, primary_key=True)
    od_id = Column(ForeignKey("bod.id"))
    do_id = Column(ForeignKey("bod.id"))
    odjezd = Column(TIME)
    ddo = Column(Boolean)
    prijezd = Column(TIME)
    ddp = Column(Boolean)
    vlak_id = Column(Integer)
    kategorie = Column(String)
    cas = Column(Integer)
    remove = Column(Boolean, default=False)
    od = relationship("Bod", back_populates="spoje_od", foreign_keys=[od_id])
    do = relationship("Bod", back_populates="spoje_do", foreign_keys=[do_id])

    # spoje_hran = relationship("SpojHrany", back_populates="spoj", foreign_keys=[SpojHrany.spoj_id])

    def __repr__(self):
        return f"Spoj {self.od!r} -> {self.do!r}, Odjezd: {self.odjezd!r}, Příjezd: {self.prijezd!r}"

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

    spoje_od = relationship("Spoj", back_populates="od", foreign_keys=[Spoj.od_id])
    spoje_do = relationship("Spoj", back_populates="do", foreign_keys=[Spoj.do_id])

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
    docile = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "checkpoint",
    }

    hrany_od = relationship("Hrana", back_populates="od", foreign_keys=[Hrana.od_id])
    hrany_do = relationship("Hrana", back_populates="do", foreign_keys=[Hrana.do_id])





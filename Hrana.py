from dateutils import *
from db import Session
from models import Presun,Spoj

class SpojHranyx:

    def __init__(self, presun_od, presun_do, spoj_id):
        self.presun_od = presun_od
        self.presun_do = presun_do
        self.spoj = spoj_id

    def __repr__(self):
        session = Session()
        if self.spoj:
            spoj = session.get(Spoj,self.spoj)
            return f"Vlak {spoj.kategorie!r} {spoj.vlak_id!r}: {spoj.od!r} -> {spoj.do!r}, Odjezd: {spoj.odjezd!r}, Příjezd: {spoj.prijezd!r}"
        else:
            presun = session.get(Presun,[self.presun_od,self.presun_do])
            return f"Přesun {presun.od!r} -> {presun.do!r}"


class Hranax:

    def __init__(self, od, do, odjezd, doba):
        self.od = od
        self.do = do
        self.odjezd = odjezd
        self.setDoba(doba)
        self.km = 0
        self.presundo = 0
        self.spoje = []


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
            return self.do < other.do

    def vypisTrasu(self):
        for spoj in self.spoje:
            print(spoj)

    def __repr__(self):
        return f"Hrana {self.od!r} -> {self.do!r}, Odjezd: {self.odjezd!r}, Příjezd: {self.prijezd!r}"
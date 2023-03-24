from datetime import datetime,date,timedelta
from settings import *
from models import Checkpoint, Bod
from db import Session
from HranaTrasy import HranaTrasy
from time import perf_counter

class Trasa:

    def countVykon(self):
        if VYKON == 1:
            self.countVykon1()
        elif VYKON == 2:
            self.countVykon2()

    def countVykon1(self):
        doba = self.cas - starttime
        doba = doba - KOEF_VZD * (1 - doba / zlom) * (ciltime-self.docile)
        doba = doba.total_seconds()
        penale = max(0, (self.km - kmsec * doba) * PENALE)
        if doba:
            self.vykon = (self.body - penale) / doba * 60.0 * 60.0
        else:
            self.vykon = 0.0

    def countVykon2(self):
        doba = self.cas - starttime
        doba = doba - KOEF_VZD * (1 - doba / zlom) * (ciltime-self.docile)
        doba = doba.total_seconds()
        penale = max(0, (self.km - kmsec * doba) * PENALE)
        if doba:
            self.vykon = self.body - penale - doba / 60.0 / 60.0
        else:
            self.vykon = 0.0

    def setBody(self, x):
        self.body = x
        self.countVykon()

    def setCas(self, x):
        self.cas = x
        self.countVykon()

    def setKm(self, x):
        self.km = x
        self.countVykon()

    def __lt__(self, other):
        return self.vykon > other.vykon

    def vypisSpoje(self):
        for hrana in self.hrany:
            hrana.vypis_spoje()

    def vypisHlavicku(self):
        premie = [x.premie_c for x in self.hrany]
        session = Session()
        print(f'Stanice: {session.get(Checkpoint,self.stanice).name}, Cas: {self.cas}, '
              
              f'Body: {self.body}, Km: {round(self.km,1)}, Vykon: {round(self.vykon,2)}, '
              f'Premie: {sum(premie)}')

    def vypisPointy(self):
        od = self.start
        session = Session()
        for hrana in self.hrany:
            if hrana.spanek:
                cil = od
                km = 0
                body = 5
            elif hrana.presun:
                cil = hrana.presun.do_id
                km = hrana.presun.km
                body = hrana.presun.body
            else:
                cil = hrana.hrana.do_id
                km = hrana.hrana.km
                body = hrana.hrana.body
            print(f'Od: {session.get(Checkpoint,od).name}, Do: {session.get(Checkpoint,cil).name}, Odjezd: {hrana.odjezd}, Prijezd: {hrana.prijezd}, '
                  f'Km: {round(km,1)}, Body: {body}, '
                  f'Premie: {hrana.premie_c+hrana.premie_d+hrana.premie_p+hrana.premie_k+hrana.premie_u}')
            od = cil

    def to_dict(self):
        return {'idstanice': self.stanice.id,
                'idstart': self.start.id,
                'cas': self.cas,
                'body': self.body,
                'km': self.km,
                'kraje': self.kraje,
                'postupka': self.postupka,
                'inday': self.inday,
                'vykon': self.vykon,
                'visited': self.visited,
                'hrany': [x.to_dict() for x in self.hrany]}


    def getNewTrasaDb(self, cas, cil, body, kraj, premie1, premie2, presunx, sec, docile, presun=None, hrana=None, spanek=None):
        c1,c2,c3,c4,c5,c6,c7 = sec
        c1 -= perf_counter()
        result = Trasa()
        result.presunx = presunx
        result.start = self.start
        result.stanice = cil
        result.docile = docile
        if cil == OLOMOUC:
            new_cas = ciltime
        elif cil == PRAHA:
            if prahatime1<cas.time()<=prahatime2:
                new_cas=datetime.combine(cas.date(),prahatime2)
            elif prahatime2<cas.time():
                new_cas = datetime.combine(cas.date(), prahatime1)+timedelta(days=1)
            else:
                new_cas = datetime.combine(cas.date(), prahatime1)
        else:
            new_cas = cas
        result.cas = new_cas
        druhyden = new_cas.date() > self.cas.date()
        if druhyden:
            result.inday = 1
            result.kraje = set()
            result.postupka = set()
        else:
            result.inday = self.inday + 1
            result.kraje = self.kraje.copy()
            result.postupka = self.postupka.copy()
        if druhyden or (cil == OLOMOUC):
            result.utecha = True
            if COUNT_PREMIE and self.utecha:
                new_premie_u = 2
            else:
                new_premie_u = 0
        else:
            new_premie_u = 0
            result.utecha = self.utecha
        c1 += perf_counter()
        c2 -= perf_counter()
        if (presun or hrana):
            if (kraj in range(1, 14)):
                result.kraje.add(kraj)
            result.postupka.add(body)
            result.postupka1 = {2, 3, 4, 5}.issubset(result.postupka)
            result.postupka2 = {3, 4, 5, 6}.issubset(result.postupka)
            if (result.inday in [6, 7, 8, 9]) and (cil != OLOMOUC):
                new_premie_d = 1
            else:
                new_premie_d = 0
            if (len(self.kraje) == 3) and (len(result.kraje) == 4):
                new_premie_k = 2
            else:
                new_premie_k = 0
            if COUNT_PREMIE and (new_cas <= premie2):
                new_premie_c = 2
                new_utecha = False
            elif (presun or hrana) and COUNT_PREMIE and (new_cas <= premie1):
                new_premie_c = 1
                new_utecha = False
            else:
                new_premie_c = 0
            if self.postupka1 and result.postupka2:
                new_premie_p = 1
            elif result.postupka2 and not self.postupka2:
                new_premie_p = 3
            elif result.postupka1 and not self.postupka1:
                new_premie_p = 2
            else:
                new_premie_p = 0
        else:
            result.postupka1 = False
            result.postupka2 = False
            new_premie_c = 0
            new_premie_d = 0
            new_premie_k = 0
            new_premie_p = 0
        c2 += perf_counter()
        c3 -= perf_counter()
        result.body = self.body+body+new_premie_p+new_premie_k+new_premie_c+new_premie_d+new_premie_u
        new_hrana = HranaTrasy(odjezd=self.cas, prijezd=new_cas, premie_c=new_premie_c,premie_d=new_premie_d,
                               premie_k=new_premie_k,premie_p=new_premie_p,premie_u=new_premie_u)
        if spanek:
            new_hrana.spanek = True
        elif presun:
            new_hrana.presun = presun
        elif hrana:
            new_hrana.hrana = hrana
        c3 += perf_counter()
        c4 -= perf_counter()
        result.hrany = self.hrany.copy()
        result.hrany.append(new_hrana)
        c4 += perf_counter()
        c5 -= perf_counter()
        result.visited = self.visited.copy()
        if spanek:
            result.visited.add(SPANEK)
            result.km = self.km
        elif presun:
            result.visited.add(cil)
            result.km = self.km+presun.km
        else:
            result.visited.add(cil)
            result.km = self.km + hrana.km
        c5 += perf_counter()
        c6 -= perf_counter()
        result.countVykon()
        c6 += perf_counter()
        c7 += 1
        return result,[c1,c2,c3,c4,c5,c6,c7]

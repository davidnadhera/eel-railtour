from datetime import date, time, datetime, timedelta
from Trasa import Trasa
import pickle
import heapdict
import bisect
from settings import *
from db import Session
from models import Hrana, Presun, Checkpoint, Bod
from sqlalchemy import func,case
from time import perf_counter
from dateutils import make_date


def doIterace(iterace,x):
    pocet = 0
    global a,b,c,d,e,f,g
    global c1, c2, c3, c4, c5, c6, c7
    new_iterace = heapdict.heapdict()
    print(x)
    while len(iterace) and (pocet<MAX_V_ITERACI):
        pocet += 1
        pocet_h = 0
        ((idstanice,frozen_visited),trasa) = iterace.popitem()
        visited = set(frozen_visited)
        alt_cas = trasa.cas + UNAVA * timedelta(minutes=trasa.presunx)



        if (alt_cas.time(),idstanice) in cache:
            a -= perf_counter()
            hrany = cache[(alt_cas.time(),idstanice)]
            a += perf_counter()
        else:
            f -= perf_counter()
            subquery = session.query(
                Hrana,
                Checkpoint.docile,Checkpoint.body,Checkpoint.kraj,Checkpoint.premie1,Checkpoint.premie2,
                Checkpoint.presunx,
                func.rank().over(
                    order_by=[case(
                        (Hrana.odjezd < alt_cas.time(), 1),
                        else_=0
                    ),Hrana.odjezd],
                    partition_by=Hrana.do_id
                ).label('rnk'),
                (60*Checkpoint.body/(Hrana.cas+1440*(case(
                        (Hrana.odjezd < alt_cas.time(), 1),
                        else_=0
                    )+func.julianday(Hrana.odjezd)-func.julianday(alt_cas.time())))).label('vykon')
            ).join(Checkpoint, Hrana.do).filter(Checkpoint.active,Hrana.od_id==idstanice)

            subquery=subquery.subquery()

            query = session.query(subquery).filter(
                subquery.c.rnk == 1
            )

            hrany = query.all()
            hrany.sort(key=lambda x: x.vykon, reverse=True)
            cache[(alt_cas.time(),idstanice)] = hrany
            f += perf_counter()

        for hrana in hrany:
            if ((hrana.vykon >= LIMIT_VYKON) and (pocet_h <= MAX_V_ITERACI/10)) or (hrana.do_id in CILS) or (pocet<=LIMIT_POCET) or (x<=2):
                pocet_h += 1
                if (hrana.do_id in visited) or ((trasa.cas<=BLOCK_DO) and hrana.do_id in TEMP_BLOCK):
                    continue
                b -= perf_counter()
                if hrana.odjezd<alt_cas.time():
                    new_cas = datetime.combine(alt_cas.date(),hrana.odjezd) + timedelta(days=1) + timedelta(minutes=hrana.cas) + UNAVA*timedelta(minutes=hrana.presundo)
                else:
                    new_cas = datetime.combine(alt_cas.date(),hrana.odjezd) + timedelta(minutes=hrana.cas) + UNAVA*timedelta(minutes=hrana.presundo)
                b += perf_counter()

                if (new_cas-trasa.cas > timedelta(hours=12)) or (new_cas > hrana.docile) or (new_cas>CIL_DO):
                    continue
                c -= perf_counter()
                if ((hrana.vykon >= LIMIT_VYKON) and (pocet_h <= LIMIT_POCET)) or (pocet<=MAX_V_ITERACI/10) or (x<=2) or ((new_cas>=CIL_OD) and (new_cas<=CIL_DO)):
                    new_trasa,[c1,c2,c3,c4,c5,c6,c7] = trasa.getNewTrasaDb(hrana=hrana,cil=hrana.do_id,cas=new_cas,body=hrana.body,kraj=hrana.kraj,
                                                    premie1=hrana.premie1, premie2=hrana.premie2, presunx=hrana.presunx, sec=[c1,c2,c3,c4,c5,c6,c7],
                                                                           docile=hrana.docile)
                    c += perf_counter()
                    d -= perf_counter()
                    if hrana.do_id != OLOMOUC:
                        if ((hrana.do_id,frozenset(new_trasa.visited)) not in new_iterace) \
                                or (new_iterace[(hrana.do_id,frozenset(new_trasa.visited))].vykon < new_trasa.vykon):
                            new_iterace[(hrana.do_id,frozenset(new_trasa.visited))] = new_trasa
                    if (hrana.do_id in CILS) and (new_cas>=CIL_OD) and (new_cas<=CIL_DO):
                        vysledky.append(new_trasa)
                    d += perf_counter()

        if idstanice in cache_pres:
            a -= perf_counter()
            presuny = cache_pres[idstanice]
            a += perf_counter()
        else:
            e -= perf_counter()
            presuny = session.query(Presun.do_id,Presun.cas,Presun.km,Checkpoint.docile,Checkpoint.body,Checkpoint.kraj,
                                    Checkpoint.premie1,Checkpoint.premie2,Checkpoint.presunx)\
                .join(Checkpoint, Presun.do).filter(Checkpoint.active,Presun.od_id==idstanice)

            presuny = presuny.all()

            e += perf_counter()
            cache_pres[idstanice] = presuny

        for presun in presuny:
            if (presun.do_id in visited) or ((trasa.cas<=BLOCK_DO) and presun.do_id in TEMP_BLOCK):
                continue
            new_cas = trasa.cas+timedelta(minutes=presun.cas)*(1+UNAVA)
            if (new_cas > presun.docile) or (new_cas>CIL_DO):
                continue
            c -= perf_counter()
            new_trasa,[c1,c2,c3,c4,c5,c6,c7] = trasa.getNewTrasaDb(presun=presun,cas=new_cas,cil=presun.do_id,body=presun.body,kraj=presun.kraj,
                                            premie1=presun.premie1, premie2=presun.premie2, presunx=presun.presunx, sec=[c1,c2,c3,c4,c5,c6,c7],
                                                                   docile=presun.docile)
            c += perf_counter()
            d -= perf_counter()
            if ((presun.do_id,frozenset(new_trasa.visited)) not in new_iterace) \
                    or (new_iterace[(presun.do_id,frozenset(new_trasa.visited))].vykon < new_trasa.vykon):
                new_iterace[(presun.do_id,frozenset(new_trasa.visited))] = new_trasa
            if (presun.do_id in CILS) and (new_cas>=CIL_OD) and (new_cas<=CIL_DO):
                vysledky.append(new_trasa)
            d += perf_counter()

        g -= perf_counter()

        if (SPANEK not in visited) and ((trasa.cas.time()<=time(hour=2)) or (trasa.cas.time()>=time(hour=20))) \
        and (trasa.cas<=SPANEK_DO) and (trasa.cas>=SPANEK_OD):
            new_cas = trasa.cas+timedelta(hours=6)
            new_trasa, [c1,c2,c3,c4,c5,c6,c7] = trasa.getNewTrasaDb(spanek=True, cas=new_cas, cil=trasa.stanice, body=5, kraj=None,
                                            premie1=None, premie2=None, presunx=trasa.presunx, sec=[c1,c2,c3,c4,c5,c6,c7],
                                                                    docile=trasa.docile)
            if ((idstanice,frozenset(new_trasa.visited)) not in new_iterace) \
                    or (new_iterace[(idstanice,frozenset(new_trasa.visited))].vykon < new_trasa.vykon):
                new_iterace[(idstanice,frozenset(new_trasa.visited))] = new_trasa
            if (idstanice in CILS) and (new_cas < CIL_DO) and (new_cas > CIL_OD):
                vysledky.append(new_trasa)
        g += perf_counter()
    return new_iterace

vysledky = []
session = Session()

with open('data/schema.pickle', 'rb') as handle:
    graf = pickle.load(handle)
try:
    with open(f'data/cache{UNAVA}.pickle', 'rb') as handle:
        cache = pickle.load(handle)
except FileNotFoundError:
    cache = {}
try:
    with open('data/cache_pres.pickle', 'rb') as handle:
        cache_pres = pickle.load(handle)
except FileNotFoundError:
    cache_pres = {}
if not USE_VYKON:
    vykony = {}
else:
    with open('data/vykony.pickle', 'rb') as handle:
        vykony = pickle.load(handle)



iterace = heapdict.heapdict()
start = Trasa()
start.cas = starttime
start.body = 0
start.km = 0.0
start.kraje = set()
start.hrany = []
start.visited = set()
start.stanice = START
start.start = START
start.postupka = set()
start.postupka1 = False
start.postupka2 = False
start.docile = ciltime
start.countVykon()
start.inday = 0
start.utecha = True
start.presunx = 0
iterace[(START,frozenset([START]))] = start
x = 0
a=b=c=d=e=f=g=0
c1=c2=c3=c4=c5=c6=c7=0


while len(iterace):
    x += 1
    iterace = doIterace(iterace,x)

vysledky.sort(reverse=True, key=lambda x:(x.vykon,x.body,-x.km))

with open(f'data/cache{UNAVA}.pickle', 'wb') as handle:
    pickle.dump(cache, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open(f'data/cache_pres.pickle', 'wb') as handle:
    pickle.dump(cache_pres, handle, protocol=pickle.HIGHEST_PROTOCOL)

if len(vysledky)>0:
    trasa = vysledky[0]
    trasa.vypisHlavicku()
    trasa.vypisPointy()
    # trasa.vypisSpoje()
else:
    print('Žádné výsledky')

print(a,b,c,d,e,f,g)
print(c1,c2,c3,c4,c5,c6,c7)
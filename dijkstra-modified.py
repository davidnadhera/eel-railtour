from datetime import date, time, datetime, timedelta
import heapdict
from copy import copy
from db import Session
from models import Spoj,Bod,Checkpoint,Presun,Stanice
from dateutils import add_time, make_time, make_date
import pickle
from Spoj import Spojx
from Hrana import Hranax,SpojHranyx


def dijkstra(start,casy):
    h = heapdict.heapdict()
    hotovo = {}
    prvni = {}
    for cas in casy:
        for s in stanice:
            if s == start:
                doba=0
            else:
                doba=14400
            my_trasa = Hranax(start.id,s.id,cas,doba)
            h[(s,cas)] = my_trasa
    for s in stanice:
        hotovo[s] = time(0,0)
        prvni[s] = time(23,59)
        if s.type=='checkpoint':
            hrany[s.id] = []
    x=0
    ((curr_stanice,curr_odjezd),temptrasa) = h.popitem()
    while len(h) and ((x==0) or (temptrasa.cas <= 2880)):
        x+=1
        if (hotovo[curr_stanice]>curr_odjezd) or \
           (temptrasa.cas >= 1440) or \
           ((curr_odjezd>temptrasa.prijezd) and (temptrasa.prijezd>=prvni[curr_stanice])):
            ((curr_stanice,curr_odjezd),temptrasa) = h.popitem()
            continue
        hotovo[curr_stanice] = curr_odjezd
        if prvni[curr_stanice] == time(23,59):
            prvni[curr_stanice] = temptrasa.prijezd
        curr_cas = make_date(temptrasa.odjezd)+timedelta(minutes=temptrasa.cas)
        if (curr_stanice.type == 'checkpoint'):
            if (curr_stanice != start):
                temptrasa.do = curr_stanice.id
                hrany[temptrasa.do].append(temptrasa)
            if temptrasa.cas:
                ((curr_stanice,curr_odjezd),temptrasa) = h.popitem()
                continue
        curr_presuny = session.query(Presun).filter(Presun.od == curr_stanice).all()
        if (curr_stanice.type == 'checkpoint') or (temptrasa.presundo>0):
            curr_presuny = [presun for presun in curr_presuny if presun.do.type=='stanice']
        for presun in curr_presuny:
            new_doba = temptrasa.cas + presun.cas
            new_key = (presun.do,temptrasa.odjezd)
            # new_prijezd = make_date(temptrasa.odjezd)+new_doba
            # new_key2 = (next_stan['idstanicedo'],new_prijezd.time())
            if ((new_key in h) and (new_doba<h[new_key].cas)):
                newtrasa = copy(temptrasa)
                newtrasa.setDoba(new_doba)
                newtrasa.spoje = list(temptrasa.spoje)
                newtrasa.spoje.append(SpojHranyx(presun.od.id,presun.do.id,None))
                newtrasa.km = temptrasa.km + presun.km
                newtrasa.presundo = presun.cas
                newtrasa.do = presun.do.id
                h[new_key] = newtrasa

        if (temptrasa.presundo == 0) and (curr_stanice.type == 'stanice'):
            curr_cas += timedelta(minutes=session.get(Stanice,curr_stanice.id).prestup)
        if curr_stanice.id in gvd:
            curr_gvd_idstanice = gvd[curr_stanice.id]
            for next_stan_id in curr_gvd_idstanice:
                if curr_gvd_idstanice[next_stan_id][-1].odjezd < curr_cas.time():
                    curr_spoj = curr_gvd_idstanice[next_stan_id][0]
                    new_cas = datetime.combine(curr_cas.date(),curr_spoj.odjezd) + timedelta(minutes=1440)
                else:
                    for spoj in curr_gvd_idstanice[next_stan_id]:
                        if spoj.odjezd >= curr_cas.time():
                            curr_spoj = spoj
                            new_cas = datetime.combine(curr_cas.date(),curr_spoj.odjezd)
                            break
                new_doba = (new_cas - make_date(temptrasa.odjezd)).total_seconds()/60 + curr_spoj.doba
                next_stan = session.get(Bod,next_stan_id)
                new_key = (next_stan,temptrasa.odjezd)
                # new_prijezd = make_date(temptrasa.odjezd)+new_doba
                # new_key2 = (next_stan,new_prijezd.time())
                if (new_key in h) and (new_doba<h[new_key].cas):
                    newtrasa = copy(temptrasa)
                    newtrasa.setDoba(new_doba)
                    newtrasa.spoje = list(temptrasa.spoje)
                    newtrasa.spoje.append(SpojHranyx(None, None, curr_spoj.id))
                    newtrasa.presundo = 0
                    newtrasa.do = next_stan_id
                    h[new_key] = newtrasa
        ((curr_stanice,curr_odjezd),temptrasa) = h.popitem()

session = Session()
schema = {}
neuzly = session.query(Stanice.id).filter(Stanice.uzel==False).all()
stanice = session.query(Bod).filter(Bod.id not in neuzly).all()
with open('data/gvd.pickle', 'rb') as handle:
    gvd = pickle.load(handle)

# for start in range(3293,3294):
for start in list(range(3000,3297))+[3333]:
    print(start)
    hrany = {}
    start_checkpoint = session.get(Bod,start)
    if start not in [3000,3333]:
        odj_stanice = [x for x in start_checkpoint.sousede_tam if x.type == 'stanice']
        odjezdy = [(y,x.odjezd) for y in odj_stanice for x in y.spoje_od]
        odchody = [add_time(x[1],-timedelta(minutes=session.get(Presun,(start,x[0].id)).cas)) for x in odjezdy]
        odchody = list(set(odchody))
        odchody.sort()
    elif start==3000:
        odchody=[time(8,23),time(20,23),time(2,23)]
    elif start==3333:
        odchody=[time(8,35),time(8,46),time(8,56),time(8,59),time(9,0)]

    if odchody:
        dijkstra(start_checkpoint,odchody)

    for cil in hrany:
        hrany[cil].sort(key=lambda x: x.odjezd)

    with open(f'hrany/hrany{start}.pickle', 'wb') as handle:
        pickle.dump(hrany, handle, protocol=pickle.HIGHEST_PROTOCOL)

    schema[start] = hrany

with open(f'data/hrany.pickle', 'wb') as handle:
    pickle.dump(schema, handle, protocol=pickle.HIGHEST_PROTOCOL)



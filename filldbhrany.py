from db import Session
from models import Hrana,SpojHrany
import pickle
from datetime import timedelta

session = Session()

with open('data/hrany.pickle', 'rb') as handle:
    hrany = pickle.load(handle)

for start in hrany:
    print(start)
    for cil in hrany[start]:
        print(f'->{cil}')
        for hrana in hrany[start][cil]:
            new_hrana = Hrana(od_id=start,do_id=cil,odjezd=hrana.odjezd,prijezd=hrana.prijezd,
                              ddo=False,ddp=((hrana.prijezd<hrana.odjezd) or (hrana.cas>=1440)),
                              cas=hrana.cas,presundo=hrana.presundo,km=hrana.km)
            curr_cas = hrana.odjezd
            for i,spoj in enumerate(hrana.spoje):
                new_spoj = SpojHrany()
                new_spoj.spoj_id = spoj.spoj
                new_spoj.od_id = spoj.presun_od
                new_spoj.do_id = spoj.presun_do
                if spoj.presun_od:
                    new_spoj.odjezd = curr_cas
                curr_cas = hrana.prijezd
                new_spoj.poradi = i+1
                new_hrana.spoje.append(new_spoj)
            session.add(new_hrana)
    session.commit()


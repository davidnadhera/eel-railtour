from datetime import date, time, datetime, timedelta
from models import Stanice
from Spoj import Spojx
from db import Session
import pickle
from collections import defaultdict

gvd = {}
session = Session()

def build_gvd():
    for stanice in session.query(Stanice).filter_by(uzel=True).all():
        print(stanice.id)
        odjezdy = sorted(stanice.spoje_od,key=lambda x: x.odjezd)
        if odjezdy:
            gvd[stanice.id] = {}
            for spoj in odjezdy:
                if spoj.do.id not in gvd[stanice.id]:
                    gvd[stanice.id][spoj.do.id] = []
                gvd[stanice.id][spoj.do.id].append(Spojx(cas=spoj.odjezd,id=spoj.id,doba=spoj.cas))
    return gvd

if __name__ == '__main__':
    build_gvd()

    with open('data/gvd.pickle', 'wb') as handle:
        pickle.dump(gvd, handle, protocol=pickle.HIGHEST_PROTOCOL)

    



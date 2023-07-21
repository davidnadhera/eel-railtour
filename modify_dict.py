from datetime import date, time, datetime, timedelta
from db import Session
from models import Bod,Spoj

session = Session()
body = session.query(Bod).filter(Bod.uzel).all()

for bod in body:
    print(bod)
    cile = set([spoj.do_id for spoj in bod.spoje_od])

    for cil in cile:
        spoje = session.query(Spoj).filter_by(od_id=bod.id,do_id=cil).order_by(Spoj.prijezd,Spoj.odjezd.desc())
        prev_odjezd = spoje[0].odjezd
        is_ddp = True
        for spoj in spoje:
            if is_ddp and not spoj.ddp:
                is_ddp = False
                prev_odjezd = time.min
            if spoj.ddp and not is_ddp:
                spoj.remove = True
            elif spoj.odjezd < prev_odjezd:
                spoj.remove = True
            else:
                prev_odjezd = spoj.odjezd

    session.commit()


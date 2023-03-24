import pickle
from BuildDict import build_gvd
from db import Session
from models import Bod,Checkpoint,Hrana
from sqlalchemy import case, func
from datetime import time

# with open('data/schema.pickle', 'rb') as handle:
#     gvd = pickle.load(handle)

# gvd = build_gvd()

# for trasa in gvd[3001]:
#     print(trasa)

# gvd[3001][0].vypisTrasu()

session = Session()

subquery = session.query(
    Hrana,
    Checkpoint.docile, Checkpoint.body, Checkpoint.kraj, Checkpoint.premie1, Checkpoint.premie2,
    Checkpoint.presunx,
    func.rank().over(
        order_by=[case(
            (Hrana.odjezd < time(12,0), 1),
            else_=0
        ), Hrana.odjezd],
        partition_by=Hrana.do_id
    ).label('rnk'),
    (60*Checkpoint.body / (Hrana.cas + 1440 * (case(
        (Hrana.odjezd < time(12,0), 1),
        else_=0
    ) + func.julianday(Hrana.odjezd) - func.julianday(time(12,0))))).label('vykon')
).join(Checkpoint, Hrana.do).filter(Checkpoint.active, Hrana.od_id == 3001)

subquery = subquery.subquery()

query = session.query(subquery).filter(
    subquery.c.rnk == 1
)

hrany = query.all()
hrany.sort(key=lambda x: x.vykon, reverse=True)

for hrana in hrany:
    print(hrana)

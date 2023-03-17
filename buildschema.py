from db import Session
from models import Hrana,Checkpoint
from sqlalchemy.orm import aliased
import pickle

session = Session()
ch1 = aliased(Checkpoint)
ch2 = aliased(Checkpoint)
active_hrany = session.query(Hrana,ch2.kraj,ch2.body,ch2.docile).join(ch1, Hrana.od) \
                                       .join(ch2, Hrana.do) \
                                       .filter(ch1.active==True,ch2.active==True) \
                                       .order_by(Hrana.od_id,Hrana.do_id,Hrana.odjezd)
active_chp = session.query(Checkpoint).filter(Checkpoint.active==True).order_by(Checkpoint.id).all()

schema = {}
for start in active_chp:
    print(start)
    subschema = {}
    for cil in active_chp:
        my_query = active_hrany.filter(Hrana.od==start,Hrana.do==cil).all()
        if len(my_query):
            subschema[cil.id] = [{'od': u.Hrana.od_id,
                                  'do': u.Hrana.do_id,
                                  'odjezd': u.Hrana.odjezd,
                                  'cas': u.Hrana.cas,
                                  'presundo': u.Hrana.presundo,
                                  'km': u.Hrana.km,
                                  'kraj': u.kraj,
                                  'body': u.body,
                                  'docile': u.docile} for u in my_query]
    schema[start.id] = subschema

with open('data/schema.pickle', 'wb') as handle:
    pickle.dump(schema, handle, protocol=pickle.HIGHEST_PROTOCOL)

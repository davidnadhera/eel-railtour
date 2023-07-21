
from db import Session
from models import Bod, Stop

session = Session()
date = '31.07.2023'

body = session.query(Bod).filter(Bod.id==999,Bod.uzel).order_by(Bod.id)
for bod in body:
    print(bod)
    bod.from_idos(session,date,True)
    bod.from_idos(session,date,False)

#     bod.lower_name = str.lower(bod.name)
# session.commit()
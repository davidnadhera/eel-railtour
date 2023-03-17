from db import Session
from models import Checkpoint
import random

LOS = {1:5,2:5,3:5,4:5,5:5,6:6,7:5,8:5,9:6,10:6,11:5,12:6,13:6}

session = Session()
session.get(Checkpoint,3000).active = True
session.get(Checkpoint,3333).active = True
session.get(Checkpoint,3334).active = True

for kraj in LOS.keys():
    chp = session.query(Checkpoint).filter_by(kraj=kraj,active=False).all()
    aktivovat = random.sample(chp,LOS[kraj])
    for x in aktivovat:
        x.active=True
        session.add(x)
    session.commit()

aktivovat = random.sample(range(0,12),7)
for i in aktivovat:
    session.get(Checkpoint, 3260+i*3+1).active = True
    session.get(Checkpoint, 3260+i*3+2).active = True
    session.get(Checkpoint, 3260+i*3+3).active = True
session.commit()
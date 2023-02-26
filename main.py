import eel
from db import Session
from models import Bod, Stanice, Checkpoint, Presun
from sqlalchemy import or_


session = Session()

# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
eel.init('web', allowed_extensions=['.js', '.html'])

@eel.expose                         # Expose this function to Javascript
def chplist(x):
    query_x = str.lower(f'%{x}%')
    if x:
        body = session.query(Bod) \
                      .filter(or_(Bod.lower_name.like(query_x),Bod.id.like(query_x))) \
                      .order_by(Bod.id)
        options = '\n'.join([f'<option value="{bod.id}">{bod.id} {bod.name}</option>' for bod in body])
        return options

@eel.expose                         # Expose this function to Javascript
def send_data(data):
    for trasa in data:
        bod_od = session.get(Bod,trasa['od'])
        bod_do = session.get(Bod,trasa['do'])
        if bod_od and bod_do:
            bod_od.uzel = True
            bod_do.uzel = True
            bod_od.gps_N = trasa['gps_od']['y']
            bod_od.gps_E = trasa['gps_od']['x']
            bod_do.gps_N = trasa['gps_do']['y']
            bod_do.gps_E = trasa['gps_do']['x']
            presun = session.query(Presun).filter_by(od=bod_od,do=bod_do).first()
            if presun:
                presun.km = trasa['delka']
                presun.cas = trasa['cas']
            else:
                bod_od.presuny_od.append(Presun(od=bod_od,do=bod_do,km=trasa['delka'],cas=trasa['cas']))
    try:
        session.commit()
        return "Úspěšně zapsáno"
    except Exception as e:
        session.rollback()
        return str(e)

@eel.expose                         # Expose this function to Javascript
def coords(id):
    bod = session.get(Bod,id)
    if bod:
        return {'y': bod.gps_N,'x': bod.gps_E}
    else:
        return None

body = session.query(Bod).all()
for bod in body:
    bod.lower_name = str.lower(bod.name)
session.commit()

eel.start('index.html', mode='my_portable_chromium')             # Start (this blocks and enters loop)


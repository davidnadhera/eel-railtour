from datetime import datetime,time,timedelta,date
from db import Session
from models import Stop

TRAMVAJE = [{'trasa' : [{'id':4001, 'cas':timedelta(0)},
                        {'id':4015, 'cas':timedelta(minutes=13)}],
            'intervaly' : [{'od': time(hour=4,minute=29),
                            'do': time(hour=23,minute=20),
                            'interval': timedelta(minutes=10)}],
            'basecislo' : 3000000,
            'name': 'Liberec Lidové sady -> Nádraží'},
            {'trasa': [{'id': 4015, 'cas': timedelta(0)},
                       {'id': 4001, 'cas': timedelta(minutes=15)}],
             'intervaly': [{'od': time(hour=4, minute=22),
                            'do': time(hour=23, minute=9),
                            'interval': timedelta(minutes=10)}],
             'basecislo': 3000001,
             'name': 'Liberec Nádraží -> Lidové sady'},
            {'trasa': [{'id': 4002, 'cas': timedelta(0)},
                       {'id': 4014, 'cas': timedelta(minutes=8)}],
             'intervaly': [{'od': time(hour=4, minute=42),
                            'do': time(hour=23, minute=13),
                            'interval': timedelta(minutes=12)}],
             'basecislo': 4000000,
             'name': 'Olomouc Pavlovičky -> Nádraží'},
            {'trasa': [{'id': 4014, 'cas': timedelta(0)},
                       {'id': 4002, 'cas': timedelta(minutes=8)}],
             'intervaly': [{'od': time(hour=4, minute=29),
                            'do': time(hour=23, minute=2),
                            'interval': timedelta(minutes=12)}],
             'basecislo': 4000001,
             'name': 'Olomouc Nádraží -> Pavlovičky'},
            {'trasa': [{'id': 4003, 'cas': timedelta(0)},
                       {'id': 4013, 'cas': timedelta(minutes=9)}],
             'intervaly': [{'od': time(hour=0, minute=11),
                            'do': time(hour=4, minute=12),
                            'interval': timedelta(minutes=60)},
                           {'od': time(hour=0, minute=47),
                            'do': time(hour=3, minute=48),
                            'interval': timedelta(minutes=60)},
                           {'od': time(hour=4, minute=23),
                            'do': time(hour=23, minute=47),
                            'interval': timedelta(minutes=60)}
                           ],
             'basecislo': 8000000,
             'name': 'Ostrava Karolina -> Nádraží'},
            {'trasa': [{'id': 4013, 'cas': timedelta(0)},
                       {'id': 4003, 'cas': timedelta(minutes=9)}],
             'intervaly': [{'od': time(hour=0, minute=19),
                            'do': time(hour=3, minute=20),
                            'interval': timedelta(minutes=60)},
                           {'od': time(hour=0, minute=54),
                            'do': time(hour=3, minute=55),
                            'interval': timedelta(minutes=60)},
                           {'od': time(hour=4, minute=9),
                            'do': time(hour=23, minute=54),
                            'interval': timedelta(minutes=5)}
                           ],
             'basecislo': 8000001,
             'name': 'Ostrava Nádraží -> Karolina'},
            {'trasa': [{'id': 4003, 'cas': timedelta(0)},
                       {'id': 4012, 'cas': timedelta(minutes=13)}],
             'intervaly': [{'od': time(hour=0, minute=3),
                            'do': time(hour=4, minute=4),
                            'interval': timedelta(minutes=30)},
                           {'od': time(hour=4, minute=17),
                            'do': time(hour=23, minute=59),
                            'interval': timedelta(minutes=8)}],
             'basecislo': 8100000,
             'name': 'Ostrava Karolina -> Svinov'},
            {'trasa': [{'id': 4012, 'cas': timedelta(0)},
                       {'id': 4003, 'cas': timedelta(minutes=13)}],
             'intervaly': [{'od': time(hour=0, minute=0),
                            'do': time(hour=3, minute=6),
                            'interval': timedelta(minutes=30)},
                           {'od': time(hour=3, minute=18),
                            'do': time(hour=23, minute=59),
                            'interval': timedelta(minutes=8)}],
             'basecislo': 8100001,
             'name': 'Ostrava Svinov -> Karolina'},
            {'trasa': [{'id': 4010, 'cas': timedelta(0)},
                       {'id': 4004, 'cas': timedelta(minutes=8)},
                       {'id': 4011, 'cas': timedelta(minutes=24)},
                       {'id': 4005, 'cas': timedelta(minutes=32)}],
             'intervaly': [{'od': time(hour=4, minute=20),
                            'do': time(hour=23, minute=30),
                            'interval': timedelta(minutes=15)}],
             'basecislo': 2000000,
             'name': 'Most -> Litvínov'},
            {'trasa': [{'id': 4005, 'cas': timedelta(0)},
                       {'id': 4011, 'cas': timedelta(minutes=8)},
                       {'id': 4004, 'cas': timedelta(minutes=24)},
                       {'id': 4010, 'cas': timedelta(minutes=28)}],
             'intervaly': [{'od': time(hour=4, minute=27),
                            'do': time(hour=23, minute=59),
                            'interval': timedelta(minutes=15)}],
             'basecislo': 2000001,
             'name': 'Litvínov -> Most'},
            {'trasa': [{'id': 4006, 'cas': timedelta(0)},
                       {'id': 4009, 'cas': timedelta(minutes=13)}],
             'intervaly': [{'od': time(hour=4, minute=38),
                            'do': time(hour=23, minute=59),
                            'interval': timedelta(minutes=5)}],
             'basecislo': 1000000,
             'name': 'Plzeň Bolevec -> Nádraží'},
            {'trasa': [{'id': 4009, 'cas': timedelta(0)},
                       {'id': 4006, 'cas': timedelta(minutes=15)}],
             'intervaly': [{'od': time(hour=4, minute=19),
                            'do': time(hour=23, minute=59),
                            'interval': timedelta(minutes=5)}],
             'basecislo': 1000001,
             'name': 'Plzeň Nádraží -> Bolevec'},
            {'trasa': [{'id': 4007, 'cas': timedelta(0)},
                       {'id': 4008, 'cas': timedelta(minutes=17)}],
             'intervaly': [{'od': time(hour=4, minute=34),
                            'do': time(hour=23, minute=40),
                            'interval': timedelta(minutes=4)}],
             'basecislo': 1100000,
             'name': 'Plzeň Košutka -> Chodské náměstí'},
            {'trasa': [{'id': 4008, 'cas': timedelta(0)},
                       {'id': 4007, 'cas': timedelta(minutes=17)}],
             'intervaly': [{'od': time(hour=4, minute=43),
                            'do': time(hour=23, minute=45),
                            'interval': timedelta(minutes=4)}],
             'basecislo': 1100001,
             'name': 'Plzeň Chodské náměstí -> Košutka'},
            ]
den = date(day=10, month=8, year=2022)
session = Session()

for linka in TRAMVAJE:
    curr_cislo = linka['basecislo']
    for interval in linka['intervaly']:
        curr_time = datetime.combine(den,interval['od'])
        while curr_time < datetime.combine(den,interval['do']):
            for i,stop in enumerate(linka['trasa']):
                new_stop = Stop(bod_id=stop['id'],kategorie='tram',vlak_id=curr_cislo,poradi=i+1)
                new_stop.vlak = new_stop.kategorie + ' ' + str(new_stop.vlak_id)
                if i != len(linka['trasa'])-1:
                    odj = curr_time + stop['cas']
                    new_stop.odjezd = odj.time()
                    if odj.date() > den:
                        new_stop.ddo = True
                if i != 0:
                    prij = curr_time + stop['cas']
                    new_stop.prijezd = prij.time()
                    if prij.date() > den:
                        new_stop.ddp = True
                session.add(new_stop)
            curr_time = curr_time + interval['interval']
            curr_cislo = curr_cislo + 2
        session.commit()
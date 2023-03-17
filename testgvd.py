import pickle
from BuildDict import build_gvd
from db import Session
from models import Bod,Checkpoint,Hrana

with open('data/schema.pickle', 'rb') as handle:
    gvd = pickle.load(handle)

# gvd = build_gvd()

# for trasa in gvd[3001]:
#     print(trasa)

# gvd[3001][0].vypisTrasu()
data =  gvd[3293][3001]
for hrana in data:
    print(hrana)
    print('test')
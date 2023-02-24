import eel
import pandas as pd
import csv
from datetime import timedelta
from time import sleep

chp = pd.read_csv('data/stanice.csv', names=['cislo','nazev','uzel'],index_col=0)
chp['orig_nazev'] = chp.nazev
chp.nazev = chp.index.astype(str)+' '+chp.nazev

sour = pd.read_csv('data/sour2.csv', header=0,index_col=0, delimiter=';')
# new = sour.gps.str.split(", ",expand=True)
# sour['x'] = new[1].str[:-1].astype(float)
# sour['y'] = new[0].str[:-1].astype(float)
# sour = sour.drop('gps', axis=1)

 #pd.read_pickle('data/checkpointy.pickle')

# Set web files folder and optionally specify which file types to check for eel.expose()
#   *Default allowed_extensions are: ['.js', '.html', '.txt', '.htm', '.xhtml']
eel.init('web', allowed_extensions=['.js', '.html'])

@eel.expose                         # Expose this function to Javascript
def chplist(x):
    if x:
        chp_filtered = chp.loc[chp.nazev.str.contains(x, case=False),['nazev']].to_dict()['nazev']
        options = '\n'.join([f'<option value="{id}">{nazev}</option>' for (id, nazev) in chp_filtered.items()])
        return options

@eel.expose                         # Expose this function to Javascript
def send_data(x):
    print(x)
    x['cas'] = timedelta(minutes=x['cas'])
    chp.at[int(x['od']),'uzel'] = True
    with open('data/presuny.csv', 'a', newline='') as csvfile:
        fieldnames = ['od', 'do', 'cas', 'delka']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(x)

# @eel.expose
# def send_coords(x):
#     coord = pd.DataFrame.from_dict(x, orient='index')
#     coord.index = coord.index.astype(int)
#     sour = pd.concat([sour,coord])
#     sour = sour.loc[(sour > 0).all(axis=1)].sort_index()
#
#     sour.to_csv('data/sour2.csv')
#
# coords = []
# u_stanice = chp.loc[~chp.index.isin(range(3000,3999)),'orig_nazev'].to_dict()
# query = [{'id':k,'nazev':v} for k,v in u_stanice.items()]

# eel.geokoduj({'od':'Praha-Vysočany vlaková stanice',
#               'do':'Praha – Památník prvního rozhlasového vysílání v ČSR',
#               'od_id':889,
#               'do_id':3000})

@eel.expose                         # Expose this function to Javascript
def coords(id):
    if id.isnumeric():
        id = int(id)
    else:
        return None
    if id in sour.index:
        # print(sour.loc[id].to_dict())
        return sour.loc[id].to_dict()
    else:
        return None

eel.start('index.html', mode='my_portable_chromium')             # Start (this blocks and enters loop)


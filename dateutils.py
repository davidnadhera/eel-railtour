from datetime import date, time, datetime, timedelta

def make_date(x):
    return datetime.combine(date(2021,6,1),x)

def make_time(x):
    return x.time()

def add_time(cas,doba):
    return make_time(make_date(cas)+doba)
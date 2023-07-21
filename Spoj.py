from datetime import datetime, timedelta


class Spojx:
    def __init__(self, cas, id, doba):
        self.odjezd = cas
        self.id = id
        self.doba = timedelta(seconds=doba)
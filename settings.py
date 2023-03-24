from datetime import datetime,time

MAX_V_ITERACI = 5000
starttime = datetime(year=2023, month=7, day=31, hour=9, minute=0)
ciltime = datetime(year=2023, month=8, day=4, hour=16, minute=0)
prahatime1 = time(8,23)
prahatime2 = time(20,23)
# CILS = [3334]
# CIL_OD = datetime(year=2023, month=8, day=4, hour=12, minute=0)
# CIL_DO = datetime(year=2023, month=8, day=4, hour=16, minute=0)
CILS = list(range(3000,3297))
CIL_OD = datetime(year=2023, month=8, day=1, hour=6, minute=0)
CIL_DO = datetime(year=2023, month=8, day=1, hour=12, minute=0)
SPANEK = 3999
START = 3333
OLOMOUC = 3334
PRAHA = 3000
SPANEK_OD = datetime(year=2023, month=8, day=1, hour=20, minute=0)
SPANEK_DO = datetime(year=2023, month=8, day=3, hour=2, minute=0)
TEMP_BLOCK = []
BLOCK_DO = datetime(year=2023, month=8, day=2, hour=0, minute=0)
COUNT_PREMIE = False
TOTAL_KM = 185
PENALE = 0.2
UNAVA = 0
USE_VYKON = False
VYKON = 2
LIMIT_VYKON = 0
LIMIT_POCET = 50
KOEF_VZD = 0

celkdoba = (ciltime - starttime)
zlom = celkdoba/2
kmsec = TOTAL_KM/celkdoba.total_seconds()
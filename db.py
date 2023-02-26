from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
# from decouple import config

# sqlite_USERNAME = config('sqlite_USERNAME', default='postgres')
# sqlite_PASSWORD = config('sqlite_PASSWORD', default='')
# sqlite_URL = config('sqlite_URL', default='localhost')
# sqlite_PORT = config('sqlite_PORT', default=5432)
# DB_NAME = config('DB_NAME', default='HA')


# conn_string = f'postgresql://{pg_USERNAME}:{pg_PASSWORD}@{pg_URL}:{pg_PORT}/{DB_NAME}'
conn_string = 'sqlite:///data/rt23.db'
engine = create_engine(conn_string)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine, checkfirst=True)



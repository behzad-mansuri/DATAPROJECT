import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Float, String, DateTime
df_usgs = pd.read_csv('JAPAN_USGS.csv')
df_geofon = pd.read_csv('JAPAN_GEOFON.csv')
#2. create a database connection 
#MySQL:
engine=create_engine("mysql+pymysql://user:password@host:port/database_name")
metadata =MetaData()
earthquakes = Table('earthquakes', metadata,
    Column('time', DateTime),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('depth', Float),
    Column('magnitude', Float),
    Column('region', String),
    Column('source', String))

df_usgs['region'] = df_usgs['place'].str.replace(r'^.*of\s', '', regex=True)
df_usgs['source'] = 'USGS'
df_usgs['time'] = pd.to_datetime(df_usgs['time'])
df_usgs = df_usgs[['time', 'latitude', 'longitude', 'depth', 'magnitude', 'region', 'source']]
df_geofon
df_geofon['source'] = 'GEOFON'
df_geofon['time'] = pd.to_datetime(df_geofon['time'])
df_geofon = df_geofon[['time', 'latitude', 'longitude', 'depth', 'magnitude', 'region', 'source']]
df = pd.concat([df_usgs, df_geofon])
con = engine.connect()  #  اتصال به دیتابیس
df.to_sql(name='earthquakes', con=engine, if_exists='append', index=False,chunksize=1000)

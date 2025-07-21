import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, text
from dotenv import load_dotenv
import os

load_dotenv()
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

class EarthquakeLoader:
    def __init__(self, usgs_path, geofon_path):
        self.usgs_path = usgs_path
        self.geofon_path = geofon_path

    def clean_data(self, df, source):
        df['source'] = source
        df['time'] = pd.to_datetime(df['time'])

        if source == 'GEOFON' and 'region' in df.columns and 'place' not in df.columns:
            df.rename(columns={'region': 'place'}, inplace=True)

        for col in ['latitude', 'longitude', 'depth', 'mag', 'place']:
            if col not in df.columns:
                df[col] = None

        return df[['time', 'latitude', 'longitude', 'depth', 'mag', 'place', 'source']]
    
    def load_data(self):
        df_usgs = pd.read_csv(self.usgs_path)
        df_geofon = pd.read_csv(self.geofon_path)
        return pd.concat([self.clean_data(df_usgs, 'USGS'),self.clean_data(df_geofon, 'GEOFON')])
    
class DatabaseManager:
    def __init__(self, engine):
        self.engine = engine

    def create_table(self):
        earthquakes = Table('earthquakes', metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('time', DateTime, index=True),
            Column('latitude', Float),
            Column('longitude', Float),
            Column('depth', Float),
            Column('mag', Float, index=True),
            Column('place', String(255), index=True),
            Column('source', String(10)),
            Column('month', Integer, index= True))
        metadata.create_all(self.engine)

    def insert_data(self, df):
        df['time']= pd.to_datetime(df['time'], utc=True)
        df['time'] = df['time'].dt.tz_localize(None)
        df['month'] = df['time'].dt.month
        df.to_sql("earthquakes", con=self.engine, if_exists="append", index=False, chunksize=1000)

    def cleanup_data(self):
        with self.engine.connect() as conn:
            deleted = conn.execute(text("DELETE FROM earthquakes WHERE mag > 10 OR depth > 700"))
            updated = conn.execute(text("UPDATE earthquakes SET place = 'Unknown' WHERE place IS NULL"))
            print(f"Deleted suspicious records: {deleted.rowcount}")
            print(f"Updated NULL place values: {updated.rowcount}")
            conn.commit()

    def create_index(self):
        dbname = os.getenv("dbname")
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                    SELECT COUNT(1)
                    FROM information_schema.statistics
                    WHERE table_schema = :schema
                    AND table_name = 'earthquakes'
                     AND index_name = 'idx_place_month'
                    """), {"schema": dbname})
            print("Created index on (place, month)")
            conn.commit()

class EarthquakeAnalyzer:
    def __init__(self, engine):
        self.engine = engine

    def run_query(self, query, label, writer=None, sheet_name=None):
        try:
            df = pd.read_sql(query, self.engine)
            print(df)

            if writer and sheet_name:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                return df
            
        except Exception as e:
            print(f"Error in query '{label}': {e}")
            return None
        print(f"1 {sheet_name}")

    def analyze(self):
        with pd.ExcelWriter("earthquake_analysis.xlsx") as writer:
            self.run_query(text("""
                SELECT place, source, AVG(mag) AS avg_mag
                FROM earthquakes
                GROUP BY place, source
            """), "Average mag by place and source", writer, "Avg Mag by Place")

            self.run_query(text("""
                SELECT *
                FROM earthquakes
                ORDER BY mag DESC, time DESC
                LIMIT 10
            """), "Top 10 strongest earthquakes", writer, "Top 10 Quakes")

            self.run_query(text("""
                SELECT place, EXTRACT(MONTH FROM time) AS month, COUNT(*) AS count
                FROM earthquakes
                GROUP BY place, EXTRACT(MONTH FROM time)
            """), "Earthquake count per place and month", writer, "Monthly Count")

            self.run_query(text("""
                SELECT place, MAX(depth) AS max_depth, MIN(depth) AS min_depth
                FROM earthquakes
                GROUP BY place
            """), "Max and Min depth by place", writer, "Depth by Place")

            self.run_query(text("""
                SELECT place, COUNT(*) as total
                FROM earthquakes
                GROUP BY place
                ORDER BY total DESC
                LIMIT 5
            """), "Top 5 place by earthquake frequency", writer, "Most Quakes")

            self.run_query(text("""
                SELECT EXTRACT(MONTH FROM time) AS month, MAX(mag) AS max_mag
                FROM earthquakes
                GROUP BY EXTRACT(MONTH FROM time)
                ORDER BY month
            """), "Maximum mag per month", writer, "Max Mag Per Month")

            self.run_query(text("""
                SELECT source, AVG(depth) AS avg_depth
                FROM earthquakes
                GROUP BY source
            """), "Average depth by source", writer, "Avg Depth Per Source")


def main():
    loader = EarthquakeLoader("JAPAN_USGS.csv", "JAPAN_GEOFON.csv")
    df = loader.load_data()

    db = DatabaseManager(engine)
    db.create_table()
    db.insert_data(df)
    db.cleanup_data()
    db.create_index()

    analyzer = EarthquakeAnalyzer(engine)
    analyzer.analyze()

main()
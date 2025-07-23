import unittest
import csv
import os
import pandas as pd

# READ EXCEL
df = pd.read_excel("earthquake_analysis.xlsx")
df.to_csv("earthquake_analysis.csv", index=False)

# ===============================
# START UNIT TESTS
# ===============================
class TestEarthquakeCSV(unittest.TestCase):

    # ===============================
    # SET FILE NAMES
    # ===============================
    def setUp(self):
        self.usgs_file = "JAPAN_USGS.csv"
        self.geofon_file = "JAPAN_GEOFON.csv"
        self.analys_file = "earthquake_analysis.csv"

    # ===============================
    # TEST COLUMN
    # ===============================
    def test_column_count(self):
        # CHECK FILES EXIST
        self.assertTrue(os.path.exists(self.usgs_file))
        self.assertTrue(os.path.exists(self.geofon_file))

        # CHECK USGS 22 COLUMNS
        with open(self.usgs_file, newline='', encoding='utf-8') as file:
            readerU = csv.reader(file)
            header = next(readerU)
            self.assertEqual(len(header), 22)

        # CHECK GEOFON 4 COLUMNS
        with open(self.geofon_file, newline='', encoding='utf-8') as file:
            readerG = csv.reader(file)
            header = next(readerG)
            self.assertEqual(len(header), 4)

    # ===============================
    # TEST IS NUMBER
    # ===============================
    def test_mag_is_numeric(self):
        # USGS MAG CHECK
        with open(self.usgs_file, newline='', encoding='utf-8') as file:
            readerU = csv.DictReader(file)
            for i, row in enumerate(readerU, start=2):
                valU = row['mag']
                try:
                    float(valU)
                except (TypeError, ValueError):
                    self.fail(f"Row {i}: 'mag' is not numeric: {valU}")

        # GEOFON MAG CHECK
        with open(self.geofon_file, newline='', encoding='utf-8') as file:
            readerG = csv.DictReader(file)
            for i, row in enumerate(readerG, start=2):
                valG = row['mag']
                try:
                    float(valG)
                except (TypeError, ValueError):
                    self.fail(f"Row {i}: 'mag' is not numeric: {valG}")

    # ===============================
    # TEST NO EMPTY CELL
    # ===============================
    def test_not_empty(self):
        # CHECK USGS
        with open(self.usgs_file, newline='', encoding='utf-8') as file:
            readerU = csv.DictReader(file)
            for rowU in readerU:
                for valueU in rowU.values():
                    self.assertTrue(valueU and valueU.strip())

        # CHECK GEOFON
        with open(self.geofon_file, newline='', encoding='utf-8') as file:
            readerG = csv.DictReader(file)
            for rowG in readerG:
                for valueG in rowG.values():
                    self.assertTrue(valueG and valueG.strip())

    # ===============================
    # TEST MEAN
    # ===============================
    def test_mean(self):
        df = pd.read_csv(self.analys_file)
        for i, row in df.iterrows():
            valA = float(row['avg_mag'])
            self.assertTrue(4 <= valA <= 6)

samp =TestEarthquakeCSV()
samp.setUp()
samp.test_column_count()
samp.test_mag_is_numeric()
samp.test_mean()

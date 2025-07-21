import unittest
import csv
import os

class TestEarthquakeCSV(unittest.TestCase):

    def setUp(self):
        self.usgs_file = "JAPAN_USGS.csv"
        self.geofon_file = 'JAPAN_GEOFON.csv'

    def test_column_count(self):
        self.assertTrue(os.path.exists(self.usgs_file))
        self.assertTrue(os.path.exists(self.geofon_file))

        with open(self.usgs_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            self.assertEqual(len(header), 22)

        with open(self.geofon_file, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            self.assertEqual(len(header), 4)


    def test_mag_is_numeric(self):
        with open(self.usgs_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader, start=2):
                valU = row['mag']
                try:
                    float(valU)
                except (TypeError):
                    self.fail(f"Row {i}: 'mag' is not numeric: {valU}")

        with open(self.geofon_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader, start=2):
                valG = row['mag']
                try:
                    float(valG)
                except (TypeError):
                    self.fail(f"Row {i}: 'mag' is not numeric: {valG}")

    def test_not_empty(self):
        with open(self.usgs_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.assertTrue(row)

        with open(self.geofon_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.assertTrue(row)
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta 
import re
import csv 
import matplotlib.pyplot as plt

#Sectione 1 (scrapping_section)
#USGS
end_date = datetime.today().date() 
start_date = end_date - timedelta(days=90) 
 
url = "https://earthquake.usgs.gov/fdsnws/event/1/query" 
params = { 
    "format": "csv", 
    "starttime": str(start_date), 
    "endtime": str(end_date + timedelta(days=1)), 
    "minlatitude": 24, 
    "maxlatitude": 46, 
    "minlongitude": 123, 
    "maxlongitude": 146, 
    "minmagnitude": 4 
} 
 
response = requests.get(url, params=params) 

with open("JAPAN_USGS.csv", "w", encoding="utf-8") as f: 
    f.write(response.text) 


#GEOFON


url2 = f"https://geofon.gfz.de/eqinfo/list.php?datemin={start_date}&datemax={end_date}&latmax=46&lonmin=123&lonmax=146&latmin=24&magmin=4&fmt=html&nmax=1000"
response2 = requests.get(url2)
soup = BeautifulSoup(response2.content , "html.parser")
data_containers = soup.find_all("div" , class_= lambda items : items is not None and "flex-row row" in items)


Mag=[]
Region=[]
Depth = []
Time = []

for data in data_containers:
    mag = data.find("span" , class_ = "magbox")
    pattern = r'\b\d+\.\d+\b'
    if mag is not None:
        selected = re.search(pattern ,mag.text)
        Mag.append(selected.group())

    region = data.find("strong")
    if region is not None:
        Region.append(region.text)


    depth = data.find("span" , class_ = "pull-right")
    selected2 = re.search("[0-9][0-9]", depth.text)
    Depth.append(selected2.group() if selected2 else None)

    time = data.find_all("div" , class_ = "col-xs-12")
    texts = (text for text in time[1].find_all(string=True, recursive=False))
    result_text = ''.join(texts)
    Time.append(result_text.strip())

Time.pop(0)

final_data = {"mag" : Mag , "region" : Region , "time" : Time , "depth" : Depth}




final_text = "region  mag  time  depth\n"
for r, m, t, d in zip(final_data["region"], final_data["mag"], final_data["time"], final_data["depth"]):
    final_text += f"{r}  {m}  {t}  {d}\n"

csv_filename = "JAPAN_GEOFON.csv"


headers = ["region", "mag", "time", "depth"]


with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(headers)

    for r, m, t, d in zip(final_data["region"], final_data["mag"], final_data["time"], final_data["depth"]):
        writer.writerow([r, m, t, d])

#Section_2
import pandas as pd

def get_pandas():
#1
    df_geofon = pd.read_csv('JAPAN_GEOFON.csv')
    df_usgs = pd.read_csv('JAPAN_USGS.csv')
    print("Shape of data from geofon")
    print(df_geofon.shape)
    print("Shape of data from usgs")
    print(df_usgs.shape)

#2
    print("Type of data from geofon")
    print(df_geofon.dtypes)
    print("Type of data from usgs")
    print(df_usgs.dtypes)

#3
    df_geofon['time'] = pd.to_datetime(df_geofon['time'])
    df_geofon['mag'] = pd.to_numeric(df_geofon['mag'], errors='coerce').astype(float)
    df_geofon['depth'] = pd.to_numeric(df_geofon['depth'], errors='coerce').astype(float)
    df_usgs['time'] = pd.to_datetime(df_usgs['time'])
    df_usgs['updated'] = pd.to_datetime(df_usgs['updated'])
    df_usgs['latitude'] = pd.to_numeric(df_usgs['latitude'], errors='coerce').astype(float)
    df_usgs['longitude'] = pd.to_numeric(df_usgs['longitude'], errors='coerce').astype(float)
    df_usgs['depth'] = pd.to_numeric(df_usgs['depth'], errors='coerce').astype(float)
    df_usgs['mag'] = pd.to_numeric(df_usgs['mag'], errors='coerce').astype(float)
    df_usgs['nst'] = pd.to_numeric(df_usgs['nst'], errors='coerce').astype(float)
    df_usgs['gap'] = pd.to_numeric(df_usgs['gap'], errors='coerce').astype(float)
    df_usgs['dmin'] = pd.to_numeric(df_usgs['dmin'], errors='coerce').astype(float)
    df_usgs['rms'] = pd.to_numeric(df_usgs['rms'], errors='coerce').astype(float)
    df_usgs['horizontalError'] = pd.to_numeric(df_usgs['horizontalError'], errors='coerce').astype(float)
    df_usgs['depthError'] = pd.to_numeric(df_usgs['depthError'], errors='coerce').astype(float)
    df_usgs['magError'] = pd.to_numeric(df_usgs['magError'], errors='coerce').astype(float)
    df_usgs['magNst'] = pd.to_numeric(df_usgs['magNst'], errors='coerce').astype(float)
    print("Type of data from geofon after changes")
    print(df_geofon.dtypes)
    print("Type of data from usgs after changes")
    print(df_usgs.dtypes)

#4
    print("Sum of NaN in data from geofon")
    print(df_geofon.isna().sum())
    print("Sum of NaN in data from usgs")
    print(df_usgs.isna().sum())
    df_geofon = df_geofon.dropna()
    print("Sum of NaN in data from geofon after changes")
    print(df_geofon.isna().sum())

#5
    df_geofon['Month_Name'] = df_geofon['time'].dt.month_name()
    df_usgs['Month_Name'] = df_usgs['time'].dt.month_name()

#6
    df_geofon['Category'] = df_geofon['mag'].apply(lambda x: 'Weak' if x < 5 else 'Moderate' if 5 <= x < 6 else 'Strong')
    df_usgs['Category'] = df_usgs['mag'].apply(lambda x: 'Weak' if x < 5 else 'Moderate' if 5 <= x < 6 else 'Strong')
    print("Data from geofon after changes")
    print(df_geofon)
    print("Data from usgs after changes")
    print(df_usgs)

    #7
    df_geofon_grouped = df_geofon.groupby(['Month_Name', 'Category']).agg(count = ('mag','count'), mean_mag = ('mag', 'mean')).reset_index()
    df_usgs_grouped = df_usgs.groupby(['Month_Name', 'Category']).agg(count = ('mag','count'), mean_mag = ('mag', 'mean')).reset_index()
    print("df_geofon_grouped:")
    print(df_geofon_grouped)
    print("df_usgs_grouped:")
    print(df_usgs_grouped)

    #8 
    df_usgs['area_name'] = df_usgs['place'].str.replace(r'^.*of\s', '', regex=True)
    df_geofon['area_name'] = df_geofon['region']

#9
    df_geofon_grouped_area_name = df_geofon.groupby(['area_name']).agg(count = ('mag','count'), mean_mag = ('mag', 'mean'), mean_depth = ('depth', 'mean'), max_mag = ('mag', 'max'), max_depth = ('depth', 'max')).reset_index()
    print(df_geofon_grouped_area_name)
    df_geofon_grouped_area_name.set_index('area_name')['count'].plot(
        kind='bar',
        figsize=(12, 6),
        color='skyblue',
        title='Count_of_earthquakes_per_region'
    )
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#Numpy
#1
def get_numpy():
    import numpy as np
    df_geofon = pd.read_csv('JAPAN_GEOFON.csv')
    df_usgs = pd.read_csv('JAPAN_USGS.csv')
    df_usgs['area_name'] = df_usgs['place'].str.replace(r'^.*of\s', '', regex=True)
    df_geofon['area_name'] = df_geofon['region']
    x = df_usgs['longitude'].values  
    y = df_usgs['latitude'].values   
    mag_usgs = df_usgs['mag'].values
    mag_geofon = df_geofon['mag'].values
    places = df_usgs['area_name'].values
    n = len(x)
    distance_matrix = pd.DataFrame(np.zeros((n, n)), index = places, columns = places)
    for i in range(n):
        for j in range(n):
            distance_matrix.iloc[i,j] = np.sqrt((x[i] - x[j])**2+(y[i] - y[j])**2)
    print(distance_matrix)

    #2
    print("descriptiv_estatistics_for_mag_from_usgs")
    print(f"mean: {np.mean(mag_usgs):.2f}")
    print(f"sd: {np.std(mag_usgs):.2f}")
    print(f"median: {np.median(mag_usgs):.2f}")
    print(f"min: {np.min(mag_usgs):.2f}")
    print(f"max: {np.max(mag_usgs):.2f}")
    print(f"percentile: {np.percentile(mag_usgs, [25, 50, 75])}")
    print("descriptiv_estatistics_for_mag_from_geofon")
    print(f"mean: {np.mean(mag_geofon):.2f}")
    print(f"sd: {np.std(mag_geofon):.2f}")
    print(f"median: {np.median(mag_geofon):.2f}")
    print(f"min: {np.min(mag_geofon):.2f}")
    print(f"max: {np.max(mag_geofon):.2f}")
    print(f"percentile: {np.percentile(mag_geofon, [25, 50, 75])}")

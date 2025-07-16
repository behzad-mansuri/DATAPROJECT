from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta 
import re
import csv 
 
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

url2 = f"https://geofon.gfz.de/eqinfo/list.php?datemin={start_date}&datemax={end_date}&latmax=46&lonmin=123&lonmax=146&latmin=24&magmin=4&fmt=html&nmax=1000"
response2 = requests.get(url2)



soup = BeautifulSoup(response2.content , "html.parser")

data_containers = soup.find_all("div" , class_= lambda items : items is not None and "flex-row row eqinfo-all" in items)


Mag=[]
Region=[]
Depth = []
Time = []

for data in data_containers:
    mag = data.find("span" , class_ = "magbox")
    pattern = r'\b\d+\.\d+\b'
    selected = re.search(pattern , mag.text)
    Mag.append(selected.group())

    region = data.find("strong")
    Region.append(region.text)


    depth = data.find("span" , class_ = "pull-right")
    selected2 = re.search("[0-9][0-9]", depth.text)
    Depth.append(selected2.group() if selected2 else None)

    time = data.find_all("div" , class_ = "col-xs-12")
    texts = (text for text in time[1].find_all(string=True, recursive=False))
    result_text = ''.join(texts)
    Time.append(result_text.strip())



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


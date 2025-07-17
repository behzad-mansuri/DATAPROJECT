import pandas as pd
import matplotlib.pyplot as plt

url1 = "https://raw.githubusercontent.com/behzad-mansuri/DATAPROJECT/refs/heads/main/JAPAN_GEOFON.csv"
df1 = pd.read_csv(url1)

#----DASTE BANDI E SHAHRHA----

df1['city'] = df1['region']
n = 5
top_cities = df1['city'].value_counts().head(n).index.tolist()
df1['city_grouped'] = df1['city'].apply(lambda x: x if x in top_cities else 'Others')
cities = df1['city_grouped'].unique()

#----HISTIGRAM----

plt.figure(figsize=(10, 6))

for city in cities:
    subset = df1[df1['city_grouped'] == city]
    plt.hist(
        subset['mag'], bins=20, alpha=0.5,
        label=city, edgecolor='black'
    )

plt.title('Earthquake Magnitude Histogram by City')
plt.xlabel('Magnitude')
plt.ylabel('Count')
plt.grid(True, alpha=0.3)
plt.legend(title='City')
plt.tight_layout()
plt.savefig('histogram_magnitude_by_city_overlay.png')
plt.show()
# ===============================
#  IMPORT LIBRARIES
# ===============================
import pandas as pd
import matplotlib.pyplot as plt
# ===============================
#  READ DATAS
# ===============================
#GEOFON
url = "https://raw.githubusercontent.com/behzad-mansuri/DATAPROJECT/refs/heads/main/JAPAN_USGS.csv"
df = pd.read_csv(url)
#USGS
url1 = "https://raw.githubusercontent.com/behzad-mansuri/DATAPROJECT/refs/heads/main/JAPAN_GEOFON.csv"
df1 = pd.read_csv(url1)
# ===============================
#TIME TO DATE AND TIME AND MONTH
# ===============================
df['time'] = pd.to_datetime(df['time'])
df['month'] = df['time'].dt.to_period('M')
# ===============================
#  HISTOGRAM
# ===============================
# GROUP OF CITIES
df1['city'] = df1['region']
n = 5
top_cities = df1['city'].value_counts().head(n).index.tolist()
df1['city_grouped'] = df1['city'].apply(lambda x: x if x in top_cities else 'Others')
cities = df1['city_grouped'].unique()

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
# ===============================
#  LINE-CHART
# ===============================
monthly_counts = df.groupby('month').size()
plt.figure(figsize=(10,6))
monthly_counts.plot(marker='o', color='darkblue')
plt.title('Monthly Earthquake Count')
plt.xlabel('Month')
plt.ylabel('Number of Earthquakes')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('line_monthly_counts.png')
plt.show()
# ===============================
#  SCATTER
# ===============================
plt.figure(figsize=(10,6))
plt.scatter(df['depth'], df['mag'], alpha=0.5, color='mediumseagreen', edgecolors='black')
plt.title('Magnitude vs. Depth')
plt.xlabel('Depth (km)')
plt.ylabel('Magnitude')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('scatter_mag_vs_depth.png')
plt.show()
# ===============================
#  BOX-PLOT
# ===============================
plt.figure(figsize=(10,6))
plt.boxplot(df['depth'], patch_artist=True, boxprops=dict(facecolor='steelblue', alpha=0.3))
plt.title('Boxplot of Earthquake Depths')
plt.ylabel('Depth (km)')
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('boxplot_depth.png')
plt.show()
# ===============================
#  UNIT TEST
# ===============================
print("\n🔍 Simple Data Checks")

# CHECK EMPTY
if df.empty:
    raise ValueError("❌ Dataset khali ast!")

# CHECK COLUMNS
required_cols = ['mag', 'time']
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"❌ Sotune zaroori mojood nist: {col}")

# CHECK VALUE
if df['mag'].isnull().any():
    raise ValueError("❌ Sotune 'mag' meghdare null darad!")

# CHECK TYPE
if not pd.api.types.is_numeric_dtype(df['mag']):
    raise TypeError("❌ 'mag' bayad numeric bashad!")

if not pd.api.types.is_datetime64_any_dtype(df['time']):
    raise TypeError("❌ 'time' bayad datetime bashad!")

# CHECK MEAN
mean_mag = df['mag'].mean()
if not (3 <= mean_mag <= 7):
    raise ValueError(f"❌ Magnitude motavaset gheire mamool: {mean_mag:.2f}")

print("✅ Hameye check-ha ba movafaghiat anjam shod!")


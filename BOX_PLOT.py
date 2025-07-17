import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/behzad-mansuri/DATAPROJECT/refs/heads/main/JAPAN_USGS.csv"
df = pd.read_csv(url)


df['time'] = pd.to_datetime(df['time'])

plt.figure(figsize=(10,6))
plt.boxplot(df['depth'], patch_artist=True, boxprops=dict(facecolor='steelblue', alpha=0.3))
plt.title('Boxplot of Earthquake Depths')
plt.ylabel('Depth (km)')
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('boxplot_depth.png')
plt.show()


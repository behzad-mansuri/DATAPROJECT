import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/behzad-mansuri/DATAPROJECT/refs/heads/main/JAPAN_USGS.csv"
df = pd.read_csv(url)

plt.figure(figsize=(10,6))
plt.scatter(df['depth'], df['mag'], alpha=0.5, color='mediumseagreen', edgecolors='black')
plt.title('Magnitude vs. Depth')
plt.xlabel('Depth (km)')
plt.ylabel('Magnitude')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('scatter_mag_vs_depth.png')
plt.show()
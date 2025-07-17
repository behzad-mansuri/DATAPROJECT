import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/behzad-mansuri/DATAPROJECT/refs/heads/main/JAPAN_USGS.csv"
df = pd.read_csv(url)

df['time'] = pd.to_datetime(df['time'])
df['month'] = df['time'].dt.to_period('M')

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
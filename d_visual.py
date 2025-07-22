import pandas as pd
import matplotlib.pyplot as plt

# ===============================
#  READ DATA 
# ===============================
df_usgs = pd.read_csv('JAPAN_USGS.csv')
df_geofon = pd.read_csv('JAPAN_GEOFON.csv')

class Visualz:
    def __init__(self, df_usgs, df_geofon):
        self.df = df_usgs.copy()
        self.dfG = df_geofon.copy()

        self.df['time'] = pd.to_datetime(self.df['time'], errors='coerce')
        self.df['month'] = self.df['time'].dt.to_period('M')

    # ===============================
    #  HISTOGRAM
    # ===============================
    def g_city(self):
        self.dfG['city'] = self.dfG['region']
        top_cities = self.dfG['city'].value_counts().head(5).index.tolist()

        grouped = []
        for city in self.dfG['city']:
            if city in top_cities:
                grouped.append(city)
            else:
                grouped.append('Others')

        self.dfG['city_grouped'] = grouped
        return self.dfG['city_grouped'].unique()

    def hist(self):
        plt.figure(figsize=(10, 6))
        for city in self.g_city():
            subset = self.dfG[self.dfG['city_grouped'] == city]
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
        plt.savefig('histogram_magnitude_by_city.png')
        plt.show()

    # ===============================
    #  LINE-CHART
    # ===============================
    def line(self):
        monthly_counts = self.df.groupby('month').size()
        plt.figure(figsize=(10, 6))
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
    def scatter(self):
        plt.figure(figsize=(10, 6))
        plt.scatter(
            self.df['depth'], self.df['mag'],
            alpha=0.5, color='mediumseagreen', edgecolors='black'
        )
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
    def box(self):
        plt.figure(figsize=(10, 6))
        plt.boxplot(
            self.df['depth'].dropna(),
            patch_artist=True,
            boxprops=dict(facecolor='steelblue', alpha=0.3)
        )
        plt.title('Boxplot of Earthquake Depths')
        plt.ylabel('Depth (km)')
        plt.grid(True, axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('boxplot_depth.png')
        plt.show()

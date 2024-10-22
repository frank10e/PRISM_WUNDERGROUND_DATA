import pandas as pd
import utm

file_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\UTM Coordinates of Rain Gauge Stations.xlsx"
df = pd.read_excel(file_path)

def utm_to_latlon(x, y):
    lat, lon = utm.to_latlon(x, y, 12, 'N')  
    return lat, lon


df[['Latitude', 'Longitude']] = df.apply(lambda row: pd.Series(utm_to_latlon(row['X-COORD'], row['Y-COORD'])), axis=1)

output_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\Rain_Gauge_Stations_with_Lat_Lon.xlsx"
df.to_excel(output_path, index=False)

print(f"Data file {output_path}")

import pandas as pd
import os

# Read PRISM data
prism_data = pd.read_csv(r'C:\Users\User\OneDrive\桌面\Wunderground Data\ppt_data_inches.csv')

# List of station names
stations_list = [
    "KAZGREEN141", "KAZGREEN175", "KAZGREEN232", "KAZGREEN241", 
    "KAZGREEN153", "KAZSAHUA112", "KAZVAIL270", "KAZSAHUA24", 
    "KAZVAIL276", "KAZVAIL76", "KAZGREEN15"
]

# Reshape PRISM data from wide format to long format
prism_long = pd.melt(prism_data, 
                     id_vars=["Name", "Elevation_ft", "Latitude", "Longitude"], 
                     var_name="date", 
                     value_name="ppt_prism")

# Convert 'date' in PRISM data to date format
prism_long['date'] = pd.to_datetime(prism_long['date'], format='%Y%m%d')

# Path for Wunderground data files
wunderground_path = r'C:\Users\User\OneDrive\桌面\Wunderground Data'

# To store the combined data from all stations
combined_data = pd.DataFrame()

# Merge PRISM and Wunderground data for each station
for station in stations_list:
    try:
        # Load Wunderground data for the current station
        wunderground_file = os.path.join(wunderground_path, f"{station}.csv")
        wunderground_data = pd.read_csv(wunderground_file)
        wunderground_data['date'] = pd.to_datetime(wunderground_data['date'])
        
        # Filter PRISM data for the current station
        prism_station_data = prism_long[prism_long['Name'] == station]
        
        # Merge PRISM and Wunderground data by 'date'
        comparison_data = pd.merge(prism_station_data, wunderground_data[['date', 'precipTotal']], on='date', how='inner')
        
        # Append to the combined dataset
        combined_data = pd.concat([combined_data, comparison_data], ignore_index=True)
    
    except FileNotFoundError:
        print(f"Wunderground data file for {station} not found.")
    except Exception as e:
        print(f"An error occurred for station {station}: {e}")

# Save the combined dataset to CSV
file_path = r'C:\Users\User\OneDrive\桌面\Wunderground Data\combined_prism_wunderground_data_2.csv'
combined_data.to_csv(file_path, index=False)

print(f"Combined data saved to: {file_path}")

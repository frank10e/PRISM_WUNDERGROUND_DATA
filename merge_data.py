import pandas as pd
import os
import matplotlib.pyplot as plt

# Load the PRISM data
prism_data = pd.read_csv(r'C:\Users\User\OneDrive\桌面\Wunderground Data\ppt_data_inches.csv')

# List of station names
stations_to_select = [
    "KAZGREEN141", "KAZGREEN175", "KAZGREEN232", "KAZGREEN241", 
    "KAZGREEN153", "KAZSAHUA112", "KAZVAIL270", "KAZSAHUA24", 
    "KAZVAIL276", "KAZVAIL76", "KAZGREEN15"
]

# Reshape PRISM data (wide to long format)
prism_long = pd.melt(prism_data, 
                     id_vars=["Name", "Elevation_ft", "Latitude", "Longitude"], 
                     var_name="date", 
                     value_name="ppt_prism")

# Format PRISM 'date' column to datetime format
prism_long['date'] = pd.to_datetime(prism_long['date'], format='%Y%m%d')

# Base path for Wunderground data files
wunderground_path = r'C:\Users\User\OneDrive\桌面\Wunderground Data'
average_differences = {}
# Loop over each station
for station in stations_to_select:
    try:
        # Load Wunderground data for the current station
        wunderground_file = os.path.join(wunderground_path, f"{station}.csv")
        wunderground_data = pd.read_csv(wunderground_file)
        wunderground_data['date'] = pd.to_datetime(wunderground_data['date'])
        
        # Filter PRISM data for the current station
        prism_station_data = prism_long[prism_long['Name'] == station]
        
        # Merge PRISM and Wunderground data on 'date'
        comparison_data = pd.merge(prism_station_data, wunderground_data[['date', 'precipTotal']], on='date', how='inner')

        comparison_data['difference'] = abs(comparison_data['ppt_prism'] - comparison_data['precipTotal'])
        
        # Compute the average difference
        avg_difference = comparison_data['difference'].mean()
        
        # Store the result in the dictionary
        average_differences[station] = avg_difference
        
        print(f"Average difference for {station}: {avg_difference:.4f} inches")
        
        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(comparison_data['date'], comparison_data['ppt_prism'], label='PRISM ppt_prism (in)', color='blue', marker='o')
        plt.plot(comparison_data['date'], comparison_data['precipTotal'], label='Wunderground precipTotal (in)', color='orange', marker='x')
        
        # Customize the plot
        plt.title(f'Precipitation Comparison: PRISM vs Wunderground ({station})')
        plt.xlabel('Date')
        plt.ylabel('Precipitation (inches)')
        plt.legend()
        plt.grid(True)
        
        # Save the plot
        plot_file_path = os.path.join(wunderground_path, f"comparison_{station}.png")
        plt.savefig(plot_file_path)
        
        # Show the plot
        plt.show()
        print(f"Comparison plot for {station} saved successfully.")
    
    except FileNotFoundError:
        print(f"Wunderground data file for {station} not found.")
    except Exception as e:
        print(f"An error occurred for station {station}: {e}")



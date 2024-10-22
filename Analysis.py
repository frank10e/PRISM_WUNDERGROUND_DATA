import pandas as pd
import os
from scipy import stats

# Path for Wunderground data files
wunderground_path = r'C:\Users\User\OneDrive\桌面\Wunderground Data'

# Load PRISM data
prism_data = pd.read_csv(r'C:\Users\User\OneDrive\桌面\Wunderground Data\ppt_data_inches.csv')

# Station list
stations_list = [ "KAZGREEN205", "KAZGREEN153", "KAZGREEN159", "KAZGREEN285", "KAZGREEN122",
    "KAZSAHUA98", "KAZGREEN85", "KAZGREEN131", "KAZGREEN218", "KAZGREEN293",
    "KAZGREEN232", "KAZGREEN95", "KAZGREEN251", "KAZSAHUA100", "KAZSAHUA109",
    "KAZSAHUA60", "KAZSAHUA117", "KAZGREEN99", "KAZSAHUA74", "KAZSAHUA102",
    "KAZSAHUA105", "KAZGREEN181", "KAZGREEN241", "KAZGREEN281", "KAZGREEN299",
    "KAZGREEN140", "KAZGREEN174", "KAZGREEN233", "KAZGREEN129", "KAZGREEN177",
    "KAZGREEN168", "KAZGREEN46", "KAZGREEN180", "KAZGREEN269", "KAZGREEN71",
    "KAZGREEN227", "KAZGREEN48", "KAZGREEN166", "KAZGREEN25", "KAZGREEN204",
    "KAZGREEN265", "KAZGREEN297", "KAZGREEN141", "KAZGREEN175", "KAZGREEN53",
    "KAZGREEN244", "KAZGREEN266", "KAZGREEN143", "KAZGREEN221", "KAZGREEN229",
    "KAZGREEN151", "KAZGREEN261", "KAZGREEN258", "KAZGREEN82", "KAZGREEN201",
    "KAZGREEN88", "KAZGREEN253", "KAZGREEN290", "KAZGREEN176", "KAZGREEN61",
    "KAZGREEN15", "KAZSONOI59", "KAZVAIL289", "KAZVAIL185", "KAZVAIL66",
    "KAZVAIL205", "KAZVAIL258", "KAZVAIL273", "KAZVAIL112", "KAZVAIL252",
    "KAZVAIL210", "KAZVAIL259", "KAZVAIL196", "KAZVAIL173", "KAZVAIL185",
    "KAZCORON6", "KAZVAIL134", "KAZVAIL65", "KAZVAIL288", "KAZVAIL214",
    "KAZVAIL71", "KAZCORON16", "KAZCORON7", "KAZVAIL226", "KAZVAIL76",
    "KAZCORON22", "KAZVAIL203", "KAZVAIL270", "KAZVAIL276", "KAZSAHUA112",
    "KAZSAHUA88", "KAZSAHUA24", "KAZSAHUA103", "KAZSAHUA32", "KAZSAHUA55",
    "KAZSAHUA42", "KAZSAHUA101", "KAZSAHUA43", "KAZSAHUA45", "KAZSAHUA108",
    "KAZSAHUA99", "KAZSAHUA80", "KAZSONOI59", "KAZGREEN294", "KAZAMADO2",
    "KAZAMADO15"]

# Convert PRISM data from wide to long format
prism_long = pd.melt(prism_data, 
                     id_vars=["Name", "Elevation_ft", "Latitude", "Longitude"], 
                     var_name="date", 
                     value_name="ppt_prism")

# Convert PRISM 'date' to datetime format
prism_long['date'] = pd.to_datetime(prism_long['date'], format='%Y%m%d')

significant_counts = 0
non_significant_counts = 0

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
        
        # Remove rows with missing values
        comparison_data.dropna(subset=['ppt_prism', 'precipTotal'], inplace=True)
        
        # Perform t-test if there are enough data points
        if not comparison_data.empty:
            t_stat, p_value = stats.ttest_ind(comparison_data['ppt_prism'], comparison_data['precipTotal'], nan_policy='omit')
            print(f"Station: {station}")
            print(f"T-statistic: {t_stat:.4f}, P-value: {p_value:.4f}")
            
            if p_value < 0.05:
                print(f"Result: Statistically significant difference (p < 0.05) between PRISM and Wunderground data for {station}.")
                significant_counts += 1
            else:
                print(f"Result: No statistically significant difference (p >= 0.05) between PRISM and Wunderground data for {station}.")
                non_significant_counts += 1
            print("-" * 50)
    
    except FileNotFoundError:
        print(f"Wunderground data file for {station} not found.")
    except Exception as e:
        print(f"An error occurred for station {station}: {e}")

# Summary of significant and non-significant results
print(f"\nSummary of T-tests:")
print(f"Number of stations with statistically significant differences: {significant_counts}")
print(f"Number of stations with no statistically significant differences: {non_significant_counts}")
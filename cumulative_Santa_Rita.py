import pandas as pd
import numpy as np

# File path
file_path = r'C:\Users\User\OneDrive\桌面\Wunderground Data\corrected_prism_data_linear_regression.csv'

# Load the data
data = pd.read_csv(file_path)

# Convert columns representing dates into datetime format for easier manipulation
data_long = pd.melt(data, id_vars=['Name', 'Latitude', 'Longitude'], 
                    var_name='Date', value_name='Precip')
data_long['Date'] = pd.to_datetime(data_long['Date'], format='%Y%m%d')

# Filter data to only include dates from March 1, 2024, onwards
march_start = pd.to_datetime('2024-03-01')
data_filtered = data_long[data_long['Date'] >= march_start]

# Define the end dates for cumulative sums (April 1, May 1, etc.)
end_dates = ['2024-04-01', '2024-05-01', '2024-06-01', '2024-07-01', '2024-08-01', '2024-09-01']
end_dates = [pd.to_datetime(date) for date in end_dates]

# Function to categorize precipitation
def categorize_precip(precip):
    if precip == 0:
        return "Extremely Dry"
    elif precip < 1.0:
        return "Dry"
    elif precip < 2.5:
        return "Wet"
    else:
        return "Very Wet"

# Initialize an empty list to hold the results
cumulative_data = []

# Calculate cumulative precipitation for each station and each end date
for station in data_filtered['Name'].unique():
    station_data = data_filtered[data_filtered['Name'] == station]
    for end_date in end_dates:
        cumulative_precip = station_data[(station_data['Date'] >= march_start) & 
                                         (station_data['Date'] < end_date)]['Precip'].sum()
        precip_category = categorize_precip(cumulative_precip)
        cumulative_data.append({
            'Station': station,
            'End Date': end_date.strftime('%m/%d/%Y'),
            'Cumulative Precip': cumulative_precip,
            'Category': precip_category
        })

# Convert results to a DataFrame
cumulative_df = pd.DataFrame(cumulative_data)

# Save the DataFrame to an Excel file
output_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\cumulative_precipitation_data_2.xlsx"
cumulative_df.to_excel(output_path, index=False)

# Print confirmation message
print(f"Data file {output_path}")

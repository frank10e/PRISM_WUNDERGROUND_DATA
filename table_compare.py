import pandas as pd


file_path = 'C:/Users/User/OneDrive/桌面/Wunderground Data/corrected_prism_data_linear_regression.csv'
data = pd.read_csv(file_path)
data['date'] = pd.to_datetime(data['date'])

# Define cumulative ranges and calculate the sum for each range
ranges = [
    ('2024-04-01', '2024-05-01'),
    ('2024-04-01', '2024-06-01'),
    ('2024-04-01', '2024-07-01'),
    ('2024-04-01', '2024-08-01'),
    ('2024-04-01', '2024-09-01')
]

# Gather all stations and corresponding details
stations = data.groupby(['Name', 'Elevation_ft', 'Latitude', 'Longitude']).size().reset_index()
for start_date, end_date in ranges:
    stations[f'Sum_{start_date}_to_{end_date}'] = 0
for start_date, end_date in ranges:
    range_sum = data[(data['date'] >= start_date) & (data['date'] < end_date)] \
                  .groupby(['Name', 'Elevation_ft', 'Latitude', 'Longitude'])['Corrected_PRISM'].sum().reset_index()
    stations = pd.merge(stations, range_sum, how='left', on=['Name', 'Elevation_ft', 'Latitude', 'Longitude'])
    stations[f'Sum_{start_date}_to_{end_date}'] = stations['Corrected_PRISM'].fillna(0)
    stations.drop(columns=['Corrected_PRISM'], inplace=True)
stations.to_csv('C:/Users/User/OneDrive/桌面/Wunderground Data/cumulative_station_linear_regression.csv', index=False)
print(stations.head())

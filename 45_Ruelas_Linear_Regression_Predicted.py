import pandas as pd

# Load the data from the provided CSV file
file_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\ppt_data_inches_Santa_Rita.csv"
data = pd.read_csv(file_path)

# Extract the data for "Ruelas" and "45"
ruelas_45_data = data[data['Name'].isin(['Ruelas', '45'])]

# Melt the data to convert the date columns into a single column
date_columns = ruelas_45_data.columns[3:]
data_long = pd.melt(ruelas_45_data, id_vars=['Name', 'Latitude', 'Longitude'],
                    value_vars=date_columns, var_name='Date', value_name='ppt_prism')

# Convert 'Date' to datetime format
data_long['Date'] = pd.to_datetime(data_long['Date'], format='%Y%m%d')

# Apply the regression model: y = 0.0619 + 0.5380 * x
data_long['Corrected_PRISM'] = 0.0619 + 0.5380 * data_long['ppt_prism']

# Save the modified data to a new CSV file
output_file_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\ruelas_45_predicted_rainfall.csv"
data_long.to_csv(output_file_path, index=False)

print(f"Data successfully saved to {output_file_path}")

import pandas as pd


file_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\ppt_data_inches_Santa_Rita.csv"
data_clean = pd.read_csv(file_path)
date_columns = data_clean.columns[3:]  
data_long = pd.melt(data_clean, id_vars=['Name', 'Latitude', 'Longitude'], 
                    value_vars=date_columns, var_name='Date', value_name='ppt_prism')
data_long['Date'] = pd.to_datetime(data_long['Date'], format='%Y%m%d')
data_long['Corrected_PRISM'] = 0.0479 + 0.5096 * data_long['ppt_prism']
output_file_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\modified_santa_rita_data.csv"
data_long.to_csv(output_file_path, index=False)

print(f"Data successfully saved to {output_file_path}")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the two datasets
csv_data_path = r"C:\Users\User\Downloads\santa_rita_observation_data.csv"
excel_data_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\Cumulative_Santa_Rita_V2.xlsx"

df_csv = pd.read_csv(csv_data_path)
df_excel = pd.read_excel(excel_data_path)

# Merge the datasets using 'Station' and 'End Date' from the Excel file and 'Date' from the CSV
df_merged = pd.merge(df_csv, df_excel, left_on=['Station', 'Date'], right_on=['Station', 'End Date'], how='inner')

output_csv_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\merged_santa_rita_data_obvserved_predicted.csv"
df_merged.to_csv(output_csv_path, index=False)

# Function to plot trendlines for "Observation", "Estimated", and "Cumulative Precip" in one plot
def plot_trendlines_comparison(df, station_name):
    x = np.arange(len(df['Date']))
    
    # Extract numerical values from 'Observation', 'Estimated', and 'Cumulative Precip' columns
    y_observation = df['Observation'].apply(lambda val: float(val.split()[0])).values
    y_estimated = df['Estimated'].apply(lambda val: float(val.split()[0])).values
    y_cumulative = df['Cumulative Precip'].values  # Cumulative Precip is already numeric

    # Create the scatter plots
    plt.scatter(x, y_observation, label='Observation', color='blue', alpha=0.6)
    plt.scatter(x, y_estimated, label='Estimated', color='orange', alpha=0.6)
    plt.scatter(x, y_cumulative, label='Cumulative Precip', color='green', alpha=0.6)

    # Fit trendlines
    z_obs = np.polyfit(x, y_observation, 1)
    p_obs = np.poly1d(z_obs)

    z_est = np.polyfit(x, y_estimated, 1)
    p_est = np.poly1d(z_est)

    z_cum = np.polyfit(x, y_cumulative, 1)
    p_cum = np.poly1d(z_cum)

    # Plot the trendlines
    plt.plot(x, p_obs(x), label='Observation Trendline', color='blue', linestyle='--')
    plt.plot(x, p_est(x), label='Estimated Trendline', color='orange', linestyle='--')
    plt.plot(x, p_cum(x), label='Cumulative Precip Trendline', color='green', linestyle='--')

    # Add labels, title, and legend
    plt.title(f'Observation, Estimated, and Cumulative Precip Comparison for {station_name}')
    plt.xlabel('Time (Index)')
    plt.ylabel('Precipitation (inches)')
    plt.legend()
    plt.grid(True)

    # Save the plot as an image file (PNG)
    plt.savefig(f"C:/Users/User/Downloads/{station_name}_trend_comparison_with_cumulative.png", dpi=300)
    plt.close()  # Close the plot to avoid displaying it

# Loop over each station and plot the comparison of "Observation", "Estimated", and "Cumulative Precip" trendlines
stations = df_merged['Station'].unique()
for station in stations:
    station_data = df_merged[df_merged['Station'] == station]
    plot_trendlines_comparison(station_data, station)

print("Plots saved successfully.")
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

# Load the combined dataset
combined_data = pd.read_csv(r'C:\Users\User\OneDrive\桌面\Wunderground Data\combined_prism_wunderground_data_2.csv')

# Drop any rows with missing ppt_prism or precipTotal values
combined_data.dropna(subset=['ppt_prism', 'precipTotal'], inplace=True)

# 强制条件：当 precipTotal 为 0 时，将 ppt_prism 也设为 0
combined_data.loc[combined_data['precipTotal'] == 0, 'ppt_prism'] = 0

# Define X as PRISM data and y as Wunderground data
X = combined_data[['ppt_prism']].values  # PRISM precipitation (X variable)
y = combined_data['precipTotal'].values  # Wunderground precipitation (Y variable)

# Create and fit the linear regression model
model = LinearRegression()
model.fit(X, y)

# Get the intercept and slope of the regression
intercept = model.intercept_
slope = model.coef_[0]

print(f"Intercept: {intercept:.4f}")
print(f"Slope: {slope:.4f}")

# Use the regression model to predict corrected PRISM data
corrected_prism = model.predict(X)

# Add the corrected PRISM data to the dataset
combined_data['corrected_prism'] = corrected_prism

# Save the corrected dataset
combined_data.to_csv(r'C:\Users\User\OneDrive\桌面\Wunderground Data\corrected_prism_wunderground_data_with_condition.csv', index=False)

# Print the first few rows to verify
print(combined_data[['ppt_prism', 'precipTotal', 'corrected_prism']].head())

# Plot corrected PRISM data vs. Wunderground data with hollow markers
plt.figure(figsize=(10, 6))

# Hollow markers for Wunderground data (blue circles)
plt.scatter(combined_data['ppt_prism'], combined_data['precipTotal'], edgecolor='blue', facecolor='none', label='Wunderground Data')

# Hollow markers for corrected PRISM data (red circles)
plt.scatter(combined_data['ppt_prism'], combined_data['corrected_prism'], edgecolor='red', facecolor='none', label='Corrected PRISM Data')

# Add trend line (regression line) for Wunderground data
x_range = np.linspace(combined_data['ppt_prism'].min(), combined_data['ppt_prism'].max(), 100)
trend_line_wunderground = intercept + slope * x_range
plt.plot(x_range, trend_line_wunderground, color='blue', linestyle='-', label='Trend Line (Wunderground Data)')

# Add trend line for Corrected PRISM data (it is the same as Wunderground, so it will overlap)
plt.plot(x_range, trend_line_wunderground, color='red', linestyle='-', label='Trend Line (Corrected PRISM Data)')

# Add regression equation text on the plot
equation_text = f"y = {intercept:.4f} + {slope:.4f} * x"
plt.text(0.05, 0.9, equation_text, transform=plt.gca().transAxes, fontsize=12, color='black')

# Add labels, title, and legend
plt.xlabel('PRISM Precipitation (ppt_prism)')
plt.ylabel('Precipitation (inches)')
plt.legend()
plt.title('Corrected PRISM Data vs Wunderground Data with Trend Lines')

# Display the plot
plt.show()

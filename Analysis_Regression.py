import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the dataset from the provided file path
file_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\combined_prism_wunderground_data.csv"
data = pd.read_csv(file_path)

# Drop rows where either 'ppt_prism' or 'precipTotal' contains NaN
data_clean = data.dropna(subset=['ppt_prism', 'precipTotal'])

# Separate features (ppt_prism) and target (precipTotal)
X = data_clean[['ppt_prism']]  # PRISM precipitation data (independent variable)
y = data_clean['precipTotal']  # Wunderground precipitation data (dependent variable)

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
rf_model.fit(X_train, y_train)

# Predict corrected precipitation values for the entire dataset
data_clean['Corrected_PRISM'] = rf_model.predict(X)

# Clip any negative predictions to 0 (since precipitation cannot be negative)
data_clean['Corrected_PRISM'] = np.clip(data_clean['Corrected_PRISM'], 0, None)

# Save the corrected data into a new CSV file
output_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\corrected_prism_data_rf.csv"
data_clean.to_csv(output_path, index=False)

# Evaluate the model on the test set
y_pred = rf_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Print the feature importance
print("Feature Importances (if applicable):")
print(rf_model.feature_importances_)

# Print confirmation
print(f"Corrected data saved to {output_path}")

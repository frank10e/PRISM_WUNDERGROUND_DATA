import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

# Step 1: Load the dataset
file_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\combined_prism_wunderground_data.csv"
data = pd.read_csv(file_path)

# Step 2: Drop rows with NaN values in 'ppt_prism' or 'precipTotal'
data_clean = data.dropna(subset=['ppt_prism', 'precipTotal'])

# Step 3: Separate features (ppt_prism) and target (precipTotal)
X = data_clean[['ppt_prism']].values  # PRISM precipitation data
y = data_clean['precipTotal'].values  # Wunderground precipitation data

# Step 4: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Standardize the data (this helps with neural network training)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Step 6: Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

# Step 7: Define a simple feedforward neural network model in PyTorch
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# Model parameters
input_size = 1  # We have one feature: ppt_prism
hidden_size = 64  # You can tune the number of hidden units
output_size = 1  # We want to predict a single output: precipTotal

# Instantiate the model
model = SimpleNN(input_size, hidden_size, output_size)

# Step 8: Define the loss function and optimizer
criterion = nn.MSELoss()  # Mean Squared Error loss
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam optimizer

# Step 9: Train the neural network
num_epochs = 500  # You can adjust the number of epochs
for epoch in range(num_epochs):
    # Forward pass
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)
    
    # Backward pass and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if (epoch+1) % 50 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Step 10: Evaluate the model on the test set
model.eval()  # Set the model to evaluation mode
with torch.no_grad():  # Disable gradient computation for inference
    predictions = model(X_test_tensor)
    test_loss = criterion(predictions, y_test_tensor)
    print(f'Test Loss: {test_loss.item():.4f}')

# Step 11: Apply the model to the new data (Santa Rita dataset)
file_path_new = r"C:\Users\User\OneDrive\桌面\Wunderground Data\ppt_data_inches_Santa_Rita.csv"
data_new = pd.read_csv(file_path_new)

# Reshape and standardize the new dataset
data_new_long = pd.melt(data_new, id_vars=['Name', 'Latitude', 'Longitude'], 
                        var_name='Date', value_name='ppt_prism')
data_new_long['ppt_prism_scaled'] = scaler.transform(data_new_long[['ppt_prism']])

# Convert to tensor for model prediction
X_new_tensor = torch.tensor(data_new_long['ppt_prism_scaled'].values, dtype=torch.float32).view(-1, 1)

# Predict using the trained model
model.eval()
with torch.no_grad():
    data_new_long['Corrected_Precip'] = model(X_new_tensor).numpy()

# Clip any negative values to 0
data_new_long['Corrected_Precip'] = np.clip(data_new_long['Corrected_Precip'], 0, None)

# Save the corrected data
output_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\Transformed_PRISM_Data_NN.xlsx"
data_new_long.to_excel(output_path, index=False)

print(f"Transformed data saved to {output_path}")

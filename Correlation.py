import pandas as pd

# Load the dataset for training the model
train_file_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\combined_prism_wunderground_data.csv"
data_train = pd.read_csv(train_file_path)

# Check correlation between ppt_prism and precipTotal
correlation = data_train[['ppt_prism', 'precipTotal']].corr()
print(correlation)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# 加载数据集
file_path = r"C:/Users/User/OneDrive/桌面/Wunderground Data/ppt_data_inches_Santa_Rita.csv"
data = pd.read_csv(file_path)

# 删除 'ppt_prism' 或 'precipTotal' 为空的行
data_clean = data.dropna(subset=['ppt_prism', 'precipTotal'])

# 分离特征 (ppt_prism) 和 目标变量 (precipTotal)
X = data_clean[['ppt_prism']]  # PRISM 的降水数据（自变量）
y = data_clean['precipTotal']  # Wunderground 的降水数据（因变量）

# 使用线性回归模型公式 y = 0.0473 + 0.3732 * x 进行预测
data_clean['Corrected_PRISM'] = 0.0473 + 0.3732 * data_clean['ppt_prism']

# 将任何负的预测值截取为 0（因为降水量不能为负）
data_clean['Corrected_PRISM'] = np.clip(data_clean['Corrected_PRISM'], 0, None)

# 将修正后的数据保存到一个新的 CSV 文件中
output_path = r"C:\Users\User\OneDrive\桌面\Wunderground Data\corrected_prism_data_linear_regression.csv"
data_clean.to_csv(output_path, index=False)

# 分割数据集为训练集和测试集 (80% 训练, 20% 测试)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 计算在测试集上的均方误差（直接基于线性回归公式）
y_pred_test = 0.0473 + 0.3732 * X_test
mse = mean_squared_error(y_test, y_pred_test)
print(f"Mean Squared Error using Linear Regression: {mse}")

# 打印确认信息
print(f"Corrected data saved to {output_path}")

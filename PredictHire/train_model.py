import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

UN_COL = 'UN'
VN_COL = 'VN'
EBITDA_COL = 'EBITDA'
ANO_COL = 'ANO'
TURNOVER = 'Turnover'
CRESCIMENTO_VN = 'Crescimento_VN'
CRESCIMENTO_HEADCOUNT = 'Crescimento_Headcount'
MARGEN_EBITDA = 'Margem_EBITDA'
TARGET_COL = 'HEADCOUNT'

file_path = 'previsao_necessidades_contratacao_atualizado.csv'
data = pd.read_csv(file_path)

required_cols = [UN_COL, VN_COL, EBITDA_COL, ANO_COL, TURNOVER, CRESCIMENTO_VN, CRESCIMENTO_HEADCOUNT, MARGEN_EBITDA, TARGET_COL]
missing_cols = [col for col in required_cols if col not in data.columns]
if missing_cols:
    raise ValueError(f"The following columns are missing from the dataset: {missing_cols}")

# Convert categorical data in 'UN' to numeric using Label Encoding
label_encoder = LabelEncoder()
data[UN_COL] = label_encoder.fit_transform(data[UN_COL])

# Normalize the feature columns
scaler = MinMaxScaler()
scaling_cols = [UN_COL, VN_COL, EBITDA_COL, ANO_COL, TURNOVER, CRESCIMENTO_VN, CRESCIMENTO_HEADCOUNT, MARGEN_EBITDA]
data[scaling_cols] = scaler.fit_transform(data[scaling_cols])

features = [UN_COL, VN_COL, EBITDA_COL, ANO_COL, TURNOVER, CRESCIMENTO_VN, CRESCIMENTO_HEADCOUNT, MARGEN_EBITDA]
X = data[features]
y = data[TARGET_COL]

# Split the data into training (60%), validation (20%), and testing (20%) sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

y_val_pred = model.predict(X_val)

# Calculate RMSE (Root Mean Squared Error)
rmse_val = np.sqrt(mean_squared_error(y_val, y_val_pred))

# Calculate MAE (Mean Absolute Error)
mae_val = mean_absolute_error(y_val, y_val_pred)

# Calculate R² (coefficient of determination)
r2_val = r2_score(y_val, y_val_pred)


# Save the trained model, scaler, and features
model_filename = 'random_forest_model.pkl'
joblib.dump((model, scaler, features), model_filename)
print(f"Model, scaler, and features saved to: {model_filename}")

print(f"Validation RMSE: {rmse_val:.2f}")
print(f"Validation MAE: {mae_val:.2f}")
print(f"Validation R²: {r2_val:.2f}")


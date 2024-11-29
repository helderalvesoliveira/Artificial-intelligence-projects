import numpy as np
import pandas as pd
import joblib
import predict_model_chart as predict_model_chart

# Column name constants
UN_COL = 'UN'
VN_COL = 'VN'
EBITDA_COL = 'EBITDA'
ANO_COL = 'ANO'
TURNOVER = 'Turnover'
CRESCIMENTO_VN = 'Crescimento_VN'
CRESCIMENTO_HEADCOUNT = 'Crescimento_Headcount'
MARGEN_EBITDA = 'Margem_EBITDA'

# Load the trained model, scaler, and feature list
model_filename = 'random_forest_model.pkl'
try:
    model, scaler, features = joblib.load(model_filename)
    print("Model, scaler, and features loaded successfully.")
except FileNotFoundError:
    print(f"Error: File '{model_filename}' not found.")
    exit()

# Example new data for prediction
new_data = pd.DataFrame({
    "ANO": [2025],
    "VN": [600000],
    "EBITDA": [80000],
    "HEADCOUNT": [7],
    "Turnover": [0.15],
    "Crescimento_VN": [((600000 / 500000) - 1) * 100],
    "Crescimento_Headcount": [0],
    "Margem_EBITDA": [(80000 / 600000) * 100]
})


# Replace 0 with a valid identifier in your business context
new_data[UN_COL] = 0

# Drop the 'HEADCOUNT' column, as it is the target in the training data
if 'HEADCOUNT' in new_data.columns:
    new_data = new_data.drop(columns=['HEADCOUNT'])

# Verify that all required feature columns are present in the new data
missing_cols = [col for col in features if col not in new_data.columns]
if missing_cols:
    print(f"Error: Missing columns in new data: {missing_cols}")
    exit()

try:
    new_data_normalized = new_data.copy()
    new_data_normalized[features] = scaler.transform(new_data[features])
except Exception as e:
    print(f"Error during data normalization: {e}")
    exit()

try:
    predictions = model.predict(new_data_normalized[features])
    print("Predictions for new data:", predictions)
except Exception as e:
    print(f"Error during prediction: {e}")
    exit()

# Current number of employees
current_headcount = 7

# Compare predicted headcount with the current headcount
predicted_headcount = predictions[0]
if predicted_headcount > current_headcount:
    additional_needed = int(np.ceil(predicted_headcount - current_headcount))
    print(f"According to the prediction, you should hire {additional_needed} additional employee(s).")
else:
    print("No need to hire additional employees at this time.")


file_path = 'previsao_necessidades_contratacao_atualizado.csv'
historical_data = pd.read_csv(file_path)

# Call the function to plot the chart
predict_model_chart.plot_historical_and_predicted_headcount(
    historical_data=historical_data, 
    predicted_year=2025, 
    predicted_headcount=predicted_headcount,
    current_headcount=current_headcount
)
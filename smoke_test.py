import joblib
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "loan_model.pkl"
SCALER_PATH = BASE_DIR / "scaler_top5.pkl"
TOP_5_FEATURES = [
    "Credit_History",
    "ApplicantIncome",
    "LoanAmount",
    "CoapplicantIncome",
    "Loan_Amount_Term",
]

print("Loading model and scaler...")
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
print("Loaded model and scaler.")

# create a sample input
sample = pd.DataFrame([{
    "Credit_History": 1.0,
    "ApplicantIncome": 2350,
    "LoanAmount": 1000,
    "CoapplicantIncome": 1508,
    "Loan_Amount_Term": 80,
}])

print("Preprocessing sample...")
scaled = scaler.transform(sample[TOP_5_FEATURES])
print("Predicting...")
pred = model.predict(scaled)
print("Prediction:", int(pred[0]))
print("Done.")

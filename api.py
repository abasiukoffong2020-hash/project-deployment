from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

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

app = FastAPI(
    title="Loan Approval Prediction API",
    description="Predict loan approval using a pretrained model and scaler.",
    version="1.0",
)

model = None
scaler = None


class LoanRequest(BaseModel):
    Credit_History: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="1.0 for yes, 0.0 for no",
    )
    ApplicantIncome: float = Field(..., ge=0.0, description="Applicant income amount")
    LoanAmount: float = Field(..., ge=0.0, description="Requested loan amount")
    CoapplicantIncome: float = Field(..., ge=0.0, description="Coapplicant income amount")
    Loan_Amount_Term: float = Field(..., ge=1.0, description="Loan term length in months")


class PredictionResponse(BaseModel):
    loan_status: str
    prediction: int
    raw_input: dict


@app.on_event("startup")
def startup_event():
    global model, scaler

    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    if not SCALER_PATH.exists():
        raise FileNotFoundError(f"Scaler file not found: {SCALER_PATH}")

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)


def preprocess_input(data: LoanRequest) -> pd.DataFrame:
    df = pd.DataFrame([data.dict()])
    return df[TOP_5_FEATURES]


@app.get("/", summary="API health check")
def root():
    return {"status": "ok", "message": "Loan Approval Prediction API is running."}


@app.post("/predict", response_model=PredictionResponse, summary="Predict loan approval")
def predict_loan(request: LoanRequest):
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model is not loaded.")

    input_df = preprocess_input(request)

    try:
        scaled_input = scaler.transform(input_df)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Error during preprocessing: {exc}")

    try:
        prediction = model.predict(scaled_input)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {exc}")

    result = int(prediction[0])
    loan_status = "Approved" if result == 1 else "Rejected"

    return PredictionResponse(
        loan_status=loan_status,
        prediction=result,
        raw_input=request.dict(),
    )

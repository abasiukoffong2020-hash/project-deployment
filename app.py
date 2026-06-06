import joblib
import pandas as pd
import streamlit as st

# Define the paths to your saved model and scaler
MODEL_PATH = 'loan_model.pkl'
SCALER_PATH = 'scaler_top5.pkl'

# Define the top 5 features used during training
top_5_features = ['Credit_History', 'ApplicantIncome', 'LoanAmount', 'CoapplicantIncome', 'Loan_Amount_Term']

def load_model_and_scaler(model_path, scaler_path):
    """Loads the pre-trained model and scaler."""
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler

def preprocess_data(data, features, scaler):
    """Preprocesses new data for prediction."""
    # Ensure the order of columns matches the training data's top 5 features
    processed_data = data[features]
    # Scale the input data using the loaded scaler
    scaled_data = scaler.transform(processed_data)
    return scaled_data

def predict_loan_status(model, preprocessed_data):
    """Makes a prediction using the loaded model."""
    prediction = model.predict(preprocessed_data)
    return prediction

# Streamlit App Interface
st.title('Loan Approval Prediction App')

# Load model and scaler only once
model, scaler = load_model_and_scaler(MODEL_PATH, SCALER_PATH)

st.header('Enter Applicant Information:')

# Input fields for the top 5 features
credit_history = st.selectbox('Credit History (1.0 for Yes, 0.0 for No)', [1.0, 0.0])
applicant_income = st.number_input('Applicant Income', min_value=0, value=2350)
loan_amount = st.number_input('Loan Amount', min_value=0.0, value=1000.0)
coapplicant_income = st.number_input('Coapplicant Income', min_value=0.0, value=1508.0)
loan_amount_term = st.number_input('Loan Amount Term (in months)', min_value=1.0, value=80.0)

# Create a DataFrame from the inputs
user_data_raw = {
    'Credit_History': [credit_history],
    'ApplicantIncome': [applicant_income],
    'LoanAmount': [loan_amount],
    'CoapplicantIncome': [coapplicant_income],
    'Loan_Amount_Term': [loan_amount_term]
}
user_df = pd.DataFrame(user_data_raw)

if st.button('Predict Loan Status'):
    # Preprocess user input
    user_scaled_data = preprocess_data(user_df, top_5_features, scaler)

    # Make prediction
    prediction = predict_loan_status(model, user_scaled_data)

    # Interpret and display result
    loan_status_map = {0: 'Rejected', 1: 'Approved'}
    predicted_status = loan_status_map[prediction[0]]

    if prediction[0] == 1:
        st.success(f'Prediction: {predicted_status} (Score: {prediction[0]})')
    else:
        st.error(f'Prediction: {predicted_status} (Score: {prediction[0]})')

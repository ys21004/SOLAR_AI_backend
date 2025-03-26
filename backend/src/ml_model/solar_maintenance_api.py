from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the saved model and scaler
try:
    model = joblib.load('solar_maintenance_model.joblib')
    scaler = joblib.load('feature_scaler.joblib')
    feature_columns = joblib.load('feature_columns.joblib')
    print("Model and related files loaded successfully!")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    model = None
    scaler = None
    feature_columns = None

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to predict maintenance needs for solar panels
    Expected input format:
    {
        "dc_power": float,
        "ac_power": float,
        "ambient_temperature": float,
        "module_temperature": float,
        "irradiation": float,
        "timestamp": "YYYY-MM-DD HH:MM:SS"
    }
    """
    if model is None or scaler is None or feature_columns is None:
        return jsonify({"error": "Model not loaded"}), 500

    data = request.get_json()
    # Process the input data and make predictions
    # (Add your prediction logic here)

    return jsonify({"message": "Prediction logic not implemented yet."}), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
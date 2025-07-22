import pandas as pd
import joblib

# === 1. Load trained model ===
# Choose one: 'logistic_model.pkl' or 'random_forest_model.pkl'
model = joblib.load('models/random_forest_model.pkl')

# === 2. Sample input data for prediction ===
# This should match the structure of X_train (10 features)
sample_input = {
    'wind_speed': 25.0,
    'temperature': 32.5,
    'humidity': 65.0,
    'precipitation': 2.5,
    'tree_pollen': 70,
    'grass_pollen': 50,
    'weed_pollen': 30,
    'total_pollen': 150,
    'wind_direction_E': 0,
    'wind_direction_N': 0,
    'wind_direction_NE': 1,
    'wind_direction_NW': 0,
    'wind_direction_S': 0,
    'wind_direction_SE': 0,
    'wind_direction_SW': 0,
    'wind_direction_W': 0
}

# Convert to DataFrame (1 row)
X_new = pd.DataFrame([sample_input])

# Ensure feature order matches training set
# If needed, load X_train and reorder
X_train = pd.read_csv('X_train.csv')
X_new = X_new[X_train.columns]

# === 3. Make prediction ===
prediction = model.predict(X_new)[0]
risk_level = "High Risk" if prediction == 1 else "Low Risk"

print("🩺 Predicted Asthma Risk Level:", risk_level)

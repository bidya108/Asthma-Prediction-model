import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler

model = joblib.load('models/random_forest_model.pkl')
scaler = joblib.load('models/scaler.pkl')

sample_input = {
    'wind_speed': 25.0,
    'temperature': 32.5,
    'humidity': 65.0,
    'precipitation': 2.5,
    'tree_pollen': 70,
    'grass_pollen': 50,
    'weed_pollen': 30,
    'total_pollen': 150,
    'coughing': 1,
    'wheezing': 1,
    'short_breath': 0,
    'trigger_exposure': 1,
    'medication_taken': 0,
    'wind_direction_E': 0,
    'wind_direction_N': 0,
    'wind_direction_NE': 1,
    'wind_direction_NW': 0,
    'wind_direction_S': 0,
    'wind_direction_SE': 0,
    'wind_direction_SW': 0,
    'wind_direction_W': 0
}
X_new = pd.DataFrame([sample_input])         #converting to dataFrame & reordering
X_train = pd.read_csv('X_train.csv')
X_new = X_new[X_train.columns]                     #match exact column order
numeric_cols = X_new.select_dtypes(include=['float64', 'int64']).columns      #numeric features
X_new[numeric_cols] = scaler.transform(X_new[numeric_cols])

prediction = model.predict(X_new)[0]         #predict
risk_level = "High Risk" if prediction == 1 else "Low Risk"
print("Predicted Asthma Risk Level:", risk_level)

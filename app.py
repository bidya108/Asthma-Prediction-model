import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import os
import requests
from datetime import date

# 🌐 App settings
st.set_page_config(page_title="Asthma Risk Predictor", layout="centered")
st.title("Asthma Risk Forecasting")
st.markdown("Enter environmental and personal symptoms to predict asthma risk.")

# 🔌 Load model and scaler
model = joblib.load('models/random_forest_model.pkl')
scaler = joblib.load('models/scaler.pkl') if os.path.exists('models/scaler.pkl') else None

# 🌦️ Weather API function
def get_today_weather():
    api_key = 'SKZ7FS64G3N37QFMJLQ65G2GS'
    LOCATION = 'Bangalore,IN'
    today = date.today().strftime('%Y-%m-%d')
    try:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{LOCATION}/{today}?unitGroup=metric&include=current&key={api_key}&contentType=json"
        response = requests.get(url)
        data = response.json()
        current = data['days'][0]
        return float(current['windspeed']), float(current['temp']), float(current['humidity']), float(current['precip'])
    except Exception as e:
        st.warning(f"Weather fetch failed: {e}")
        return 15.0, 30.0, 60.0, 1.0

# 🌿 Pollen API function for Bangalore
def get_real_pollen():
    api_key = '09a3ab483196fd9ad175973c93142ee08f675bed156c6277c1e0a69bb641d04a'
    headers = {'x-api-key': api_key}
    url = 'https://api.ambeedata.com/latest/pollen/by-place?place=Bangalore'
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if 'data' in data and data['data']:
            pollen = data['data'][0]
            return int(pollen['Count'].get('tree_pollen', 50)), int(pollen['Count'].get('grass_pollen', 30)), int(pollen['Count'].get('weed_pollen', 20))
        else:
            return 50, 30, 20
    except Exception as e:
        st.warning(f"Pollen fetch failed: {e}")
        return 50, 30, 20

# Sidebar toggles
use_auto_weather = st.sidebar.checkbox("📡 Use Live Weather Data", value=True)
use_real_pollen = st.sidebar.checkbox("🌾 Use Real Pollen Data", value=True)

# Fetch values
wind_speed, temperature, humidity, precipitation = get_today_weather() if use_auto_weather else (15.0, 30.0, 60.0, 1.0)
tree_pollen, grass_pollen, weed_pollen = get_real_pollen() if use_real_pollen else (50, 30, 20)

# 🌍 Environmental Inputs
env_col1, env_col2 = st.columns(2)
with env_col1:
    st.markdown("### Environmental Conditions")
    if use_auto_weather:
        st.metric("Wind Speed (km/h)", value=wind_speed)
        st.metric("Temperature (°C)", value=temperature)
        st.metric("Humidity (%)", value=humidity)
        st.metric("Precipitation (mm)", value=precipitation)
    else:
        wind_speed = st.slider("Wind Speed (km/h)", 0.0, 50.0, wind_speed)
        temperature = st.slider("Temperature (°C)", 10.0, 45.0, temperature)
        humidity = st.slider("Humidity (%)", 10.0, 100.0, humidity)
        precipitation = st.slider("Precipitation (mm)", 0.0, 20.0, precipitation)

with env_col2:
    st.markdown("### Pollen Levels")
    if use_real_pollen:
        st.metric("Tree Pollen", value=tree_pollen)
        st.metric("Grass Pollen", value=grass_pollen)
        st.metric("Weed Pollen", value=weed_pollen)
    else:
        tree_pollen = st.slider("Tree Pollen", 0, 100, tree_pollen)
        grass_pollen = st.slider("Grass Pollen", 0, 100, grass_pollen)
        weed_pollen = st.slider("Weed Pollen", 0, 100, weed_pollen)

# Wind direction
wind_direction = st.selectbox("Wind Direction", ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])

# 🧍 Personal symptoms
st.markdown("### Personal Symptoms")
coughing = st.checkbox("Coughing", value=False)
wheezing = st.checkbox("Wheezing", value=False)
short_breath = st.checkbox("Shortness of Breath", value=False)
trigger_exposure = st.checkbox("Exposure to Triggers", value=False)
medication_taken = st.checkbox("Took Medication Today", value=True)

# One-hot encode wind direction
wind_dir_encoded = {f'wind_direction_{d}': 1 if d == wind_direction else 0 for d in ['E', 'N', 'NE', 'NW', 'S', 'SE', 'SW', 'W']}

# Final input
input_data = {
    'wind_speed': wind_speed,
    'temperature': temperature,
    'humidity': humidity,
    'precipitation': precipitation,
    'tree_pollen': tree_pollen,
    'grass_pollen': grass_pollen,
    'weed_pollen': weed_pollen,
    'total_pollen': tree_pollen + grass_pollen + weed_pollen,
    'coughing': int(coughing),
    'wheezing': int(wheezing),
    'short_breath': int(short_breath),
    'trigger_exposure': int(trigger_exposure),
    'medication_taken': int(medication_taken),
    **wind_dir_encoded
}

# Prepare prediction
X = pd.DataFrame([input_data])
X_train = pd.read_csv('X_train.csv')
X = X[X_train.columns]
if scaler:
    numeric_cols = X.select_dtypes(include=['float64', 'int64']).columns
    X[numeric_cols] = scaler.transform(X[numeric_cols])

# 🔮 Predict button
if st.button("Predict Asthma Risk"):
    prediction = model.predict(X)[0]
    result = "High Risk" if prediction == 1 else "Low Risk"
    if prediction == 1:
        st.error(f"Prediction: {result}")
        st.markdown("🚫 Avoid outdoor exposure and take medication if needed.")
    else:
        st.success(f"Prediction: {result}")
        st.markdown("✅ Conditions look safe. Stay cautious and healthy.")

# 📊 Graphs
st.markdown("---")
st.subheader("Weather Trends & Asthma Risk (General Historical Data)")
try:
    df_full = pd.read_csv('asthma_data.csv')
    df_full['date'] = pd.to_datetime(df_full['date'], errors='coerce')

    with st.expander("📈 Show Trend Graphs"):
        fig1 = px.line(df_full, x='date', y='total_pollen', title='Total Pollen Over Time')
        st.plotly_chart(fig1)

        fig2 = px.line(df_full, x='date', y='wind_speed', title='Wind Speed Over Time')
        st.plotly_chart(fig2)

        fig3 = px.bar(df_full, x='date', y='asthma_risk', title='Asthma Risk Per Day', color='asthma_risk')
        st.plotly_chart(fig3)
except:
    st.info("No historical data available for visualization.")

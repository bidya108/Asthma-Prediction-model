import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Try to load real pollen values
def get_real_pollen():
    try:
        df = pd.read_csv('data/real_pollen.csv')
        return int(df['tree_pollen'][0]), int(df['grass_pollen'][0]), int(df['weed_pollen'][0])
    except:
        return None, None, None

# Load the trained model
model = joblib.load('models/random_forest_model.pkl')

# Set page title
st.set_page_config(page_title="Asthma Risk Predictor", layout="centered")

st.title("🩺 Asthma Risk Forecasting")
st.markdown("Enter environmental conditions below to predict asthma risk.")

# Sidebar Inputs
use_real = st.sidebar.checkbox("Use Live Pollen Data", value=False)

# Get real pollen values if available
tree_real, grass_real, weed_real = get_real_pollen()

# Use real values if selected
tree_default = tree_real if use_real and tree_real is not None else 50
grass_default = grass_real if use_real and grass_real is not None else 30
weed_default = weed_real if use_real and weed_real is not None else 20

wind_speed = st.slider("Wind Speed (km/h)", 0.0, 50.0, 15.0)
temperature = st.slider("Temperature (°C)", 10.0, 45.0, 30.0)
humidity = st.slider("Humidity (%)", 10.0, 100.0, 60.0)
precipitation = st.slider("Precipitation (mm)", 0.0, 20.0, 1.0)

tree_pollen = st.slider("Tree Pollen", 0, 100, tree_default)
grass_pollen = st.slider("Grass Pollen", 0, 100, grass_default)
weed_pollen = st.slider("Weed Pollen", 0, 100, weed_default)

wind_direction = st.selectbox("Wind Direction", ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])

# Derived values
total_pollen = tree_pollen + grass_pollen + weed_pollen

# One-hot encode wind_direction
wind_dir_encoded = {f'wind_direction_{d}': 1 if d == wind_direction else 0 for d in ['E', 'N', 'NE', 'NW', 'S', 'SE', 'SW', 'W']}

# Prepare input
input_data = {
    'wind_speed': wind_speed,
    'temperature': temperature,
    'humidity': humidity,
    'precipitation': precipitation,
    'tree_pollen': tree_pollen,
    'grass_pollen': grass_pollen,
    'weed_pollen': weed_pollen,
    'total_pollen': total_pollen,
    **wind_dir_encoded
}

X = pd.DataFrame([input_data])

# Align columns with training data
X_train = pd.read_csv('X_train.csv')
X = X[X_train.columns]

# Predict
if st.button("Predict Asthma Risk"):
    prediction = model.predict(X)[0]
    result = "🌡️ High Risk" if prediction == 1 else "✅ Low Risk"
    st.subheader(f"Prediction: {result}")

# ==========================
# 📊 Visualization Section
# ==========================
st.markdown("---")
st.subheader("📊 Asthma Risk Trends Over Time")

# Load dataset for visualization
df_full = pd.read_csv('asthma_data.csv')
df_full['date'] = pd.to_datetime(df_full['date'])

# Show plots in collapsible expander
with st.expander("📈 Show Trend Graphs"):
    fig1 = px.line(df_full, x='date', y='total_pollen', title='Total Pollen Over Time')
    st.plotly_chart(fig1)

    fig2 = px.line(df_full, x='date', y='wind_speed', title='Wind Speed Over Time')
    st.plotly_chart(fig2)

    fig3 = px.bar(df_full, x='date', y='asthma_risk', title='Asthma Risk Per Day', color='asthma_risk')
    st.plotly_chart(fig3)

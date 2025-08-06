# Asthma Risk Forecasting App

This project is a real-time Asthma Risk Forecasting System built using Streamlit, Machine Learning, and live environmental APIs. It helps users assess their asthma risk based on current weather, pollen levels, and personal symptoms.

> ✅ Ideal for public health awareness, environment monitoring, or predictive healthcare applications.

## Features

- Location-based asthma risk prediction *(default: Bangalore)*
- Real-time weather via **Visual Crossing API**
- Real-time pollen data via **Ambee API**
- Machine learning model to classify risk as **High or Low**
- Trend visualizations (pollen, weather, asthma risk over time)
- Modular structure and easy to deploy

## Installation and Setup

```bash
1. Clone the repository
- git clone https://github.com/your-username/asthma-risk-forecasting.git
- cd asthma-risk-forecasting

2. Install dependencies
- pip install -r requirements.txt

3. Add your API keys in app.py
- Visual Crossing (Weather)
- Ambee (Pollen)
- OpenCage (Geocoding - optional, used in fetch_pollen.py)

4. Run the app
- streamlit run app.py

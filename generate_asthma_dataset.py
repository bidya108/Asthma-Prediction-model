import pandas as pd
import numpy as np
import requests
from datetime import datetime

# === SETUP ===
API_KEY = 'SKZ7FS64G3N37QFMJLQ65G2GS'  # Replace with your actual key
LOCATION = 'Bangalore,IN'
START_DATE = '2025-07-01'
END_DATE = '2025-07-15'

# === Fetch weather data ===
url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{LOCATION}/{START_DATE}/{END_DATE}?unitGroup=metric&include=days&key={API_KEY}&contentType=json"

response = requests.get(url)

if response.status_code != 200:
    raise Exception("Failed to fetch data:", response.text)

weather_json = response.json()
weather_days = weather_json['days']

# === Convert to DataFrame ===
df_weather = pd.DataFrame(weather_days)
df_weather = df_weather[['datetime', 'windspeed', 'winddir', 'temp', 'humidity', 'precip']]
df_weather.rename(columns={
    'datetime': 'date',
    'windspeed': 'wind_speed',
    'winddir': 'wind_direction',
    'temp': 'temperature',
    'precip': 'precipitation'
}, inplace=True)

# === Convert wind_direction from degrees to compass ===
def degrees_to_compass(deg):
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    ix = int((deg + 22.5) // 45) % 8
    return dirs[ix]

df_weather['wind_direction'] = df_weather['wind_direction'].apply(degrees_to_compass)

# === Simulate pollen levels ===
np.random.seed(42)
df_weather['tree_pollen'] = np.random.randint(20, 100, size=len(df_weather))
df_weather['grass_pollen'] = np.random.randint(10, 80, size=len(df_weather))
df_weather['weed_pollen'] = np.random.randint(5, 50, size=len(df_weather))
df_weather['total_pollen'] = df_weather['tree_pollen'] + df_weather['grass_pollen'] + df_weather['weed_pollen']

# === Compute asthma risk ===
df_weather['asthma_risk'] = df_weather.apply(
    lambda row: 1 if row['total_pollen'] > 150 and row['wind_speed'] > 20 else 0,
    axis=1
)

# === Save to CSV ===
df_weather.to_csv('asthma_data.csv', index=False)
print(df_weather.head())

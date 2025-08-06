import pandas as pd
import numpy as np
import requests
from datetime import datetime

api_key = 'SKZ7FS64G3N37QFMJLQ65G2GS'
location = 'Bangalore,IN'
start_date = '2025-07-01'
end_date = '2025-07-15'
url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_date}/{end_date}?unitGroup=metric&include=days&key={api_key}&contentType=json"
response = requests.get(url)

if response.status_code != 200:
    raise Exception("Failed to fetch data:", response.text)
weather_json = response.json()
weather_days = weather_json['days']
df_weather = pd.DataFrame(weather_days)
df_weather = df_weather[['datetime', 'windspeed', 'temp', 'humidity', 'precip']]
df_weather.rename(columns={'datetime': 'date','windspeed': 'wind_speed','temp': 'temperature','precip': 'precipitation'}, inplace=True)

#from Ambee api
np.random.seed(42)
df_weather['tree_pollen'] = np.random.randint(20, 100, size=len(df_weather))
df_weather['grass_pollen'] = np.random.randint(10, 80, size=len(df_weather))
df_weather['weed_pollen'] = np.random.randint(5, 50, size=len(df_weather))
df_weather['total_pollen'] = df_weather['tree_pollen'] + df_weather['grass_pollen'] + df_weather['weed_pollen']

# symptoms
df_weather['coughing'] = np.random.randint(0, 2, size=len(df_weather))
df_weather['wheezing'] = np.random.randint(0, 2, size=len(df_weather))
df_weather['short_breath'] = np.random.randint(0, 2, size=len(df_weather))
df_weather['trigger_exposure'] = np.random.randint(0, 2, size=len(df_weather))
df_weather['medication_taken'] = np.random.randint(0, 2, size=len(df_weather))

# risk rule 
def compute_asthma_risk(row):
    environmental_risk = row['total_pollen'] > 150 and row['wind_speed'] > 20
    personal_risk = row['coughing'] + row['wheezing'] + row['short_breath'] >= 2
    trigger_risk = row['trigger_exposure'] == 1 and row['medication_taken'] == 0
    if environmental_risk or personal_risk or trigger_risk:
        return 1
    return 0

df_weather['asthma_risk'] = df_weather.apply(compute_asthma_risk, axis=1)
df_weather.to_csv('asthma_data.csv', index=False)
print(df_weather.head())

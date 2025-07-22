import requests
import pandas as pd

API_KEY = 'e444ce955bd72a5dff8c8333970bf0d9e18f837d5a8c7340bc3d8ee02ea6386c'  # Replace with your actual key
headers = {
    'x-api-key': API_KEY
}

location = 'Bangalore'
url = f'https://api.ambeedata.com/latest/pollen/by-place?place={location}'

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    pollen = data['data'][0]  # First item in list

    # Extract numeric pollen counts
    tree_count = pollen['Count']['tree_pollen']
    grass_count = pollen['Count']['grass_pollen']
    weed_count = pollen['Count']['weed_pollen']

    # Optional: extract text risk levels
    tree_risk = pollen['Risk']['tree_pollen']
    grass_risk = pollen['Risk']['grass_pollen']
    weed_risk = pollen['Risk']['weed_pollen']

    print("🌾 Real-Time Pollen Levels:")
    print(f"Tree: {tree_count} ({tree_risk})")
    print(f"Grass: {grass_count} ({grass_risk})")
    print(f"Weed: {weed_count} ({weed_risk})")

    # Save to CSV
    df = pd.DataFrame([{
        'tree_pollen': tree_count,
        'grass_pollen': grass_count,
        'weed_pollen': weed_count,
        'tree_risk': tree_risk,
        'grass_risk': grass_risk,
        'weed_risk': weed_risk
    }])
    df.to_csv('data/real_pollen.csv', index=False)

else:
    print("❌ Failed to fetch pollen data:", response.text)

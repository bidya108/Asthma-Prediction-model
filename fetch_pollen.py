import requests
import pandas as pd
import os

ambee_api_key = '09a3ab483196fd9ad175973c93142ee08f675bed156c6277c1e0a69bb641d04a'
opencage_api_key = 'fba0bc1b56ae4a41b453027485c8a1a2'

#geocode
def get_coordinates(place):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={place}&key={opencage_api_key}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get('results')
            if results:
                lat = results[0]['geometry']['lat']
                lng = results[0]['geometry']['lng']
                return lat, lng
        print("Location not found.")
    except Exception as e:
        print("Error fetching coordinates:", e)
    return None, None

#Pollen
def get_pollen_data(lat, lng):
    url = f'https://api.ambeedata.com/latest/pollen/by-lat-lng?lat={lat}&lng={lng}'
    headers = {'x-api-key': ambee_api_key}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'data' not in data or not data['data']:
                print("No data found for this location.")
                return

            pollen = data['data'][0]

            # Count & Risk
            tree_count = pollen['Count'].get('tree_pollen', 50)
            grass_count = pollen['Count'].get('grass_pollen', 30)
            weed_count = pollen['Count'].get('weed_pollen', 20)

            tree_risk = pollen['Risk'].get('tree_pollen', 'Unknown')
            grass_risk = pollen['Risk'].get('grass_pollen', 'Unknown')
            weed_risk = pollen['Risk'].get('weed_pollen', 'Unknown')

            # Detect fallback
            if (tree_count, grass_count, weed_count) == (50, 30, 20):
                print("Fallback default values received (not real-time).")
                print("Try cities like Bangalore, Delhi, Mumbai, London, New York.")

            # Display results
            print(f"\n Pollen Data at ({lat}, {lng}):")
            print(f"Tree Pollen: {tree_count} ({tree_risk})")
            print(f"Grass Pollen: {grass_count} ({grass_risk})")
            print(f"Weed Pollen: {weed_count} ({weed_risk})")

            # Save to CSV
            os.makedirs('data', exist_ok=True)
            df = pd.DataFrame([{
                'latitude': lat,
                'longitude': lng,
                'tree_pollen': tree_count,
                'grass_pollen': grass_count,
                'weed_pollen': weed_count,
                'tree_risk': tree_risk,
                'grass_risk': grass_risk,
                'weed_risk': weed_risk
            }])
            df.to_csv('data/real_pollen.csv', index=False)
            print("Saved to data/real_pollen.csv")

        else:
            print(f"Failed to fetch pollen data: {response.status_code}")
            print(response.text)

    except Exception as e:
        print("Error during pollen data fetch:", e)


#if __name__ == '__main__':
   # place = input("Enter a location (e.g., Bangalore, Delhi, Kashmir, London): ").strip()
   # lat, lng = get_coordinates(place)
    #if lat and lng:
    #    get_pollen_data(lat, lng)
   # else:
    #    print("Could not get coordinates for that place.")
     #   print("Try a major city like: Bangalore, Delhi, New York, London")
        

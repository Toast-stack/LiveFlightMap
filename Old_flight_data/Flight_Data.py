import requests, json

# API request Setup
url = "https://opensky-network.org/api/states/all"

# Fetch flight data from OpenSky API
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Flight data fetched successfully.")

    # Save the data to a JSON file
    with open("flight_data.json", "w") as file:
        json.dump(data, file, indent=4)
        print("Flight data saved to flight_data.json")
else:
    print(f"Failed to fetch flight data. Status code: {response.status_code}")
    print("Response:", response.text)


import json
import pandas as pd

# Load raw aircraft data
with open("flight_data.json", "r") as file:
    flight_data = json.load(file)

# Define correct columns from OpenSky response
columns = [
    "icao24", "callsign", "origin_country", "time_position", "last_contact",
    "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
    "heading", "vertical_rate", "sensors", "geo_altitude", "squawk",
    "spi", "position_source"
]

# Convert to DataFrame
df = pd.DataFrame(flight_data["states"], columns=columns)

# Apply filtering for Florida to New York (approximate boundaries)
df_filtered = df[(df["latitude"] >= 27) & (df["latitude"] <= 41) & 
                 (df["longitude"] >= -81) & (df["longitude"] <= -74)]

# Save filtered data
df_filtered.to_csv("filtered_flight_data.csv", mode="a", header=False, index=False)

print("Filtered aircraft data saved successfully.")
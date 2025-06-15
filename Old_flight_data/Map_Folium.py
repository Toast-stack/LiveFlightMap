import folium
import pandas as pd

# Load the filtered flight data
df = pd.read_csv("filtered_flight_data.csv")

# Create a Folium map centered around the average coordinates of the filtered data
m = folium.Map(location=[df["latitude"].mean(), df["longitude"].mean()], zoom_start=6)

# Add markers for each flight
for _, row in df.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"ICAO24: {row['icao24']}<br>Callsign: {row['callsign']}<br>Country: {row['origin_country']}",
        icon=folium.Icon(color="blue", icon="plane")
    ).add_to(m)

# Save the map to an HTML file
m.save("flight_map.html")
print("Flight map saved to flight_map.html")


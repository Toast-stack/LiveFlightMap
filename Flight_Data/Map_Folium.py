import folium
import psycopg2
import os
import time
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
host = os.getenv("PG_HOST")
database = os.getenv("PG_DATABASE")
user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")

# Connect to PostgreSQL
conn = psycopg2.connect(dbname=database, user=user, password=password, host=host)
cursor = conn.cursor()

# Retrieve filtered flight data (from the last 1 hour)
cursor.execute("""
    SELECT icao24, callsign, origin_country, latitude, longitude, velocity, altitude, time_position_timestamp 
    FROM filtered_flights 
    WHERE time_position_timestamp >= NOW() - INTERVAL '1 hour' 
    ORDER BY time_position_timestamp DESC;
""")
flight_positions = cursor.fetchall()
conn.close()

# Ensure data exists before proceeding
if not flight_positions:
    print("No flight data available for mapping.")
    exit()

# Compute dynamic map centering
avg_lat = sum(flight[3] for flight in flight_positions) / len(flight_positions)
avg_lon = sum(flight[4] for flight in flight_positions) / len(flight_positions)

# Initialize the Folium map
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=6)

# Generate unique colors per aircraft
def get_unique_color(icao24):
    random.seed(hash(icao24))  # Ensure consistent colors per aircraft
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Function to determine marker color based on altitude
def get_marker_color(altitude):
    if altitude > 30000:
        return "green"  # High-altitude aircraft
    elif altitude > 10000:
        return "blue"   # Mid-altitude aircraft
    else:
        return "red"    # Low-altitude aircraft

# Create dictionary for flight paths
flight_dict = {}

# Loop through flight positions and add markers
for flight in flight_positions:
    icao24, callsign, country, lat, lon, velocity, altitude, time_position = flight
    
    # Store flight paths for each aircraft
    if icao24 not in flight_dict:
        flight_dict[icao24] = []
    flight_dict[icao24].append((lat, lon))  

    # Add marker for current flight position (Black for clarity)
    folium.Marker(
    location=[lat, lon],
    popup=(
        f"<b>ICAO24:</b> {icao24}<br>"
        f"<b>Callsign:</b> {callsign}<br>"
        f"<b>Country:</b> {country}<br>"
        f"<b>Altitude:</b> {altitude} ft<br>"
        f"<b>Velocity:</b> {velocity} knots<br>"
        f"<b>Last Update:</b> {time_position}"  # Restoring last seen timestamp
    ),
    icon=folium.Icon(color="black", icon="plane")
).add_to(m)

# Draw flight paths with unique colors and dashed lines for distinction
for icao24, path in flight_dict.items():
    if len(path) > 1:  # Avoid single-point errors
        folium.PolyLine(
            path, 
            color=get_unique_color(icao24), 
            weight=4, 
            opacity=0.9, 
            dash_array="5, 5"  # Dashed pattern
        ).add_to(m)

# Save the map with a timestamped filename
m.save("flight_map.html")  # Overwrite the existing file

print("Flight map saved as flight_map.html")
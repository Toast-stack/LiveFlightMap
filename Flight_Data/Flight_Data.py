import requests
import psycopg2
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
host = os.getenv("PG_HOST")
database = os.getenv("PG_DATABASE")
user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")

# Configure logging
logging.basicConfig(filename="flight_data.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# OpenSky API URL
URL = "https://opensky-network.org/api/states/all"

# Fetch data from API
response = requests.get(URL)

# Validate API response
if response.status_code != 200:
    logging.error(f"API Error: HTTP {response.status_code} - Failed to retrieve flight data.")
    exit()

flight_data = response.json().get("states", [])

# Ensure the API returned valid data
if not flight_data:
    logging.warning("API response received, but no flight data found.")
    exit()

logging.info(f"API response validated: {len(flight_data)} flights detected.")

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(dbname=database, user=user, password=password, host=host)
    cursor = conn.cursor()
except Exception as e:
    logging.error(f"Database connection error: {e}")
    exit()

# SQL query for inserting data
insert_query = """INSERT INTO flights (icao24, callsign, origin_country, time_position, longitude, latitude, velocity, altitude)
                  VALUES (%s, %s, %s, to_timestamp(%s), %s, %s, %s, %s);"""

# Prepare bulk insert data
data_to_insert = [
    (flight[0] or 'UNKNOWN', flight[1] or 'N/A', flight[2] or 'N/A',
     flight[3] if flight[3] else None, flight[5] if flight[5] else 0,
     flight[6] if flight[6] else 0, flight[9] if flight[9] else 0,
     flight[7] if flight[7] else 0)
    for flight in flight_data
]

# Perform bulk insert into database
if data_to_insert:
    try:
        cursor.executemany(insert_query, data_to_insert)
        conn.commit()
        logging.info(f"Successfully inserted {len(data_to_insert)} flight records into the database.")
    except Exception as e:
        logging.error(f"Database insertion error: {e}")
    finally:
        cursor.close()
        conn.close()
        logging.info("Database connection closed.")
else:
    logging.warning("No valid flight data available for insertion.")

print(f"{len(data_to_insert)} flight records processed successfully.")

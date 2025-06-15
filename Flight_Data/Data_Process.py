import psycopg2
import os
import pandas as pd
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

# Filter flights based on geographic region
query = """SELECT * FROM flights
           WHERE latitude BETWEEN 27 AND 41
           AND longitude BETWEEN -81 AND -74
           ORDER BY time_position DESC;"""

cursor.execute(query)
filtered_data = cursor.fetchall()
conn.commit()

# Insert filtered data into `filtered_flights` table
insert_query = """INSERT INTO filtered_flights (icao24, callsign, origin_country, time_position, longitude, latitude, velocity, altitude, time_position_timestamp)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""

#print(filtered_data[:5])  # Show first 5 entries to check structure
"""for row in filtered_data[:5]:  # Check first 5 rows
    print([type(value) for value in row])
    print(f"Row data: {row}, Length: {len(row)}")
    """

formatted_data = [
    (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]) 
    for row in filtered_data if len(row) >= 10  # Ensure data has enough elements
]
cursor.executemany(insert_query, formatted_data)
conn.commit()

cursor.close()
conn.close()

print(f"Filtered {len(filtered_data)} flight records successfully stored in the database!")
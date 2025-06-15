import schedule
import time
import subprocess

def fetch_and_process_data():
    print("Fetching aircraft data...")
    subprocess.run(["python", "Flight_Data.py"])  # Fetch raw flight data

    print("Processing filtered data...")
    subprocess.run(["python", "Data_Process.py"])  # Filter and store flight data

    print("Generating updated map...")
    subprocess.run(["python", "Map_Folium.py"])  # Create Folium visualization

    print("Data processed and map updated at:", time.strftime("%Y-%m-%d %H:%M:%S"))

# Schedule the entire process to run every 10 minutes
schedule.every(10).minutes.do(fetch_and_process_data)

while True:
    schedule.run_pending()
    time.sleep(1)


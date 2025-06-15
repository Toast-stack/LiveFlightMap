# Flight Tracker & Map Visualization System

A real‑time flight tracking system that evolved from a simple JSON/CSV‑based approach to a robust, database‐driven application. This project demonstrates the following concepts:
- API data fetching and processing
- Data transformation from JSON to CSV
- Database integration using PostgreSQL
- Dynamic data filtering and visualization using Folium
- Web serving and on‑demand updates with Flask
- Development best practices, logging, and automation

---

## Table of Contents

- [Overview](#overview)
- [Project Evolution](#project-evolution)
  - [Older Version: JSON & CSV-Based](#older-version)
  - [Newer Version: Database‑Driven](#newer-version-database-driven)
- [Features](#features)
- [Installation & Requirements](#installation--requirements)
- [Usage](#usage)
  - [Running the Flask Server](#running-the-flask-server)
  - [Map Update Process](#map-update-process)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [References](#references)
- [License](#license)

---

## Overview

This project demonstrates a flight tracking system that:
- Fetches live flight data from an API.
- Initially stored results in a JSON file, then converted to CSV for generating a flight map with Folium.
- Evolved into a more efficient system using PostgreSQL to store and query flight data.
- Provides a dynamic web interface using Flask where users can:
  - View an interactive flight map.
  - Update the map on demand with a refresh button.
  
Through this, I explored JSON/CSV file operations, SQL database integration, and real‑time web serving with Python.

---

## Project Evolution

<h3 id="older-version">Older Version: JSON & CSV-Based</h3>

- **Data Source:** Flight data fetched from an API.
- **Storage:**  
  - Fetched data is stored in a JSON file.
  - A conversion script then outputs CSV data for use in mapping.
- **Mapping:**  
  - The CSV data is loaded into a Pandas DataFrame.
  - Folium is used to plot flight positions on an interactive map.
- **Limitation:**  
  - Difficulties in scaling with increased data.
  - Manual overwrites and limited flexibility in handling dynamic data.

### <a name="newer-version-database-driven"></a>Newer Version: Database‑Driven

- **Data Source:** Flight data is received from the same API.
- **Storage:**  
  - Data is stored in a PostgreSQL database.
  - Two primary scripts are used:
    - One for fetching & storing API data.
    - Another for processing and filtering records (e.g., filtering flights in the last hour).
- **Mapping:**  
  - A custom Python script (using Folium) generates an interactive flight map.
  - Each aircraft is differentiated with unique colors, thicker and dashed flight paths, and detailed popups.
- **Web Interface:**  
  - A Flask‑based web server hosts the map.
  - An update endpoint is provided so users can refresh the map on demand via a button click.
- **Advantage:**  
  - Real‑time updates and improved performance.
  - Better management of larger datasets and historical records.

---

## Features

- **Dynamic Data Fetching:**  
  Fetches live flight data from an API.

- **Flexible Data Processing:**  
  Two modes:
  - JSON & CSV conversion (older version)
  - Database processing using PostgreSQL (newer version)

- **Interactive Mapping:**  
  Visualizes flight data with unique styles for each aircraft:
  - Unique colors based on the aircraft identifier.
  - Dashed lines and enhanced markers for current positions.
  - Detailed popups showing flight info (callsign, altitude, velocity, etc).

- **User‑Triggered Refresh:**  
  A web page (built with Flask) featuring a refresh button that triggers data update scripts and automatically reloads the map.

---

## Installation & Requirements

### Installation Requirements

- **Python 3.8+**  
- **PostgreSQL**  
- **pip** (to install Python packages)

### Python Dependencies

Install the required packages with:

```bash
pip install -r requirements.txt
```

### Database Setup
1. Install PostgreSQL and create a database (e.g., `flight_db`).
2. Setup your `filtered_flights` table with the following columns (or adjust as needed):
``` SQL
CREATE TABLE filtered_flights (
    id SERIAL PRIMARY KEY,
    icao24 VARCHAR(50),
    callsign VARCHAR(50),
    origin_country VARCHAR(50),
    time_position TIME,
    longitude FLOAT,
    latitude FLOAT,
    velocity FLOAT,
    altitude FLOAT,
    time_position_timestamp TIMESTAMP
);
```
3. Create a `.env` file in the root directory with the following variables:
```
PG_HOST=your_postgres_host
PG_DATABASE=flight_db
PG_USER=your_username
PG_PASSWORD=your_password
```

## Usage
### Running the Flask Server
Start the Flask Server with:
```Bash
python server.py
```
- **Main Page**: Opens at `http://localhost:5000` and displays the interactive map.
- **Map Refresh**: Click the "**Update Map**" button to trigger the update.
  The System then runs sequential scripts to fetch new flight data, process it, and regenerate the map as `flight_map.html`. The map iframe reloads with the latest data.

### Map Update Process
1. Fetch Data: `Flight_Data.py` connects to the API and stores new results.
2. Process Data: `Data_Process.py` filters and processes the flight data for the desired Locations.
3. Generate Map: `Map_folium.py` generates an interactive map:
   - Unique colors for each aircraft.
   - Dashed Flight paths with thicker lines.
   - Detailed popups showing flight metadata.
4. Web Refresh: A call to `/update` triggers these scripts, and the main page reloads the updated `flight_map.html` file.

## Project Structure
```
Flight_Tracker/
├── Flight_Data.py         # Script for fetching flight data from the API
├── Data_Process.py        # Script for processing and filtering flight data
├── Map_Folium.py          # Script for generating the interactive flight map
├── server.py              # Flask server hosting the map and update endpoint
├── templates/
│   └── index.html         # Web interface with refresh button and iframe for the map
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables for database configuration
└── README.md              # Project documentation (this file)
```

## Documentation
### Detailed Documentation
- API Data Retrieval:
  - `Flight_Data.py` fetches data and logs output to ensure new data is inserted into the database.
- Data Processing:
  - `Data_Process.py` transforms and filters flight data based on location.
- Web Interface:
  - `server.py` serves both the map and an updated interface.
  - `templates/index.html` provides an intuitive refresh button that reloads the iframe to show the latest map.
Comprehensive in-code comments and error handling provide insights into each component's operation.

## References
- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Folium Documentation](https://python-visualization.github.io/folium/latest/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Python Requests Documentation](https://requests.readthedocs.io/en/latest/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Python-dotenv Documentation](https://pypi.org/project/python-dotenv/)

## License
This project is licensed under the MIT License. See the LICENSE file for details.

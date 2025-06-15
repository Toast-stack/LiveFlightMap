from flask import Flask, render_template, send_file
import subprocess

app = Flask(__name__)

@app.route('/')
def display_map():
    return render_template("index.html")  # Serve the page with a refresh button

@app.route('/update')
def update_map():
    try:
        subprocess.run(["python", "Flight_Data.py"])   # Fetch new flight data
        subprocess.run(["python", "Data_Process.py"])  # Process data
        subprocess.run(["python", "Map_Folium.py"])    # Generate updated map
        return "Map updated successfully! Refresh the page to see changes."
    except Exception as e:
        return f"Error updating map: {e}"

@app.route('/map')
def serve_map():
    return send_file("flight_map.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
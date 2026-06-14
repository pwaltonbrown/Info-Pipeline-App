# Name: weather_pipeline.py
# Description: This is a program that will pull weather data from a free api website and organize it in a easer to read format.
# Author: Patrick Brown
# Date: 6/7/2026


# Import libraries
import os
import requests
import pandas as pd
from datetime import datetime

# 1. Clean Configuration Layout (Updated for 3.0 Coordinates)
CITY_NAME = "Raleigh"  # Used for your CSV logging name
LAT = "35.7796"       # Raleigh, NC Latitude
LON = "-78.6382"      # Raleigh, NC Longitude

API_KEY = os.environ.get("WEATHER_API_KEY")
CSV_FILE = "weather_history.csv"

# FIXED: Swapped legacy 2.5 endpoint for the universally supported One Call 3.0 endpoint
BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

def run_pipeline():
    # 2. Package parameters cleanly as a safe dictionary (Updated for 3.0 payload)
    query_params = {
        "lat": LAT,
        "lon": LON,
        "exclude": "minutely,hourly,daily,alerts", # We only want current weather
        "appid": API_KEY,
        "units": "imperial"
    }

    # 3. Extract Data from API
    response = requests.get(BASE_URL, params=query_params)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        print(f"Server response details: {response.text}")
        return

    # Parse the JSON response
    raw_data = response.json()

    # 4. Transform Data (Updated to match 3.0 JSON key nesting)
    cleaned_data = {
        "timestamp": [datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")],
        "city": [CITY_NAME],
        "temperature": [raw_data["current"]["temp"]],
        "humidity": [raw_data["current"]["humidity"]],
        "weather_condition": [raw_data["current"]["weather"][0]["description"]]
    }

    # Create a DataFrame
    df_new = pd.DataFrame(cleaned_data)

    # 5. Load Data
    if os.path.exists(CSV_FILE):
        df_existing = pd.read_csv(CSV_FILE)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_final = df_new

    # 6. Save Data
    df_final.to_csv(CSV_FILE, index=False)

    # 7. Log
    print(f"Successfully saved weather data for {CITY_NAME} using API v3.0!")

# 8. Run the pipeline
if __name__ == "__main__":
    run_pipeline()

# Name: weather_pipeline.py
# Description: This is a program that will pull weather data from a free api website and organize it in a easer to read format.
# Author: Patrick Brown
# Date: 6/7/2026


# Import libraries
import os
import requests
import pandas as pd
from datetime import datetime

## Use this exact config block if you are on the basic Free Plan:
CITY = "raleigh,nc,us"
API_KEY = os.environ.get("WEATHER_API_KEY")
CSV_FILE = "weather_history.csv"

def run_pipeline():
    
    # 4. Fetch Data
    query_params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "imperial"
    }
    
    # Make sure there's a ? before the first parameter
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY.replace(',', '%2C')}&appid={API_KEY}&units=imperial"
    response = requests.get(URL)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        print(f"Details: {response.text}")
        return

    # Parse the JSON response
    raw_data = response.json()

    # Match the JSON structure for 2.5 Current Weather
    cleaned_data = {
        "timestamp": [datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")],
        "city": [raw_data["name"]],
        "temperature": [raw_data["main"]["temp"]],
        "humidity": [raw_data["main"]["humidity"]],
        "weather_condition": [raw_data["weather"][0]["description"]]
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
    print(f"Successfully saved weather data for {CITY} using API v2.5!")

# 8. Run the pipeline
if __name__ == "__main__":
    run_pipeline()
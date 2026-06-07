# Name: weather_pipeline.py
# Description: This is a program that will pull weather data from a free api website and organize it in a easer to read format.
# Author: Patrick Brown
# Date: 6/7/2026


# Import libraries
import os
import requests
import pandas as pd
from datetime import datetime

import os
import requests
import pandas as pd
from datetime import datetime

# 1. Clean Configuration Layout
CITY = "Raleigh,NC,US"
API_KEY = os.environ.get("WEATHER_API_KEY")
CSV_FILE = "weather_history.csv"

# FIXED: Added BASE_URL
BASE_URL = "http://openweathermap.org"

def run_pipeline():
    # 2. Package parameters cleanly as a safe dictionary
    query_params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "imperial"
    }

    # 3. Extract Data (Requests will handle building the URL safely)
    response = requests.get(BASE_URL, params=query_params)
    
    # FIXED: Added error handling
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        print(f"Server response details: {response.text}") # Helps us see exact API errors
        return
    raw_data = response.json()

    # 4. Transform Data
    cleaned_data = {
        "timestamp": [datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")],
        "city": [raw_data["name"]],
        "temperature": [raw_data["main"]["temp"]],
        "humidity": [raw_data["main"]["humidity"]],
        "weather_condition": [raw_data["weather"][0]["description"]] # FIXED: Added index [0] to avoid future pandas issues
    }
    df_new = pd.DataFrame(cleaned_data)

    # 5. Load Data
    if os.path.exists(CSV_FILE):
        df_existing = pd.read_csv(CSV_FILE)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_csv(CSV_FILE, index=False)
    print(f"Successfully saved weather data for {CITY}!")

if __name__ == "__main__":
    run_pipeline()

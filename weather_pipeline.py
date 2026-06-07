# Name: weather_pipeline.py
# Description: This is a program that will pull weather data from a free api website and organize it in a easer to read format.
# Author: Patrick Brown
# Date: 6/7/2026


# Import libraries
import os
import requests
import pandas as pd
from datetime import datetime

# Pipeline configuration
API_KEY = os.getenv('WEATHER_API_KEY')  
location = "raleigh,nc,us"
CSV_FILE = "weather_history.csv"

# Build the URL
url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=imperial"

# Run the pipeline
def run_pipeline():

    # 1. Extract Data    
    response = requests.get(URL)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return
    
    # Get the raw data
    raw_data = response.json()

    # 2. Transform Data
    cleaned_data = {
        
        # Create a dictionary
        "timestamp": [datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")],
        
        # Create a list
        "city": [raw_data["name"]],
        "temperature": [raw_data["main"]["temp"]],
        "humidity": [raw_data["main"]["humidity"]],
        "weather_condition": [raw_data["weather"][0]["description"]]
    }
    
    # Create a DataFrame
    df_new = pd.DataFrame(cleaned_data)

    # 3. Load Data (Append to local file)
    if os.path.exists(CSV_FILE):
        
        # Read existing data
        df_existing = pd.read_csv(CSV_FILE)
        
        # Append new data
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    
    else:

        # Create a new DataFrame
        df_final = df_new

    # Save data
    df_final.to_csv(CSV_FILE, index=False)
    
    # 4. Log Data
    print(f"Successfully saved weather data for {CITY}!")

# Run the pipeline
if __name__ == "__main__":
    run_pipeline()

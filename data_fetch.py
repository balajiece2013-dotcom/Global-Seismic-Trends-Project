#Data Collection (API)
#Source: USGS Public API.

#Method: Python requests library use panni year-by-year data fetch pannen.

#Storage: Pandas DataFrame-ah convert panni process pannen.

import requests  # Used to send HTTP requests to the USGS API
import pandas as pd  # Used for data manipulation and DataFrame creation
from datetime import datetime  # Used to convert timestamp into readable datetime format

# Base URL of the official USGS Earthquake API
BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# List to store all earthquake records collected from API
all_records = []

# Loop through 5 years (2020 to 2024)
for year in range(2020, 2025):  # 2020, 2021, 2022, 2023, 2024
    for month in range(1, 13):  # Loop through all 12 months

        # Generate start date dynamically (e.g., 2020-01-01)
        start_date = f"{year}-{month:02d}-01"

        # Generate end date
        # If December, end date is 31st December
        # Otherwise, next month's 1st date is used
        if month == 12:
            end_date = f"{year}-12-31"
        else:
            end_date = f"{year}-{month+1:02d}-01"

        # Parameters sent to API request
        params = {
            "format": "geojson",  # Response format as GeoJSON
            "starttime": start_date,  # Filter by start date
            "endtime": end_date,  # Filter by end date
            "minmagnitude": 4.5  # Fetch only earthquakes with magnitude >= 4.5
        }

        print(f"Fetching {start_date}", flush=True)

        try:
            # Send GET request to API with parameters
            response = requests.get(BASE_URL, params=params, timeout=30)
        except Exception as e:
            # Handle network or request errors without stopping program
            print("Request error:", e)
            continue

        # Check if API response is valid
        if response.status_code != 200 or response.text.strip() == "":
            print("API error, skipping...")
            continue

        # Convert API response to JSON format
        data = response.json()

        # Extract earthquake records from 'features' key
        features = data.get("features", [])

        print("Records:", len(features))

        # Loop through each earthquake record
        for f in features:
            props = f["properties"]  # Contains earthquake details
            geom = f["geometry"]  # Contains geographic coordinates

            # Create structured record dictionary
            record = {
                "id": f["id"],  # Unique earthquake ID

                # Convert timestamp (milliseconds) to UTC datetime format
                "time": datetime.utcfromtimestamp(props["time"] / 1000),
                "updated": datetime.utcfromtimestamp(props["updated"] / 1000),

                # GeoJSON coordinates are stored as [longitude, latitude, depth]
                "latitude": geom["coordinates"][1],
                "longitude": geom["coordinates"][0],
                "depth_km": geom["coordinates"][2],  # Depth in kilometers

                "mag": props["mag"],  # Magnitude value
                "magType": props["magType"],  # Type of magnitude (Mw, ML, etc.)
                "place": props["place"],  # Location description
                "status": props["status"],  # Review status
                "tsunami": props["tsunami"],  # Tsunami alert flag (0 or 1)
                "sig": props["sig"],  # Significance score
                "net": props["net"],  # Network ID
                "nst": props["nst"],  # Number of seismic stations
                "dmin": props["dmin"],  # Distance to nearest station
                "rms": props["rms"],  # Root mean square travel time residual
                "gap": props["gap"],  # Azimuthal gap
                "magError": props.get("magError", 0),  # Magnitude error (default 0 if missing)
                "depthError": props.get("depthError", 0),  # Depth error
                "magNst": props.get("magNst", 0),  # Number of stations for magnitude
                "locationSource": props.get("locationSource", None),  # Location data source
                "magSource": props.get("magSource", None),  # Magnitude data source
                "types": props["types"],  # Types of data available
                "ids": props["ids"],  # Alternate IDs
                "sources": props["sources"],  # Data sources
                "type": props["type"]  # Earthquake type
            }

            # Append structured record to master list
            all_records.append(record)

# Print total records collected
print("Total records:", len(all_records))

# Convert list of dictionaries into Pandas DataFrame
df = pd.DataFrame(all_records)

# Display first 5 rows for verification
print(df.head())

# Save cleaned dataset as CSV file for dashboard usage
df.to_csv("earthquakes_5years.csv", index=False)

print("CSV saved")


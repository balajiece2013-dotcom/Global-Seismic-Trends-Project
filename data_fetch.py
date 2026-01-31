import requests
import pandas as pd
from datetime import datetime

BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

all_records = []

# 5 years loop (2020–2024 example)
for year in range(2020, 2025):          # 2020,2021,2022,2023,2024
    for month in range(1, 13):          # All 12 months

        start_date = f"{year}-{month:02d}-01"

        if month == 12:
            end_date = f"{year}-12-31"
        else:
            end_date = f"{year}-{month+1:02d}-01"

        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "minmagnitude": 4.5
        }

        print(f"Fetching {start_date}", flush=True)

        try:
            response = requests.get(BASE_URL, params=params, timeout=30)
        except Exception as e:
            print("Request error:", e)
            continue

        if response.status_code != 200 or response.text.strip() == "":
            print("API error, skipping...")
            continue

        data = response.json()
        features = data.get("features", [])

        print("Records:", len(features))

        for f in features:
            props = f["properties"]
            geom = f["geometry"]

            record = {
                "id": f["id"],
                "time": datetime.utcfromtimestamp(props["time"] / 1000),
                "updated": datetime.utcfromtimestamp(props["updated"] / 1000),
                "latitude": geom["coordinates"][1],
                "longitude": geom["coordinates"][0],
                "depth_km": geom["coordinates"][2],
                "mag": props["mag"],
                "magType": props["magType"],
                "place": props["place"],
                "status": props["status"],
                "tsunami": props["tsunami"],
                "sig": props["sig"],
                "net": props["net"],
                "nst": props["nst"],
                "dmin": props["dmin"],
                "rms": props["rms"],
                "gap": props["gap"],
                "magError": props.get("magError", 0),
                "depthError": props.get("depthError", 0),
                "magNst": props.get("magNst", 0),
                "locationSource": props.get("locationSource", None),
                "magSource": props.get("magSource", None),
                "types": props["types"],
                "ids": props["ids"],
                "sources": props["sources"],
                "type": props["type"]
            }

            all_records.append(record)

print("Total records:", len(all_records))

df = pd.DataFrame(all_records)
print(df.head())

df.to_csv("earthquakes_5years.csv", index=False)
print("CSV saved")


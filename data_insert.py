import pandas as pd
import mysql.connector
import numpy as np
import os  # For secure password handling (recommended)

# --------------------------------------------------
# 1️⃣ Load Cleaned CSV Data
# --------------------------------------------------
df = pd.read_csv("earthquake_clean.csv")

# --------------------------------------------------
# 2️⃣ Numeric Columns NULL Fix (Mean Imputation)
# Replace missing numeric values with column average
# --------------------------------------------------
numeric_cols = ['mag', 'depth_km', 'nst', 'dmin', 'rms', 
                'gap', 'magError', 'depthError', 'magNst', 'sig']

for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mean())

# --------------------------------------------------
# 3️⃣ Text Columns NULL Fix
# Replace missing text values with "Unknown"
# --------------------------------------------------
text_cols = ['locationSource', 'magSource', 'types', 'status', 
             'magType', 'net', 'place', 'country', 'day_of_week']

for col in text_cols:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")

# --------------------------------------------------
# 4️⃣ Derived Columns Processing
# Extract Year and Month from datetime
# Create Depth & Magnitude Category Flags
# --------------------------------------------------
df['time'] = pd.to_datetime(df['time'])
df['month_val'] = df['time'].dt.month
df['year_val'] = df['time'].dt.year

# Depth Category Logic
def get_depth_flag(depth):
    if depth is None or pd.isna(depth):
        return 'Unknown'
    if depth <= 70:
        return 'Shallow'
    elif depth <= 300:
        return 'Intermediate'
    else:
        return 'Deep'

# Magnitude Category Logic
def get_mag_flag(mag):
    if mag is None or pd.isna(mag):
        return 'Unknown'
    if mag >= 6.0:
        return 'Destructive'
    elif mag >= 4.5:
        return 'Strong'
    else:
        return 'Minor'

df['depth_flag'] = df['depth_km'].apply(get_depth_flag)
df['mag_flag'] = df['mag'].apply(get_mag_flag)

# --------------------------------------------------
# 5️⃣ Final NULL Replace
# Convert remaining NaN to None (MySQL compatible)
# --------------------------------------------------
df = df.replace({np.nan: None})

# --------------------------------------------------
# 6️⃣ MySQL Database Connection
# --------------------------------------------------

# 🔐 Recommended secure method
password = os.getenv("DB_PASSWORD")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,  # Avoid hardcoding
    database="earthquakes"
)

cursor = conn.cursor()

# --------------------------------------------------
# 7️⃣ Insert Query (32 Columns)
# --------------------------------------------------
sql = """
    INSERT INTO earthquake_data 
    (id, time_utc, updated_utc, latitude, longitude, depth_km, mag, magType, place, 
    status, tsunami, sig, net, nst, dmin, rms, gap, magError, depthError, 
    magNst, locationSource, magSource, types, ids, sources, type, country, 
    day_of_week, year, month, depth_flag, mag_flag)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# --------------------------------------------------
# 8️⃣ Insert Row by Row into MySQL
# --------------------------------------------------
for _, row in df.iterrows():
    values = (
        row.get('id'), row.get('time'), row.get('updated'),
        row.get('latitude'), row.get('longitude'),
        row.get('depth_km'), row.get('mag'), row.get('magType'),
        row.get('place'), row.get('status'), row.get('tsunami'),
        row.get('sig'), row.get('net'), row.get('nst'),
        row.get('dmin'), row.get('rms'), row.get('gap'),
        row.get('magError'), row.get('depthError'),
        row.get('magNst'), row.get('locationSource'),
        row.get('magSource'), row.get('types'),
        row.get('ids'), row.get('sources'),
        row.get('type'), row.get('country'),
        row.get('day_of_week'),
        row.get('year_val'), row.get('month_val'),
        row.get('depth_flag'), row.get('mag_flag')
    )

    cursor.execute(sql, values)

# --------------------------------------------------
# 9️⃣ Commit Changes & Close Connection
# --------------------------------------------------
conn.commit()

print(f"✅ Success! {len(df)} records with 32 columns inserted (No NULL issues).")

cursor.close()
conn.close()
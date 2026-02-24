#Data Cleaning (Mentor Logic)
#Numeric Fix: Numeric columns-la NULL values-ku bathila Mean (Average) fill pannen.

#Text Fix: Text columns-la NULL-ku bathila 'Unknown' nu replace pannen.

#Regex: place column-la irunthu country name-ai extract pannen.



import pandas as pd

# Step 1: Load raw 5-year earthquake dataset
df = pd.read_csv("earthquakes_5years.csv")

# Step 2: Convert time-related fields to proper datetime format
df["time"] = pd.to_datetime(df["time"], errors="coerce")
df["updated"] = pd.to_datetime(df["updated"], errors="coerce")

# Step 3: Derive new columns from datetime
df["year"] = df["time"].dt.year.astype(int)   # Extract year as integer
df["month"] = df["time"].dt.month            # Extract month number
df["day"] = df["time"].dt.day                # Extract day of month
df["day_of_week"] = df["time"].dt.day_name() # Extract weekday name

# Step 4: Depth classification (Shallow vs Deep)
df["depth_flag"] = df["depth_km"].apply(lambda x: "Shallow" if x < 50 else "Deep")

# Step 5: Strength classification (Normal vs Destructive)
df["strength_flag"] = df["mag"].apply(lambda x: "Destructive" if x >= 7.5 else "Normal")

# Step 6: Extract country name from 'place' field using regex
# If no match, fill with "Unknown"
df["country"] = df["place"].str.extract(r",\s*([A-Za-z\s]+)$").fillna("Unknown")

# Step 7: Clean numeric fields (convert to float, replace invalids with 0)
numeric_cols = ["mag","depth_km","nst","dmin","rms","gap","magError","depthError","magNst","sig"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Step 8: Save cleaned dataset to new CSV file
df.to_csv("earthquake_clean.csv", index=False)

# Step 9: Print summary info
print("✅ Data cleaning complete. Columns:", len(df.columns))
print(df.head())  # Show first 5 rows
print(df["year"].value_counts().sort_index())  # Show year-wise record counts


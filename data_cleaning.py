#Data Cleaning (Mentor Logic)
#Numeric Fix: Numeric columns-la NULL values-ku bathila Mean (Average) fill pannen.

#Text Fix: Text columns-la NULL-ku bathila 'Unknown' nu replace pannen.

#Regex: place column-la irunthu country name-ai extract pannen.



import pandas as pd  # Library used for data manipulation and analysis

# Step 1: Load raw 5-year earthquake dataset from CSV file
# This file was created during the data fetching phase
df = pd.read_csv("earthquakes_5years.csv")

# Step 2: Convert time-related columns into proper datetime format
# errors="coerce" ensures invalid formats are converted to NaT instead of crashing
df["time"] = pd.to_datetime(df["time"], errors="coerce")
df["updated"] = pd.to_datetime(df["updated"], errors="coerce")

# Step 3: Create new time-based features from 'time' column
# Feature engineering for trend analysis

df["year"] = df["time"].dt.year.astype(int)   # Extract year (for yearly trend analysis)
df["month"] = df["time"].dt.month            # Extract month (for seasonal/monthly analysis)
df["day"] = df["time"].dt.day                # Extract day of month
df["day_of_week"] = df["time"].dt.day_name() # Extract weekday name (Monday, Tuesday, etc.)

# Step 4: Classify earthquake depth into categories
# If depth < 50 km → Shallow, else → Deep
# Helps in analyzing shallow vs deep earthquake distribution
df["depth_flag"] = df["depth_km"].apply(
    lambda x: "Shallow" if x < 50 else "Deep"
)

# Step 5: Classify earthquake strength based on magnitude
# Magnitude >= 7.5 considered Destructive, else Normal
# Helps identify high-impact earthquakes
df["strength_flag"] = df["mag"].apply(
    lambda x: "Destructive" if x >= 7.5 else "Normal"
)

# Step 6: Extract country name from 'place' column using Regular Expression
# Example: "123 km SE of Tokyo, Japan" → Extracts "Japan"
# If extraction fails, fill missing values with "Unknown"
df["country"] = df["place"].str.extract(
    r",\s*([A-Za-z\s]+)$"
).fillna("Unknown")

# Step 7: Clean numeric columns
# Convert selected columns to numeric type
# errors="coerce" converts invalid values to NaN
# fillna(0) replaces missing values with 0 for consistency

numeric_cols = [
    "mag","depth_km","nst","dmin","rms",
    "gap","magError","depthError","magNst","sig"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Step 8: Save cleaned dataset into a new CSV file
# This file will be used for dashboard visualization
df.to_csv("earthquake_clean.csv", index=False)

# Step 9: Print summary information for verification
print("✅ Data cleaning complete. Columns:", len(df.columns))
print(df.head())  # Display first 5 rows to verify cleaned data
print(df["year"].value_counts().sort_index())  # Display year-wise earthquake counts


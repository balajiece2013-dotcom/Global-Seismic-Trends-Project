import pandas as pd

# Step 1: DataFrame load 
df = pd.read_csv("earthquakes_test.csv") 

# Step 2: Date/Time fields convertion
df["time"] = pd.to_datetime(df["time"])
df["updated"] = pd.to_datetime(df["updated"])

# Step 3: Derived columns add 
df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
df["day"] = df["time"].dt.day
df["day_of_week"] = df["time"].dt.day_name()

# Step 4: Depth flag (shallow vs deep)
df["depth_flag"] = df["depth_km"].apply(lambda x: "Shallow" if x < 50 else "Deep")

# Step 5: Strength flag (normal vs destructive)
df["strength_flag"] = df["mag"].apply(lambda x: "Destructive" if x >= 7.5 else "Normal")

# Step 6: Country extract (Regex)
df["country"] = df["place"].str.extract(r",\s*([A-Za-z\s]+)$")

# Step 7: Numeric fields clean 
numeric_cols = ["mag","depth_km","nst","dmin","rms","gap","magError","depthError","magNst","sig"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Step 8: Cleaned data save 
df.to_csv("earthquake_clean.csv", index=False)

print("Data cleaning complete. Total columns:", len(df.columns))
print(df.head())


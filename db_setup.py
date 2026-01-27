import pandas as pd
from sqlalchemy import create_engine

# Step 1: Cleaned data load 
df = pd.read_csv("earthquake_clean.csv")

# Step 2: MySQL connection setup
# Format: mysql+mysqlconnector://username:password@localhost/databasename
engine = create_engine("mysql+mysqlconnector://root:12345@localhost/earthquakes")

# Step 3: DataFrame → MySQL table insert
df.to_sql("earthquake_data", con=engine, if_exists="replace", index=False)

print("Data inserted into MySQL successfully!")


import streamlit as st
import pandas as pd

# Step 1: Cleaned data load 
df = pd.read_csv("earthquake_clean.csv")

# Step 2: Dashboard title
st.title("🌍 Global Seismic Trends Dashboard")

# Step 3: Filters (Year + Country)
year = st.selectbox("Select Year", sorted(df["year"].unique()))
country = st.selectbox("Select Country", sorted(df["country"].dropna().unique()))

# Step 4: Filtered dataset
filtered = df[(df["year"] == year) & (df["country"] == country)]

# Step 5: Map visualization
st.subheader("Earthquake Locations")
st.map(filtered[["latitude", "longitude"]])

# Step 6: Monthly count bar chart
st.subheader("Monthly Earthquake Count")
st.bar_chart(filtered["month"].value_counts())

# Step 7: Magnitude trend line chart
st.subheader("Average Magnitude by Month")
st.line_chart(filtered.groupby("month")["mag"].mean())

# Step 8: Depth vs Magnitude scatter plot
st.subheader("Depth vs Magnitude")
st.scatter_chart(filtered[["depth_km", "mag"]])

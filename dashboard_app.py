import streamlit as st
import pandas as pd

df = pd.read_csv("earthquake_clean.csv")
df["time"] = pd.to_datetime(df["time"], errors="coerce")
df["year"] = df["time"].dt.year.astype(int)
df["month"] = df["time"].dt.month
df["country"] = df["place"].str.extract(r",\s*([A-Za-z\s]+)$")

st.title("🌍 Global Seismic Trends Dashboard")

year = st.selectbox("Select Year", sorted(df["year"].unique()))
country = st.selectbox("Select Country", sorted(df["country"].dropna().unique()))


filtered = df[(df["year"] == year) & (df["country"] == country)]

if filtered.empty:
    st.warning("⚠️ No earthquake records found for this selection.")
else:
    st.subheader("Earthquake Locations")
    st.map(filtered[["latitude", "longitude"]])

    st.subheader("Monthly Earthquake Count")
    st.bar_chart(filtered["month"].value_counts().sort_index())

    st.subheader("Average Magnitude by Month")
    st.line_chart(filtered.groupby("month")["mag"].mean())

    st.subheader("Depth vs Magnitude")
    st.scatter_chart(filtered[["depth_km", "mag"]])


import streamlit as st
import pandas as pd

# Load cleaned dataset
df = pd.read_csv("earthquake_clean.csv")
df["time"] = pd.to_datetime(df["time"], errors="coerce")
df["year"] = df["time"].dt.year.astype(int)
df["month"] = df["time"].dt.month
df["country"] = df["place"].str.extract(r",\s*([A-Za-z\s]+)$")

st.sidebar.markdown("<h2 style='color:blue;'>Project Info</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<b style='color:green;'>Global Seismic Trends Dashboard</b>", unsafe_allow_html=True)
st.sidebar.markdown("<b style='color:purple;'>Built with Python, Pandas, SQL, Streamlit</b>", unsafe_allow_html=True)
st.sidebar.markdown("<b style='color:red;'>Data Source: USGS Earthquake API</b>", unsafe_allow_html=True)
st.sidebar.markdown("<b style='color:orange;'>Developed by: Balaji Venkatesan</b>", unsafe_allow_html=True)


st.header("📊 Year & Country Analysis")

year = st.selectbox("Select Year", sorted(df["year"].unique()))
country = st.selectbox("Select Country", sorted(df["country"].dropna().unique()))

filtered = df[(df["year"] == year) & (df["country"] == country)]

if filtered.empty:
    st.warning("No earthquake records found for this selection.")
else:
    st.subheader("Earthquake Locations")
    st.map(filtered[["latitude", "longitude"]])

    st.subheader("Monthly Earthquake Count")
    st.bar_chart(filtered["month"].value_counts().sort_index())

    st.subheader("Average Magnitude by Month")
    st.line_chart(filtered.groupby("month")["mag"].mean())

    st.subheader("Depth vs Magnitude")
    st.scatter_chart(filtered[["depth_km", "mag"]])

from sqlalchemy import create_engine

# Step 1: MySQL connection
engine = create_engine("mysql+pymysql://root:12345@localhost/earthquakes")

# Step 2: Queries dictionary (30 queries)
queries = {
    # Time Analysis
    "1. Year with most earthquakes": """
        SELECT year, COUNT(*) AS total 
        FROM earthquake_data 
        GROUP BY year 
        ORDER BY total DESC LIMIT 1;
    """,
    "2. Month with highest count": """
        SELECT month, COUNT(*) AS total 
        FROM earthquake_data 
        GROUP BY month 
        ORDER BY total DESC LIMIT 1;
    """,
    "3. Day of week trend": """
        SELECT day_of_week, COUNT(*) AS total 
        FROM earthquake_data 
        GROUP BY day_of_week 
        ORDER BY total DESC;
    """,
    "4. Average magnitude per year": """
        SELECT year, AVG(mag) AS avg_mag 
        FROM earthquake_data 
        GROUP BY year 
        ORDER BY year;
    """,
    "5. Average depth per year": """
        SELECT year, AVG(depth_km) AS avg_depth 
        FROM earthquake_data 
        GROUP BY year 
        ORDER BY year;
    """,

    # Magnitude Analysis
    "6. Strongest earthquake each year": """
        SELECT year, MAX(mag) AS max_mag 
        FROM earthquake_data 
        GROUP BY year 
        ORDER BY year;
    """,
    "7. Destructive earthquakes per year": """
        SELECT year, COUNT(*) AS destructive_count 
        FROM earthquake_data 
        WHERE strength_flag='Destructive' 
        GROUP BY year;
    """,
    "8. Normal earthquakes per year": """
        SELECT year, COUNT(*) AS normal_count 
        FROM earthquake_data 
        WHERE strength_flag='Normal' 
        GROUP BY year;
    """,
    "9. Top 5 countries with highest average magnitude": """
        SELECT country, AVG(mag) AS avg_mag 
        FROM earthquake_data 
        GROUP BY country 
        ORDER BY avg_mag DESC LIMIT 5;
    """,
    "10. Top 5 countries with most destructive earthquakes": """
        SELECT country, COUNT(*) AS destructive_count 
        FROM earthquake_data 
        WHERE strength_flag='Destructive' 
        GROUP BY country 
        ORDER BY destructive_count DESC LIMIT 5;
    """,

    # Depth Analysis
    "11. Shallow vs Deep count": """
        SELECT depth_flag, COUNT(*) AS total 
        FROM earthquake_data 
        GROUP BY depth_flag;
    """,
    "12. Average depth by country": """
        SELECT country, AVG(depth_km) AS avg_depth 
        FROM earthquake_data 
        GROUP BY country 
        ORDER BY avg_depth DESC;
    """,
    "13. Deepest earthquake per year": """
        SELECT year, MAX(depth_km) AS max_depth 
        FROM earthquake_data 
        GROUP BY year;
    """,
    "14. Shallowest earthquake per year": """
        SELECT year, MIN(depth_km) AS min_depth 
        FROM earthquake_data 
        GROUP BY year;
    """,
    "15. Depth vs Magnitude correlation (avg)": """
        SELECT depth_flag, AVG(mag) AS avg_mag 
        FROM earthquake_data 
        GROUP BY depth_flag;
    """,

    # Country Analysis
    "16. Top 10 countries with most earthquakes": """
        SELECT country, COUNT(*) AS total 
        FROM earthquake_data 
        GROUP BY country 
        ORDER BY total DESC LIMIT 10;
    """,
    "17. Country with highest average magnitude": """
        SELECT country, AVG(mag) AS avg_mag 
        FROM earthquake_data 
        GROUP BY country 
        ORDER BY avg_mag DESC LIMIT 1;
    """,
    "18. Country with deepest average depth": """
        SELECT country, AVG(depth_km) AS avg_depth 
        FROM earthquake_data 
        GROUP BY country 
        ORDER BY avg_depth DESC LIMIT 1;
    """,
    "19. Country with most destructive earthquakes": """
        SELECT country, COUNT(*) AS destructive_count 
        FROM earthquake_data 
        WHERE strength_flag='Destructive' 
        GROUP BY country 
        ORDER BY destructive_count DESC LIMIT 1;
    """,
    "20. Country with most shallow earthquakes": """
        SELECT country, COUNT(*) AS shallow_count 
        FROM earthquake_data 
        WHERE depth_flag='Shallow' 
        GROUP BY country 
        ORDER BY shallow_count DESC LIMIT 1;
    """,

    # Tsunami & Signal Analysis
    "21. Tsunami events count per year": """
        SELECT year, SUM(tsunami) AS tsunami_events 
        FROM earthquake_data 
        GROUP BY year;
    """,
    "22. Average signal strength per year": """
        SELECT year, AVG(sig) AS avg_signal 
        FROM earthquake_data 
        GROUP BY year;
    """,
    "23. Top 5 countries with tsunami events": """
        SELECT country, SUM(tsunami) AS tsunami_events 
        FROM earthquake_data 
        GROUP BY country 
        ORDER BY tsunami_events DESC LIMIT 5;
    """,
    "24. Tsunami vs Non-tsunami count": """
        SELECT tsunami, COUNT(*) AS total 
        FROM earthquake_data 
        GROUP BY tsunami;
    """,
    "25. Highest signal strength earthquake": """
        SELECT id, year, country, mag, sig 
        FROM earthquake_data 
        ORDER BY sig DESC LIMIT 1;
    """,

    # Miscellaneous Analysis
    "26. Average RMS per year": """
        SELECT year, AVG(rms) AS avg_rms 
        FROM earthquake_data 
        GROUP BY year;
    """,
    "27. Average GAP per year": """
        SELECT year, AVG(gap) AS avg_gap 
        FROM earthquake_data 
        GROUP BY year;
    """,
    "28. Earthquakes per month (all years)": """
        SELECT month, COUNT(*) AS total 
        FROM earthquake_data 
        GROUP BY month 
        ORDER BY month;
    """,
    "29. Earthquakes per weekday (all years)": """
        SELECT day_of_week, COUNT(*) AS total 
        FROM earthquake_data 
        GROUP BY day_of_week 
        ORDER BY total DESC;
    """,
    "30. Top 5 earthquakes by magnitude": """
        SELECT id, year, country, mag, depth_km, place 
        FROM earthquake_data 
        ORDER BY mag DESC LIMIT 5;
    """
}

# Step 3: Streamlit UI

st.header("🗂️ SQL Query Explorer")  

task = st.selectbox("Select Query", list(queries.keys()))

if st.button("Run Query"):
    query = queries[task]
    df_result = pd.read_sql(query, engine)
    st.subheader(f"Results for: {task}")
    st.dataframe(df_result, width='stretch')
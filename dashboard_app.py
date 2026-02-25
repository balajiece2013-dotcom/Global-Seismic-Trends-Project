import streamlit as st  # Streamlit library for building interactive web apps
import pandas as pd  # Pandas for data manipulation

# -------------------------------
# 📂 Load Cleaned Dataset
# -------------------------------

# Load cleaned earthquake dataset generated after preprocessing
df = pd.read_csv("earthquake_clean.csv")

# Convert 'time' column to datetime format for time-based analysis
df["time"] = pd.to_datetime(df["time"], errors="coerce")

# Extract year and month for filtering & visualization
df["year"] = df["time"].dt.year.astype(int)
df["month"] = df["time"].dt.month

# Extract country from 'place' column using regex
df["country"] = df["place"].str.extract(r",\s*([A-Za-z\s]+)$")

# -------------------------------
# 📌 Sidebar Project Information
# -------------------------------

# Display styled project info in sidebar
st.sidebar.markdown("<h2 style='color:blue;'>Project Info</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<b style='color:green;'>Global Seismic Trends Dashboard</b>", unsafe_allow_html=True)
st.sidebar.markdown("<b style='color:purple;'>Built with Python, Pandas, SQL, Streamlit</b>", unsafe_allow_html=True)
st.sidebar.markdown("<b style='color:red;'>Data Source: USGS Earthquake API</b>", unsafe_allow_html=True)
st.sidebar.markdown("<b style='color:orange;'>Developed by: Balaji Venkatesan</b>", unsafe_allow_html=True)

# GitHub repository link
st.sidebar.markdown("[View on GitHub](https://github.com/balajiece2013-dotcom/Global-Seismic-Trends-Project)")

# -------------------------------
# 📊 Year & Country Filtering Section
# -------------------------------

st.header("📊 Year & Country Analysis")

# Dropdown selection for year
year = st.selectbox("Select Year", sorted(df["year"].unique()))

# Dropdown selection for country
country = st.selectbox("Select Country", sorted(df["country"].dropna().unique()))

# Filter dataset based on selected year and country
filtered = df[(df["year"] == year) & (df["country"] == country)]

# If no data found
if filtered.empty:
    st.warning("No earthquake records found for this selection.")
else:
    # Display earthquake locations on map
    st.subheader("Earthquake Locations")
    st.map(filtered[["latitude", "longitude"]])

    # Monthly earthquake frequency (Bar chart)
    st.subheader("Monthly Earthquake Count")
    st.bar_chart(filtered["month"].value_counts().sort_index())

    # Average magnitude trend per month (Line chart)
    st.subheader("Average Magnitude by Month")
    st.line_chart(filtered.groupby("month")["mag"].mean())

    # Depth vs Magnitude relationship (Scatter plot)
    st.subheader("Depth vs Magnitude")
    st.scatter_chart(filtered[["depth_km", "mag"]])

# -------------------------------
# 🗄️ SQL Integration Section
# -------------------------------

from sqlalchemy import create_engine  # Used to connect Python with MySQL

# Establish MySQL database connection
# mysql+pymysql → database driver
# root → username
# Balaji%4012345 → encoded password (@ → %40)
# earthquakes → database name
engine = create_engine("mysql+pymysql://root:Balaji%4012345@localhost/earthquakes")

# -------------------------------
# 📑 SQL Query Dictionary (30 Analytical Queries)
# -------------------------------

# Dictionary storing predefined analytical SQL queries
# These queries perform time, magnitude, depth, country, tsunami, and signal analysis
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

# -------------------------------
# 🖥️ SQL Query Explorer UI
# -------------------------------

st.header("🗂️ SQL Query Explorer")  

# Dropdown to select query from dictionary
task = st.selectbox("Select Query", list(queries.keys()))

# Execute selected query when button is clicked
if st.button("Run Query"):
    query = queries[task]
    try:
        # Execute SQL query and load result into DataFrame
        df_result = pd.read_sql(query, engine)

        if df_result.empty:
            st.warning("No results found for this query.")
        else:
            # Display query result
            st.subheader(f"Results for: {task}")
            st.write(f"Returned {len(df_result)} rows")
            st.dataframe(df_result, use_container_width=True)

            # Expandable section to display actual SQL query
            with st.expander("Show SQL Query"):
                st.code(query, language="sql")

            # Allow user to download query results as CSV
            csv = df_result.to_csv(index=False).encode('utf-8')
            st.download_button("Download Results as CSV", csv, "query_results.csv", "text/csv")

            # Quick visualization if at least 2 numeric columns exist
            numeric_cols = df_result.select_dtypes(include='number').columns
            if len(numeric_cols) >= 2:
                st.subheader("Quick Visualization")
                st.line_chart(df_result[numeric_cols])

    except Exception as e:
        # Error handling for SQL execution
        st.error(f"Error running query: {e}")
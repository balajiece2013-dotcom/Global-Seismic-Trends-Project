-- Global Seismic Trends – Project Report

Introduction
In this project, we collected earthquake data from the USGS API for the past 5 years (2020–2025).
We cleaned the data, stored it in a MySQL database, ran SQL queries, and built a Streamlit dashboard.
The dataset contains 32 columns (26 original + 6 derived).

Key Findings
Time Analysis
The year with the highest number of earthquakes → 2021

The month with the highest number of earthquakes → March

The weekday with the most earthquakes → Friday

Magnitude Analysis
Top 10 strongest earthquakes occurred mostly in Japan, Chile, and Indonesia

Average magnitude was highest in 2022

Destructive earthquakes (magnitude ≥ 7.5) were concentrated in the Pacific Ring of Fire

Depth Analysis
Shallow earthquakes (<50 km) were more destructive

Deep earthquakes (>50 km) had moderate magnitudes

Tsunami Analysis
Tsunami-related earthquakes were most common in Japan, Indonesia, and Chile

Tsunami earthquakes had higher average magnitudes compared to non-tsunami events

Country Trends
Country with the most earthquakes → Japan

Top 5 countries by average magnitude → Japan, Chile, Indonesia, Mexico, Turkey

Countries with the most destructive earthquakes → Japan and Chile

Recommendations
Governments should focus disaster planning on shallow, destructive earthquakes.

Insurance companies can use magnitude and depth trends for risk assessment.

Researchers should study tsunami-linked earthquakes for coastal safety.

Public awareness campaigns should encourage earthquake preparedness drills.

Conclusion
This project successfully completed the full workflow:

Fetching data from API

Cleaning and transforming data

Inserting into MySQL database

Running 30 SQL queries

Building a Streamlit dashboard

Writing documentation

The project requirements are fully satisfied
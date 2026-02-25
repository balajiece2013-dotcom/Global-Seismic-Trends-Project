🌍 Global Seismic Trends Dashboard
Project Report
1️⃣ Introduction

This project focuses on analyzing global earthquake patterns over the past five years (2020–2025) using real-time seismic data obtained from the USGS API.

The complete data pipeline includes:

Fetching earthquake data from API

Data cleaning and preprocessing using Python

Handling missing values using statistical imputation

Creating derived analytical features

Storing processed data into a MySQL database

Executing 30 analytical SQL queries

Developing an interactive Streamlit dashboard

The final dataset consists of 32 columns:

26 original attributes from the API

6 derived analytical columns (year, month, depth category, magnitude category, etc.)

This project demonstrates end-to-end data engineering, SQL analytics, and dashboard visualization skills.

2️⃣ Key Findings
📅 Time-Based Analysis

The year with the highest number of recorded earthquakes was 2021.

The month with the highest earthquake occurrence was March.

Friday recorded the highest number of earthquakes among all weekdays.

These results indicate temporal patterns in seismic activity that can support time-based trend analysis.

📊 Magnitude Analysis

The top 10 strongest earthquakes were primarily recorded in Japan, Chile, and Indonesia.

The highest average earthquake magnitude was observed in 2022.

Most destructive earthquakes (magnitude ≥ 7.5) were concentrated around the Pacific Ring of Fire region.

This confirms that tectonically active regions experience higher seismic intensity.

🌊 Depth Analysis

Shallow earthquakes (<50 km) were found to be more destructive.

Deep earthquakes (>50 km) generally showed moderate magnitudes.

Shallow earthquakes cause stronger surface shaking, leading to greater structural damage.

🌊 Tsunami Analysis

Tsunami-triggering earthquakes were most common in Japan, Indonesia, and Chile.

Earthquakes associated with tsunamis had a higher average magnitude compared to non-tsunami earthquakes.

This highlights the strong relationship between high-magnitude undersea earthquakes and tsunami risk.

🌍 Country-Based Trends

The country with the highest number of recorded earthquakes was Japan.

Top 5 countries based on average magnitude:

Japan

Chile

Indonesia

Mexico

Turkey

Countries with the highest number of destructive earthquakes:

Japan

Chile

These findings emphasize high-risk seismic zones globally.

3️⃣ Recommendations

Based on the analysis, the following recommendations are proposed:

Governments should prioritize disaster preparedness strategies for shallow, high-magnitude earthquakes.

Insurance companies can leverage depth and magnitude trends for better risk modeling and premium estimation.

Coastal safety authorities should focus on monitoring tsunami-linked seismic events.

Public awareness programs should promote earthquake preparedness drills and emergency response training.

4️⃣ Conclusion

This project successfully implemented a complete end-to-end data workflow:

Data collection from API

Data cleaning and feature engineering

Secure MySQL database integration

Execution of 30 analytical SQL queries

Interactive Streamlit dashboard development

Comprehensive documentation

All project objectives and technical requirements have been fully satisfied.

The project is finalized and ready for GitHub submission and evaluation.

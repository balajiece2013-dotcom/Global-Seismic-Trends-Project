-- Time Analysis
-- 1. Year with most earthquakes
SELECT year, COUNT(*) AS total FROM earthquake_data GROUP BY year ORDER BY total DESC LIMIT 1;

-- 2. Month with highest count
SELECT month, COUNT(*) AS total FROM earthquake_data GROUP BY month ORDER BY total DESC LIMIT 1;

-- 3. Day of week trend
SELECT day_of_week, COUNT(*) AS total FROM earthquake_data GROUP BY day_of_week ORDER BY total DESC;

-- 4. Yearly growth in earthquake count
SELECT year, COUNT(*) AS total,
       LAG(COUNT(*)) OVER (ORDER BY year) AS prev_year,
       COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY year) AS growth
FROM earthquake_data GROUP BY year ORDER BY year;



-- Magnitude Analysis
-- 5. Top 10 strongest earthquakes
SELECT place, mag, time FROM earthquake_data ORDER BY mag DESC LIMIT 10;

-- 6. Average magnitude per year
SELECT year, AVG(mag) FROM earthquake_data GROUP BY year;

-- 7. Average magnitude per magType
SELECT magType, AVG(mag) FROM earthquake_data GROUP BY magType;

-- 8. Destructive earthquakes (mag >= 7.5)
SELECT place, mag, year FROM earthquake_data WHERE mag >= 7.5;


-- Depth Analysis
-- 9. Shallow vs Deep count
SELECT depth_flag, COUNT(*) FROM earthquake_data GROUP BY depth_flag;

-- 10. Average magnitude by depth_flag
SELECT depth_flag, AVG(mag) FROM earthquake_data GROUP BY depth_flag;

-- 11. Shallow destructive earthquakes
SELECT place, mag, depth_km FROM earthquake_data WHERE depth_km < 50 AND mag > 7.5;

-- 12. Deep earthquakes with mag > 6
SELECT place, mag, depth_km FROM earthquake_data WHERE depth_km >= 50 AND mag > 6;


-- Tsunami Analysis
-- 13. Tsunami vs Non-Tsunami count
SELECT tsunami, COUNT(*) FROM earthquake_data GROUP BY tsunami;

-- 14. Tsunami vs Non-Tsunami average magnitude
SELECT tsunami, AVG(mag) FROM earthquake_data GROUP BY tsunami;

-- 15. Tsunami events by country
SELECT country, COUNT(*) FROM earthquake_data WHERE tsunami=1 GROUP BY country ORDER BY COUNT(*) DESC;

-- 16. Strongest tsunami event
SELECT place, mag, time FROM earthquake_data WHERE tsunami=1 ORDER BY mag DESC LIMIT 1;


-- Country Trends
-- 17. Country with most earthquakes
SELECT country, COUNT(*) AS total FROM earthquake_data GROUP BY country ORDER BY total DESC LIMIT 1;

-- 18. Top 5 countries by average magnitude
SELECT country, AVG(mag) AS avg_mag FROM earthquake_data GROUP BY country ORDER BY avg_mag DESC LIMIT 5;

-- 19. Country-wise shallow vs deep
SELECT country, depth_flag, COUNT(*) FROM earthquake_data GROUP BY country, depth_flag;

-- 20. Country-wise destructive earthquakes
SELECT country, COUNT(*) FROM earthquake_data WHERE strength_flag='Destructive' GROUP BY country ORDER BY COUNT(*) DESC;


-- Advanced Analysis
-- 21. Yearly average depth
SELECT year, AVG(depth_km) FROM earthquake_data GROUP BY year;

-- 22. Magnitude distribution per year
SELECT year, magType, AVG(mag) FROM earthquake_data GROUP BY year, magType;

-- 23. Top 3 years with highest average magnitude
SELECT year, AVG(mag) AS avg_mag FROM earthquake_data GROUP BY year ORDER BY avg_mag DESC LIMIT 3;

-- 24. Earthquakes with missing country info
SELECT * FROM earthquake_data WHERE country IS NULL;

-- 25. Most frequent magType
SELECT magType, COUNT(*) FROM earthquake_data GROUP BY magType ORDER BY COUNT(*) DESC LIMIT 1;

-- 26. Strongest earthquake per year
SELECT year, MAX(mag) FROM earthquake_data GROUP BY year;


-- Extra Queries
-- 27. Average magnitude per month
SELECT month, AVG(mag) FROM earthquake_data GROUP BY month;

-- 28. Top 5 places with most earthquakes
SELECT place, COUNT(*) FROM earthquake_data GROUP BY place ORDER BY COUNT(*) DESC LIMIT 5;

-- 29. Average magnitude per country per year
SELECT country, year, AVG(mag) FROM earthquake_data GROUP BY country, year;

-- 30. Year with most destructive earthquakes
SELECT year, COUNT(*) FROM earthquake_data WHERE strength_flag='Destructive' GROUP BY year ORDER BY COUNT(*) DESC LIMIT 1;

import requests
import psycopg2
from datetime import date, timedelta

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="smart_retail",
    user="postgres",
    password="jayesh"
)
cur = conn.cursor()

# ✅ Ensure table exists
cur.execute("""
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city TEXT,
    temperature REAL,
    humidity REAL,
    wind_speed REAL,
    datetime DATE
);
""")
conn.commit()

# Coordinates for Thane
lat, lon = 19.2183, 72.9781

# Last 30 days (up to yesterday, since archive API has no future data)
end_date = date.today() - timedelta(days=1)
start_date = end_date - timedelta(days=30)


url = (
    f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}"
    f"&start_date={start_date}&end_date={end_date}"
    f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
)

print("Fetching data from:", url)
response = requests.get(url)
data = response.json()

# Debug: show response keys
print("API Response Keys:", data.keys())

# Insert loop
for d, tmax, tmin, precip in zip(
    data["daily"]["time"],
    data["daily"]["temperature_2m_max"],
    data["daily"]["temperature_2m_min"],
    data["daily"]["precipitation_sum"]
):
    print(d, tmax, tmin, precip)  # debug print

    if tmax is None or tmin is None:
        print(f"Skipping {d} due to missing temperature data.")
        continue

    avg_temp = (tmax + tmin) / 2

    cur.execute("""
        INSERT INTO weather_data (city, temperature, humidity, wind_speed, datetime)
        VALUES (%s, %s, %s, %s, %s)
    """, ("Thane", avg_temp, precip, None, d))

conn.commit()
cur.close()
conn.close()

print("✅ Data inserted successfully into weather_data")

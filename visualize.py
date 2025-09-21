import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="smart_retail",
    user="postgres",
    password="jayesh"
)

# Fetch last 30 days for Thane
query = """
SELECT datetime, temperature, humidity
FROM weather_data
WHERE city = 'Thane'
ORDER BY datetime;
"""
df = pd.read_sql(query, conn)
conn.close()

print("Data loaded from DB:")
print(df.head())

# Plot temperature trend
plt.figure(figsize=(10,5))
plt.plot(df['datetime'], df['temperature'], marker='o', label='Avg Temp (°C)')
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Thane - Last 30 Days Temperature Trend")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot precipitation trend (stored in humidity column as per insert logic)
plt.figure(figsize=(10,5))
plt.bar(df['datetime'], df['humidity'])
plt.xlabel("Date")
plt.ylabel("Precipitation (mm)")
plt.title("Thane - Last 30 Days Precipitation")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

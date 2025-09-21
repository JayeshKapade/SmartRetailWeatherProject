import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import timedelta

# Connect to DB
conn = psycopg2.connect(
    host="localhost",
    dbname="smart_retail",
    user="postgres",
    password="jayesh"
)

query = """
SELECT datetime, temperature
FROM weather_data
WHERE city = 'Thane'
ORDER BY datetime;
"""
df = pd.read_sql(query, conn)
conn.close()

print("Data loaded from DB:")
print(df.tail())

# Ensure datetime is proper pandas datetime
df['datetime'] = pd.to_datetime(df['datetime'])

# Use only the date part (still keep as datetime64[ns])
df['date_only'] = df['datetime'].dt.normalize()

# Create numeric feature for regression
df['day_num'] = (df['date_only'] - df['date_only'].min()).dt.days

X = df[['day_num']]
y = df['temperature']

# Train model
model = LinearRegression()
model.fit(X, y)

# Get last historical date
last_date = df['date_only'].max()
print("Last historical date:", last_date)

# Forecast next 7 calendar days
future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=7)
future_day_nums = (future_dates - df['date_only'].min()).days.values.reshape(-1, 1)

preds = model.predict(future_day_nums)

# Combine into DataFrame
forecast_df = pd.DataFrame({
    "date": future_dates,
    "predicted_temp": preds
})

print("\nNext 7 days predicted temperatures:")
print(forecast_df)

# Plot actual vs predicted
plt.figure(figsize=(10,5))
plt.plot(df['datetime'], df['temperature'], marker='o', label='Actual Temp (°C)')
plt.plot(forecast_df['date'], forecast_df['predicted_temp'], marker='x', linestyle='--', color='red', label='Predicted Temp (°C)')
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Thane - Temperature Forecast (Next 7 Days)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

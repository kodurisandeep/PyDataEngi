import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Simulate daily temperature data
np.random.seed(42)
date_range = pd.date_range(start='2023-01-01', end='2023-03-31', freq='D')
temps = (25 + np.random.randn(len(date_range)) * 5).round(2)  # Mean temp ~25 C with noise

df = pd.DataFrame({'date': date_range, 'temperature': temps})
df.set_index('date', inplace=True)


# Step 2: Resample - weekly average and monthly average
df['weekly_avg'] = df['temperature'].resample('W').mean().round(2)
df['monthly_avg'] = df['temperature'].resample('ME').mean().round(2)

# Step 3: Rolling averages - 7-day and 14-day windows
df['rolling_7d'] = df['temperature'].rolling(window=7).mean().round(2)
df['rolling_14d'] = df['temperature'].rolling(window=14).mean().round(2)


# Step 4: Plot it all
plt.figure(figsize=(14, 6))
plt.plot(df.index, df['temperature'], label='Daily Temp', alpha=0.4)
plt.plot(df.index, df['rolling_7d'], label='7-Day Rolling Avg', linewidth=2)
plt.plot(df.index, df['rolling_14d'], label='14-Day Rolling Avg', linewidth=2, linestyle='--')
plt.title('Time-Series: Temperature with Rolling Averages')
plt.xlabel('Date')
plt.ylabel('Temperature (C)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
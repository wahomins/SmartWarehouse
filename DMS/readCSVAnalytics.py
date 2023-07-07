import pandas as pd
import matplotlib.pyplot as plt

# Read data from the CSV file
df = pd.read_csv('sensor_data.csv')

# Clean data and remove invalid readings
df = df.astype({'Smoke': float, 'CO': float, 'LPG': float})
df = df[(df['Smoke'] >= 0) & (df['CO'] >= 0) & (df['LPG'] >= 0)]


# Convert Timestamp column to datetime type
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Calculate daily averages
df_daily_avg = df.groupby(df['Timestamp'].dt.date).mean()

# Create subplots within a single figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Plot the original sensor readings
ax1.plot(df['Timestamp'], df['Smoke'], label='Smoke')
ax1.plot(df['Timestamp'], df['CO'], label='CO')
ax1.plot(df['Timestamp'], df['LPG'], label='LPG')
ax1.set_xlabel('Time')
ax1.set_ylabel('Readings')
ax1.set_title('Sensor Readings')
ax1.legend()

# Plot the daily average
ax2.plot(df_daily_avg.index, df_daily_avg['Smoke'], label='Daily Average (Smoke)')
ax2.plot(df_daily_avg.index, df_daily_avg['CO'], label='Daily Average (CO)')
ax2.plot(df_daily_avg.index, df_daily_avg['LPG'], label='Daily Average (LPG)')
ax2.set_xlabel('Date')
ax2.set_ylabel('Average Readings')
ax2.set_title('Daily Average Sensor Readings')
ax2.legend()

# Set the number of x-axis ticks and adjust their appearance
num_ticks = 10
x_ticks = plt.xticks(plt.xticks()[0][::len(df)//num_ticks])

plt.xticks(rotation=45)

# Calculate statistical properties
smoke_mean = df['Smoke'].mean()
co_mean = df['CO'].mean()
lpg_mean = df['LPG'].mean()

smoke_mode = df['Smoke'].mode().tolist()
co_mode = df['CO'].mode().tolist()
lpg_mode = df['LPG'].mode().tolist()

smoke_median = df['Smoke'].median()
co_median = df['CO'].median()
lpg_median = df['LPG'].median()

# Display statistical properties
props = {
    'Smoke': {'Mean': smoke_mean, 'Mode': smoke_mode, 'Median': smoke_median},
    'CO': {'Mean': co_mean, 'Mode': co_mode, 'Median': co_median},
    'LPG': {'Mean': lpg_mean, 'Mode': lpg_mode, 'Median': lpg_median}
}

for prop_name, prop_values in props.items():
    print(f"--- {prop_name} ---")
    for stat_name, stat_value in prop_values.items():
        print(f"{stat_name}: {stat_value}")

# Adjust the spacing between subplots
plt.tight_layout()

plt.show()

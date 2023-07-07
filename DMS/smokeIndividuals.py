import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib

# Read data from the CSV file
df = pd.read_csv('sensor_data.csv')

# Clean data and remove invalid readings
df = df.astype({'Smoke': float, 'CO': float, 'LPG': float})
df = df[(df['Smoke'] >= 0) & (df['CO'] >= 0) & (df['LPG'] >= 0)]

# Convert Timestamp column to datetime type
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Calculate daily averages
df_daily_avg = df.groupby(df['Timestamp'].dt.date).mean()

# Define threshold levels
smoke_threshold = 500
co_threshold = 10
lpg_threshold = 10

# Create Figure 1: Smoke readings
fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(df['Timestamp'], df['Smoke'], color='b', label='Smoke')
ax1.axhline(smoke_threshold, color='r', linestyle='--', label='Threshold')
ax1.set_xlabel('Time')
ax1.set_ylabel('Smoke (ppm)')
ax1.set_title('Smoke Readings')
ax1.legend()
ax1.xaxis.set_major_locator(ticker.AutoLocator())
ax1.tick_params(axis='x', rotation=45)

# Create Figure 2: CO readings
fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(df['Timestamp'], df['CO'], color='g', label='CO')
ax2.axhline(co_threshold, color='r', linestyle='--', label='Threshold')
ax2.set_xlabel('Time')
ax2.set_ylabel('CO (ppm)')
ax2.set_title('CO Readings')
ax2.legend()
ax2.xaxis.set_major_locator(ticker.AutoLocator())
ax2.tick_params(axis='x', rotation=45)

# Create Figure 3: LPG readings
fig3, ax3 = plt.subplots(figsize=(12, 6))
ax3.plot(df['Timestamp'], df['LPG'], color='m', label='LPG')
ax3.axhline(lpg_threshold, color='r', linestyle='--', label='Threshold')
ax3.set_xlabel('Time')
ax3.set_ylabel('LPG (ppm)')
ax3.set_title('LPG Readings')
ax3.legend()
ax3.xaxis.set_major_locator(ticker.AutoLocator())
ax3.tick_params(axis='x', rotation=45)

# Create Figure 4: Combined readings
fig4, ax4 = plt.subplots(figsize=(12, 6))

# Plot Smoke, CO, and LPG readings
ax4.plot(df['Timestamp'], df['Smoke'], color='b', label='Smoke')
ax4.plot(df['Timestamp'], df['CO'], color='g', label='CO')
ax4.plot(df['Timestamp'], df['LPG'], color='m', label='LPG')
ax4.set_xlabel('Time')
ax4.set_ylabel('Sensor Reading (ppm)')
ax4.set_title('Combined Readings')
ax4.legend()
ax4.xaxis.set_major_locator(ticker.AutoLocator())
ax4.tick_params(axis='x', rotation=45)

# Adjust the layout to prevent overlapping of x-axis labels (optional)
# fig.autofmt_xdate()

# Adjust the spacing between subplots in Figure 1
plt.tight_layout()

# Show the figures
plt.show()

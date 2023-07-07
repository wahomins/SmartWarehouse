import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
matplotlib.rcParams['axes.labelsize'] = 18

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

# # Create Figure 1: Readings against time
# fig1, axs1 = plt.subplots(2, 2, figsize=(12, 12))

# # Plot smoke readings
# axs1[0, 0].plot(df['Timestamp'], df['Smoke'], color='b', label='Smoke')
# axs1[0, 0].axhline(smoke_threshold, color='r', linestyle='--', label='Threshold')
# axs1[0, 0].set_ylabel('Smoke (ppm)')
# axs1[0, 0].set_title('Smoke Readings')
# axs1[0, 0].legend()
# axs1[0, 0].tick_params(axis='x', rotation=45)

# # Plot CO readings
# axs1[0, 1].plot(df['Timestamp'], df['CO'], color='g', label='CO')
# axs1[0, 1].axhline(co_threshold, color='r', linestyle='--', label='Threshold')
# axs1[0, 1].set_ylabel('CO (ppm)')
# axs1[0, 1].set_title('CO Readings')
# axs1[0, 1].legend()
# axs1[0, 1].tick_params(axis='x', rotation=45)

# # Plot LPG readings
# axs1[1, 0].plot(df['Timestamp'], df['LPG'], color='m', label='LPG')
# axs1[1, 0].axhline(lpg_threshold, color='r', linestyle='--', label='Threshold')
# axs1[1, 0].set_xlabel('Time')
# axs1[1, 0].set_ylabel('LPG (ppm)')
# axs1[1, 0].set_title('LPG Readings')
# axs1[1, 0].legend()
# axs1[1, 0].tick_params(axis='x', rotation=45)

# # Adjust the layout to prevent overlapping of x-axis labels (optional)
# fig1.autofmt_xdate()

# # Adjust the spacing between subplots in Figure 1
# plt.tight_layout()

# Create Figure 2: Daily averages
fig2, axs2 = plt.subplots(2, 2, figsize=(12, 12))

# Plot daily average smoke readings
axs2[0, 0].plot(df_daily_avg.index, df_daily_avg['Smoke'], color='b', label='Daily Average (Smoke)')
axs2[0, 0].axhline(smoke_threshold, color='r', linestyle='--', label='Threshold')
axs2[0, 0].set_ylabel('Smoke (ppm)')
axs2[0, 0].set_xlabel('Date')
axs2[0, 0].set_title('Daily Average Smoke Readings')
axs2[0, 0].legend()

# Plot daily average CO readings
axs2[0, 1].plot(df_daily_avg.index, df_daily_avg['CO'], color='g', label='Daily Average (CO)')
axs2[0, 1].axhline(co_threshold, color='r', linestyle='--', label='Threshold')
axs2[0, 1].set_ylabel('CO (ppm)')
axs2[0, 1].set_xlabel('Date')
axs2[0, 1].set_title('Daily Average CO Readings')
axs2[0, 1].legend()

# Plot daily average LPG readings
axs2[1, 0].plot(df_daily_avg.index, df_daily_avg['LPG'], color='m', label='Daily Average (LPG)')
axs2[1, 0].axhline(lpg_threshold, color='r', linestyle='--', label='Threshold')
axs2[1, 0].set_xlabel('Date')
axs2[1, 0].set_ylabel('LPG (ppm)')
axs2[1, 0].set_title('Daily Average LPG Readings')
axs2[1, 0].legend()

# Hide the fourth subplot
axs2[1, 1].axis('off')
# Rotate x-axis labels for better readability (optional)
for ax_row in axs2:
    for ax in ax_row:
        ax.tick_params(axis='x', rotation=45)

plt.show()

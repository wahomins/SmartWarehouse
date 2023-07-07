import os
import csv
import random
from datetime import datetime, timedelta

# Get the current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))
print("Current directory:", current_dir)

# Specify the file path
file_path = os.path.join(current_dir, 'sensor_data.csv')

# Define threshold levels
smoke_threshold = 500
co_threshold = 10
lpg_threshold = 10

# Generate random data for a week (7 days)
num_days = 7
data_points_per_day = int((24 * 60) / 10)  # Assuming data every 10 minutes
start_date = datetime.now() - timedelta(days=num_days)

# Generate and save random sensor data to a CSV file
with open(file_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Timestamp', 'Smoke', 'CO', 'LPG'])  # Header row

    lpg_spike_day = random.randint(1, 7)
    lpg_spike_count = 0
    smoke_co_spike_count = 0

    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        for _ in range(data_points_per_day):
            timestamp = current_date.strftime('%Y-%m-%d %H:%M:%S')

            if day == lpg_spike_day and lpg_spike_count < 2:
                # Generate isolated LPG spike
                lpg_spike_count += 1
                lpg = random.uniform(lpg_threshold * 2, lpg_threshold * 2)
                smoke = random.uniform(0, smoke_threshold * 2)
                co = random.uniform(0, co_threshold * 1.4)
            elif smoke_co_spike_count < 2:
                # Generate spikes of smoke and CO below thresholds
                smoke_co_spike_count += 1
                lpg = random.uniform(0, lpg_threshold * 0.2)
                smoke = random.uniform(0, smoke_threshold * 0.2)
                co = random.uniform(0, co_threshold * 0.1)
            else:
                # Generate normal readings
                lpg = random.uniform(0, lpg_threshold * 0.01)
                smoke = random.uniform(0, smoke_threshold * 0.01)
                co = random.uniform(0, co_threshold * 0.01)

            writer.writerow([timestamp, '{:.2f}'.format(smoke), '{:.2f}'.format(co), '{:.2f}'.format(lpg)])
            current_date += timedelta(minutes=10)

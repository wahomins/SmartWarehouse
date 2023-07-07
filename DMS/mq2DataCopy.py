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
smoke_threshold = 300
co_threshold = 10
lpg_threshold = 200

# Generate random data for a week (7 days)
num_days = 7
data_points_per_day = int((24 * 60) / 10)  # Assuming data every 10 minutes
start_date = datetime.now() - timedelta(days=num_days)

# Generate and save random sensor data to a CSV file
with open(file_path, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Timestamp', 'Smoke', 'CO', 'LPG'])  # Header row
    spike_days = random.sample(range(num_days), random.randint(1, 3))
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        is_spike_day = day in spike_days
        spike_count = 0
        is_spike_active = False
        for _ in range(data_points_per_day):
            timestamp = current_date.strftime('%Y-%m-%d %H:%M:%S')
            
            if is_spike_day and not is_spike_active and spike_count < 4:
                # Generate spikes below or above the thresholds
                is_spike_active = random.choice([True, False])
                if is_spike_active:
                    if spike_count == 0:
                        lpg = random.uniform(lpg_threshold, lpg_threshold * 2)
                    else:
                        lpg = random.uniform(0, lpg_threshold)
                    
                    smoke = random.uniform(smoke_threshold, smoke_threshold * 2)
                    co = random.uniform(smoke_threshold, smoke_threshold * 2)
                    
                    spike_count += 1
            else:
                # Generate normal readings near zero
                if is_spike_active:
                    lpg = random.uniform(0, lpg_threshold)
                    smoke = random.uniform(0, smoke_threshold)
                    co = random.uniform(0, smoke_threshold)
                else:
                    lpg = random.uniform(0, lpg_threshold * 0.2)
                    smoke = random.uniform(0, smoke_threshold * 0.2)
                    co = random.uniform(0, co_threshold * 0.2)
                
                is_spike_active = False
            
            writer.writerow([timestamp, smoke, co, lpg])
            current_date += timedelta(minutes=10)

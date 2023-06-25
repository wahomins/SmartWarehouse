import os

workers = 2
bind = '0.0.0.0:8000'

# Set the log directory and filename
log_dir = 'gunicornLogs'
log_file = os.path.join(log_dir, 'gunicorn.log')

# Create the log directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

# Gunicorn configuration options
errorlog = log_file
accesslog = log_file
loglevel = 'info'

# Enable automatic worker process restart on crash
max_requests = 1000
max_requests_jitter = 100

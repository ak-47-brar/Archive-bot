import os
import time
from pyrogram import Client
from os import mkdir
from datetime import datetime
import pytz

# Set timezone to UTC
os.environ['TZ'] = 'UTC'
time.tzset()

# Function to synchronize time offset
def sync_time_offset():
    utc_now = datetime.now(pytz.utc)
    local_tz = pytz.timezone('UTC')  # Assuming the server is running in UTC
    local_now = local_tz.localize(datetime.now())
    offset = (utc_now - local_now).total_seconds()
    return offset

# Adjust for the time difference
offset = sync_time_offset()

# Environment variables
app_id = int(os.environ.get("API_ID", 12345))
app_key = os.environ.get('API_HASH')
token = os.environ.get('BOT_TOKEN')

# Initialize the Pyrogram client
app = Client("zipBot", app_id, app_key, bot_token=token)

if __name__ == '__main__':
    try:
        mkdir("static")  # create static files folder
    except FileExistsError:
        pass

    # Retry mechanism for starting the app
    for attempt in range(5):
        try:
            adjusted_time = time.time() + offset
            app.run()
            break  # If successful, exit the loop
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(5)  # Wait before retrying

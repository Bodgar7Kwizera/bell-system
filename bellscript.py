import RPi.GPIO as GPIO
import time
from datetime import datetime
import json

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

# File to store the timetable
TIMETABLE_FILE = 'timetable.json'

# Load the timetable from the file
def load_timetable():
    try:
        with open(TIMETABLE_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to ring the bell
def ring_bell():
    GPIO.output(17, GPIO.HIGH)
    time.sleep(1)  # Ring the bell for 1 second
    GPIO.output(17, GPIO.LOW)

# Main loop
try:
    while True:
        current_day = datetime.now().strftime("%A")
        current_time = datetime.now().strftime("%H:%M")
        timetable = load_timetable()
        if current_day in timetable and current_time in timetable[current_day]:
            ring_bell()
            time.sleep(60)  # Wait for a minute to avoid multiple rings

        time.sleep(1)  # Check every second

except KeyboardInterrupt:
    GPIO.cleanup()

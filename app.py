from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# File to store the timetable
TIMETABLE_FILE = 'timetable.json'

# Initialize timetable with days of the week if the file does not exist
def initialize_timetable():
    initial_timetable = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": []
    }
    save_timetable(initial_timetable)
    return initial_timetable

# Load the timetable from the file
def load_timetable():
    if os.path.exists(TIMETABLE_FILE):
        with open(TIMETABLE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return initialize_timetable()
    else:
        return initialize_timetable()

# Save the timetable to the file
def save_timetable(timetable):
    with open(TIMETABLE_FILE, 'w') as f:
        json.dump(timetable, f)

@app.route('/')
def index():
    timetable = load_timetable()
    return render_template('index.html', timetable=timetable)

@app.route('/add', methods=['POST'])
def add_entry():
    day = request.form['day']
    time = request.form['time']
    timetable = load_timetable()
    if time not in timetable[day]:
        timetable[day].append(time)
        timetable[day].sort()
        save_timetable(timetable)
    return redirect(url_for('index'))

@app.route('/delete/<day>/<time>')
def delete_entry(day, time):
    timetable = load_timetable()
    if time in timetable[day]:
        timetable[day].remove(time)
        save_timetable(timetable)
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

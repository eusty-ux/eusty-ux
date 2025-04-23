%pip install ipywidgets
import ipywidgets as widgets
from IPython.display import display, clear_output
import datetime
import threading
import time

# List to store tasks
tasks = []

# Function to update the task display
def update_task_display():
    clear_output(wait=True)
    display(input_box, time_picker, add_button)
    for i, task in enumerate(tasks):
        task_box = widgets.HBox([
            widgets.Label(f"{task['description']} at {task['time']}"),
            task['progress'],
            task['complete_button']
        ])
        display(task_box)

# Function to celebrate completion
def celebrate():
    print("🎉 Task Completed! Great job! 🎉")

# Function to check alarms
def alarm_checker():
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        for task in tasks:
            if task['time'] == now and not task['notified']:
                print(f"⏰ Reminder: Time to start '{task['description']}'!")
                task['notified'] = True
        time.sleep(30)

# Start the alarm checker in the background
threading.Thread(target=alarm_checker, daemon=True).start()

# UI components
input_box = widgets.Text(placeholder='Enter your task...')
time_picker = widgets.Text(placeholder='HH:MM')
add_button = widgets.Button(description="Add Task")

# Add button click handler
def on_add_clicked(b):
    description = input_box.value
    time_slot = time_picker.value
    progress = widgets.FloatProgress(value=0, min=0, max=100)
    complete_button = widgets.Button(description="Complete")
    task = {
        'description': description,
        'time': time_slot,
        'progress': progress,
        'complete_button': complete_button,
        'notified': False
    }

    def on_complete_clicked(c):
        task['progress'].value = 100
        celebrate()

    complete_button.on_click(on_complete_clicked)
    tasks.append(task)
    input_box.value = ''
    time_picker.value = ''
    update_task_display()

add_button.on_click(on_add_clicked)

# Initial display
update_task_display()

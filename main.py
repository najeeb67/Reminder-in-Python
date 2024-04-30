import datetime
import time
import winsound
import re
import sqlite3

conn = sqlite3.connect('reminders.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS reminders
             (reminder_time TEXT, message TEXT)''')
conn.commit()

def add_reminder():
    reminder_input = input("Enter reminder time (YYYY-MM-DD HH:MM): ")
    try:
        match = re.match(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*(.*)$', reminder_input)
        if match:
            reminder_time_str = match.group(1)
            reminder_time = datetime.datetime.strptime(reminder_time_str, "%Y-%m-%d %H:%M")

            if reminder_time <= datetime.datetime.now():
                raise ValueError("Reminder time must be in the future.")
            message = match.group(2)
            c.execute("INSERT INTO reminders (reminder_time, message) VALUES (?, ?)", (reminder_time_str, message))
            conn.commit()
            print("Reminder added successfully.")
        else:
            raise ValueError("Invalid input format.")
    except ValueError as e:
        print(e)
        print("Invalid date/time format. Please enter in YYYY-MM-DD HH:MM format.")
    except sqlite3.Error as e:
        print("SQLite error:", e)

def check_reminders():
    current_time = datetime.datetime.now()
    c.execute("SELECT * FROM reminders")
    rows = c.fetchall()
    for row in rows:
        reminder_time_str, message = row
        reminder_time = datetime.datetime.strptime(reminder_time_str, "%Y-%m-%d %H:%M")
        if current_time >= reminder_time:
            print(f"Reminder: {message}")
            trigger_alarm()
            c.execute("DELETE FROM reminders WHERE reminder_time = ?", (reminder_time_str,))
            conn.commit()

def trigger_alarm():
    print("Alarm!")
    winsound.Beep(1000, 1000)

def main():
    while True:
        print("\n1. Add Reminder")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_reminder()
        elif choice == "2":
            break
        else:
            print("Invalid choice.")

        check_reminders()
        time.sleep(1)

if __name__ == "__main__":
    main()

conn.close()

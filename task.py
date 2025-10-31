import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry, Calendar
import sqlite3

# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ---------------- Add Task ----------------
def add_task():
    task = task_entry.get()
    date_val = date_entry.get()
    time = time_entry.get()

    if task and date_val and time:
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, date, time) VALUES (?, ?, ?)", (task, date_val, time))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Task added successfully!")
        task_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Error", "Please fill all fields.")

# ---------------- Show Tasks in Calendar ----------------
def show_tasks_calendar():
    cal_window = tk.Toplevel(root)
    cal_window.title("Task Calendar")
    cal_window.geometry("400x400")

    # Calendar widget
    cal = Calendar(cal_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=20, fill="both", expand=True)

    # Fetch tasks
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT task, date, time FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    # Highlight task dates
    for t in tasks:
        cal.calevent_create(t[1], f"{t[0]} @ {t[2]}", "task")

    cal.tag_config("task", background="green", foreground="white")

    # Task list below calendar
    task_list = tk.Listbox(cal_window, width=50, height=6)
    task_list.pack(pady=10)

    # Show selected day’s tasks
    def show_day_tasks(event):
        selected_date = cal.get_date()
        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("SELECT task, time FROM tasks WHERE date=?", (selected_date,))
        day_tasks = cursor.fetchall()
        conn.close()

        task_list.delete(0, tk.END)
        if day_tasks:
            for task in day_tasks:
                task_list.insert(tk.END, f"{task[0]} - {task[1]}")
        else:
            task_list.insert(tk.END, "No tasks for this day.")

    cal.bind("<<CalendarSelected>>", show_day_tasks)

# ---------------- Delete Task ----------------
def delete_task():
    def confirm_delete():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Error", "Please select a task to delete.")
            return
        index = selection[0]
        task_id = task_ids[index]

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Deleted", "Task deleted successfully!")
        delete_window.destroy()

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, date, time FROM tasks ORDER BY date, time")
    tasks = cursor.fetchall()
    conn.close()

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Task")

    if tasks:
        listbox = tk.Listbox(delete_window, width=50, height=10)
        listbox.pack(padx=10, pady=10)

        task_ids = []
        for t in tasks:
            listbox.insert(tk.END, f"{t[1]} - {t[2]} {t[3]}")
            task_ids.append(t[0])

        tk.Button(delete_window, text="Delete Selected Task", command=confirm_delete, bg="red", fg="white").pack(pady=5)
    else:
        tk.Label(delete_window, text="No tasks to delete").pack(pady=10)

# ---------------- Main GUI ----------------
root = tk.Tk()
root.title("Smart Task Reminder")
root.geometry("400x450")

tk.Label(root, text="Smart Task Reminder", font=10)

# Task input
tk.Label(root, text="Enter Task:").pack()
task_entry = tk.Entry(root, width=40)
task_entry.pack(pady=5)

# Calendar picker
tk.Label(root, text="Select Date:").pack()
date_entry = DateEntry(root, width=37, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
date_entry.pack(pady=5)

# Time input
tk.Label(root, text="Enter Time (HH:MM):").pack()
time_entry = tk.Entry(root, width=40)
time_entry.pack(pady=5)

# Buttons
tk.Button(root, text="Add Task", command=add_task, width=20, bg="green", fg="white").pack(pady=10)
tk.Button(root, text="Show Tasks Calendar", command=show_tasks_calendar, width=20, bg="blue", fg="white").pack(pady=10)
tk.Button(root, text="Delete Task", command=delete_task, width=20, bg="red", fg="white").pack(pady=10)

init_db()
root.mainloop()
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ====== DATABASE SETUP ======
connection = sqlite3.connect("hospital.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pid TEXT,
    name TEXT,
    age INTEGER,
    severity INTEGER,
    admission_date TEXT
)
""")
connection.commit()


# ====== FUNCTIONS ======

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM patients")
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)


def add_patient():
    pid = pid_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    severity = severity_entry.get()
    date = date_entry.get()

    if not pid or not name:
        messagebox.showerror("Error", "ID and Name are required")
        return

    cursor.execute("INSERT INTO patients (pid, name, age, severity, admission_date) VALUES (?, ?, ?, ?, ?)",
                   (pid, name, age, severity, date))
    connection.commit()
    refresh_table()
    messagebox.showinfo("Success", "Patient added successfully")
    clear_inputs()


def clear_inputs():
    pid_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    severity_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)


def delete_patient():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select a patient first")
        return

    pid = tree.item(selected[0])["values"][0]
    cursor.execute("DELETE FROM patients WHERE id=?", (pid,))
    connection.commit()
    refresh_table()
    messagebox.showinfo("Success", "Patient removed")


def search_patient():
    term = search_entry.get()
    for row in tree.get_children():
        tree.delete(row)
    query = "SELECT * FROM patients WHERE pid LIKE ? OR name LIKE ?"
    cursor.execute(query, (f"%{term}%", f"%{term}%"))
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)


def update_patient():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select a patient first")
        return

    pid = tree.item(selected[0])["values"][0]
    cursor.execute("UPDATE patients SET pid=?, name=?, age=?, severity=?, admission_date=? WHERE id=?",
                   (pid_entry.get(), name_entry.get(), age_entry.get(),
                    severity_entry.get(), date_entry.get(), pid))
    connection.commit()
    refresh_table()
    messagebox.showinfo("Success", "Patient updated")


# ====== GUI SETUP ======

root = tk.Tk()
root.title("Hospital Patient Management System")

# ---- Input area ----
frame = tk.LabelFrame(root, text="Patient Details")
frame.pack(fill="x", padx=10, pady=5)

tk.Label(frame, text="Patient ID").grid(row=0, column=0, padx=5, pady=5)
pid_entry = tk.Entry(frame)
pid_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Name").grid(row=0, column=2, padx=5, pady=5)
name_entry = tk.Entry(frame)
name_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame, text="Age").grid(row=1, column=0, padx=5, pady=5)
age_entry = tk.Entry(frame)
age_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Severity").grid(row=1, column=2, padx=5, pady=5)
severity_entry = tk.Entry(frame)
severity_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Label(frame, text="Admission Date").grid(row=2, column=0, padx=5, pady=5)
date_entry = tk.Entry(frame)
date_entry.grid(row=2, column=1, padx=5, pady=5)

# ---- Buttons ----
btn_frame = tk.Frame(root)
btn_frame.pack(fill="x", padx=10, pady=5)

tk.Button(btn_frame, text="Add Patient", command=add_patient).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update Patient", command=update_patient).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete Patient", command=delete_patient).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Clear Inputs", command=clear_inputs).grid(row=0, column=3, padx=5)

# ---- Search ----
search_frame = tk.LabelFrame(root, text="Search")
search_frame.pack(fill="x", padx=10, pady=5)

search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Search", command=search_patient).pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Refresh", command=refresh_table).pack(side=tk.LEFT, padx=5)

# ---- Patient display ----
tree = ttk.Treeview(root, columns=("id", "pid", "name", "age", "severity", "date"), show="headings")
tree.heading("id", text="DB ID")
tree.heading("pid", text="Patient ID")
tree.heading("name", text="Name")
tree.heading("age", text="Age")
tree.heading("severity", text="Severity")
tree.heading("date", text="Admission Date")
tree.pack(fill="both", expand=True, padx=10, pady=5)

refresh_table()
root.mainloop()

connection.close()

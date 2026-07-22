import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

FILE_NAME = "students.csv"


def create_file():
    """Create the CSV file with headers if it does not exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Age", "Branch", "Phone"])


def clear_fields():
    """Clear all input fields."""
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    branch_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)


def add_student():
    """Add a new student record."""
    student_id = id_entry.get().strip()
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    branch = branch_entry.get().strip()
    phone = phone_entry.get().strip()

    if not all([student_id, name, age, branch, phone]):
        messagebox.showwarning("Warning", "Please fill all fields.")
        return

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.DictReader(file)
        if any(row["ID"] == student_id for row in reader):
            messagebox.showerror("Error", "Student ID already exists.")
            return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([student_id, name, age, branch, phone])

    messagebox.showinfo("Success", "Student added successfully!")
    clear_fields()
    view_students()


def view_students():
    """Display all student records in the table."""
    for item in table.get_children():
        table.delete(item)

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            table.insert("", tk.END, values=row)


def search_student():
    """Search for a student by Student ID."""
    search_id = id_entry.get().strip()

    if not search_id:
        messagebox.showwarning("Warning", "Enter Student ID to search.")
        return

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)

        for row in reader:
            if row and row[0] == search_id:
                name_entry.delete(0, tk.END)
                name_entry.insert(0, row[1])
                age_entry.delete(0, tk.END)
                age_entry.insert(0, row[2])
                branch_entry.delete(0, tk.END)
                branch_entry.insert(0, row[3])
                phone_entry.delete(0, tk.END)
                phone_entry.insert(0, row[4])
                return

    messagebox.showerror("Error", "Student not found.")


def update_student():
    """Update an existing student record."""
    update_id = id_entry.get().strip()

    if not update_id:
        messagebox.showwarning("Warning", "Enter Student ID to update.")
        return

    students = []
    found = False

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader, ["ID", "Name", "Age", "Branch", "Phone"])

        for row in reader:
            if row and row[0] == update_id:
                row = [
                    update_id,
                    name_entry.get().strip(),
                    age_entry.get().strip(),
                    branch_entry.get().strip(),
                    phone_entry.get().strip()
                ]
                found = True
            students.append(row)

    if not found:
        messagebox.showerror("Error", "Student not found.")
        return

    if not all([name_entry.get().strip(), age_entry.get().strip(),
                branch_entry.get().strip(), phone_entry.get().strip()]):
        messagebox.showwarning("Warning", "Please fill all fields.")
        return

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(students)

    messagebox.showinfo("Success", "Student updated successfully!")
    clear_fields()
    view_students()


def delete_student():
    """Delete a student record by Student ID."""
    delete_id = id_entry.get().strip()

    if not delete_id:
        messagebox.showwarning("Warning", "Enter Student ID to delete.")
        return

    students = []
    found = False

    with open(FILE_NAME, "r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader, ["ID", "Name", "Age", "Branch", "Phone"])

        for row in reader:
            if row and row[0] == delete_id:
                found = True
            else:
                students.append(row)

    if not found:
        messagebox.showerror("Error", "Student not found.")
        return

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(students)

    messagebox.showinfo("Success", "Student deleted successfully!")
    clear_fields()
    view_students()


# Create the data file before starting the application.
create_file()

# Main application window.
root = tk.Tk()
root.title("Student Management System")
root.geometry("800x600")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 24, "bold")
)
title_label.pack(pady=20)

# Input fields.
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Student ID").grid(row=0, column=0, padx=10, pady=10)
id_entry = tk.Entry(input_frame)
id_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Name").grid(row=1, column=0, padx=10, pady=10)
name_entry = tk.Entry(input_frame)
name_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Age").grid(row=2, column=0, padx=10, pady=10)
age_entry = tk.Entry(input_frame)
age_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(input_frame, text="Branch").grid(row=0, column=2, padx=10, pady=10)
branch_entry = tk.Entry(input_frame)
branch_entry.grid(row=0, column=3, padx=10, pady=10)

tk.Label(input_frame, text="Phone").grid(row=1, column=2, padx=10, pady=10)
phone_entry = tk.Entry(input_frame)
phone_entry.grid(row=1, column=3, padx=10, pady=10)

# Buttons.
button_frame = tk.Frame(root)
button_frame.pack(pady=15)

tk.Button(button_frame, text="Add Student", width=15, command=add_student).grid(
    row=0, column=0, padx=5
)
tk.Button(button_frame, text="Search", width=15, command=search_student).grid(
    row=0, column=1, padx=5
)
tk.Button(button_frame, text="Update", width=15, command=update_student).grid(
    row=0, column=2, padx=5
)
tk.Button(button_frame, text="Delete", width=15, command=delete_student).grid(
    row=0, column=3, padx=5
)
tk.Button(button_frame, text="Clear", width=15, command=clear_fields).grid(
    row=0, column=4, padx=5
)

# Student table.
columns = ("ID", "Name", "Age", "Branch", "Phone")
table = ttk.Treeview(root, columns=columns, show="headings")

for column in columns:
    table.heading(column, text=column)
    table.column(column, width=140)

table.pack(pady=20)

# Load existing records.
view_students()

# Start the application.
root.mainloop()

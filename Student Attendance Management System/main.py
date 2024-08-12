import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import csv
from datetime import datetime

# Database connection
def connect_db():
    return sqlite3.connect('attendance.db')

# Add a new student
def add_student(name, roll_number):
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO students (name, roll_number) VALUES (?, ?)', (name, roll_number))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists")
    conn.close()

# Edit student information
def edit_student(student_id, name, roll_number):
    conn = connect_db()
    c = conn.cursor()
    c.execute('UPDATE students SET name = ?, roll_number = ? WHERE id = ?', (name, roll_number, student_id))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student information updated successfully")

# Delete a student
def delete_student(student_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student deleted successfully")

# Search for a student by roll number
def search_student(roll_number):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT * FROM students WHERE roll_number = ?', (roll_number,))
    student = c.fetchone()
    conn.close()
    return student

# Mark attendance
def mark_attendance(roll_number, status):
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT id FROM students WHERE roll_number = ?', (roll_number,))
    student_id = c.fetchone()
    if student_id:
        c.execute('INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)', (student_id[0], datetime.now().date(), status))
        conn.commit()
        messagebox.showinfo("Success", "Attendance marked successfully")
    else:
        messagebox.showerror("Error", "Roll number not found")
    conn.close()

# View attendance records
def view_attendance(order_by='date'):
    conn = connect_db()
    c = conn.cursor()
    query = f'''
        SELECT students.name, students.roll_number, attendance.date, attendance.status 
        FROM attendance 
        JOIN students ON attendance.student_id = students.id
        ORDER BY {order_by}
    '''
    c.execute(query)
    records = c.fetchall()
    conn.close()
    return records

# Filter attendance by date
def filter_attendance_by_date(date):
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        SELECT students.name, students.roll_number, attendance.date, attendance.status 
        FROM attendance 
        JOIN students ON attendance.student_id = students.id
        WHERE attendance.date = ?
    ''', (date,))
    records = c.fetchall()
    conn.close()
    return records

# Export attendance to CSV
def export_to_csv(records):
    with open('attendance_records.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Roll Number', 'Date', 'Status'])
        writer.writerows(records)
    messagebox.showinfo("Success", "Records exported to attendance_records.csv")

# Main application window
class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance Management System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Add Student Section
        self.add_student_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.add_student_frame.pack(pady=20)
        self.name_label = tk.Label(self.add_student_frame, text="Name:", bg="#f0f0f0")
        self.name_label.grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.add_student_frame)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.roll_label = tk.Label(self.add_student_frame, text="Roll Number:", bg="#f0f0f0")
        self.roll_label.grid(row=1, column=0, padx=10, pady=5)
        self.roll_entry = tk.Entry(self.add_student_frame)
        self.roll_entry.grid(row=1, column=1, padx=10, pady=5)
        self.add_button = tk.Button(self.add_student_frame, text="Add Student", command=self.add_student)
        self.add_button.grid(row=2, columnspan=2, pady=10)

        # Edit and Delete Student Section
        self.edit_delete_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.edit_delete_frame.pack(pady=20)
        self.search_label = tk.Label(self.edit_delete_frame, text="Search Roll Number:", bg="#f0f0f0")
        self.search_label.grid(row=0, column=0, padx=10, pady=5)
        self.search_entry = tk.Entry(self.edit_delete_frame)
        self.search_entry.grid(row=0, column=1, padx=10, pady=5)
        self.search_button = tk.Button(self.edit_delete_frame, text="Search", command=self.search_student)
        self.search_button.grid(row=0, column=2, padx=10, pady=5)

        self.name_edit_label = tk.Label(self.edit_delete_frame, text="Name:", bg="#f0f0f0")
        self.name_edit_label.grid(row=1, column=0, padx=10, pady=5)
        self.name_edit_entry = tk.Entry(self.edit_delete_frame)
        self.name_edit_entry.grid(row=1, column=1, padx=10, pady=5)
        self.roll_edit_label = tk.Label(self.edit_delete_frame, text="Roll Number:", bg="#f0f0f0")
        self.roll_edit_label.grid(row=2, column=0, padx=10, pady=5)
        self.roll_edit_entry = tk.Entry(self.edit_delete_frame)
        self.roll_edit_entry.grid(row=2, column=1, padx=10, pady=5)
        self.edit_button = tk.Button(self.edit_delete_frame, text="Edit Student", command=self.edit_student)
        self.edit_button.grid(row=3, column=0, pady=10)
        self.delete_button = tk.Button(self.edit_delete_frame, text="Delete Student", command=self.delete_student)
        self.delete_button.grid(row=3, column=1, pady=10)

        # Mark Attendance Section
        self.mark_attendance_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.mark_attendance_frame.pack(pady=20)
        self.roll_att_label = tk.Label(self.mark_attendance_frame, text="Roll Number:", bg="#f0f0f0")
        self.roll_att_label.grid(row=0, column=0, padx=10, pady=5)
        self.roll_att_entry = tk.Entry(self.mark_attendance_frame)
        self.roll_att_entry.grid(row=0, column=1, padx=10, pady=5)
        self.status_label = tk.Label(self.mark_attendance_frame, text="Status:", bg="#f0f0f0")
        self.status_label.grid(row=1, column=0, padx=10, pady=5)
        self.status_combo = ttk.Combobox(self.mark_attendance_frame, values=["Present", "Absent"])
        self.status_combo.grid(row=1, column=1, padx=10, pady=5)
        self.mark_button = tk.Button(self.mark_attendance_frame, text="Mark Attendance", command=lambda: mark_attendance(self.roll_att_entry.get(), self.status_combo.get()))
        self.mark_button.grid(row=2, columnspan=2, pady=10)

        # View Attendance Section
        self.view_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.view_frame.pack(pady=20)
        self.view_button = tk.Button(self.view_frame, text="View Attendance Records", command=self.view_records)
        self.view_button.pack(pady=10)

        # Export Attendance Section
        self.export_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.export_frame.pack(pady=20)
        self.export_button = tk.Button(self.export_frame, text="Export Attendance Records", command=self.export_records)
        self.export_button.pack(pady=10)

        # Filter Attendance by Date Section
        self.filter_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.filter_frame.pack(pady=20)
        self.filter_label = tk.Label(self.filter_frame, text="Filter by Date (YYYY-MM-DD):", bg="#f0f0f0")
        self.filter_label.grid(row=0, column=0, padx=10, pady=5)
        self.filter_entry = tk.Entry(self.filter_frame)
        self.filter_entry.grid(row=0, column=1, padx=10, pady=5)
        self.filter_button = tk.Button(self.filter_frame, text="Filter", command=self.filter_records)
        self.filter_button.grid(row=0, column=2, padx=10, pady=5)
    def add_student(self):
        name = self.name_entry.get()
        roll_number = self.roll_entry.get()
        if name and roll_number:
            add_student(name, roll_number)
            self.name_entry.delete(0, tk.END)
            self.roll_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def search_student(self):
        roll_number = self.search_entry.get()
        student = search_student(roll_number)
        if student:
            self.name_edit_entry.delete(0, tk.END)
            self.name_edit_entry.insert(0, student[1])
            self.roll_edit_entry.delete(0, tk.END)
            self.roll_edit_entry.insert(0, student[2])
            self.current_student_id = student[0]
        else:
            messagebox.showerror("Error", "Student not found")

    def edit_student(self):
        name = self.name_edit_entry.get()
        roll_number = self.roll_edit_entry.get()
        if name and roll_number:
            edit_student(self.current_student_id, name, roll_number)
            self.name_edit_entry.delete(0, tk.END)
            self.roll_edit_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def delete_student(self):
        delete_student(self.current_student_id)
        self.name_edit_entry.delete(0, tk.END)
        self.roll_edit_entry.delete(0, tk.END)

    def view_records(self):
        records = view_attendance()
        self.view_window = tk.Toplevel(self.root)
        self.view_window.title("Attendance Records")
        self.view_window.geometry("800x400")
        self.tree = ttk.Treeview(self.view_window, columns=("Name", "Roll Number", "Date", "Status"), show='headings')
        self.tree.heading("Name", text="Name")
        self.tree.heading("Roll Number", text="Roll Number")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True)
        for record in records:
            self.tree.insert("", tk.END, values=record)

    def export_records(self):
        records = view_attendance()
        export_to_csv(records)

    def filter_records(self):
        date = self.filter_entry.get()
        if date:
            records = filter_attendance_by_date(date)
            if records:
                self.filter_window = tk.Toplevel(self.root)
                self.filter_window.title(f"Attendance Records for {date}")
                self.filter_window.geometry("800x400")
                self.tree = ttk.Treeview(self.filter_window, columns=("Name", "Roll Number", "Date", "Status"), show='headings')
                self.tree.heading("Name", text="Name")
                self.tree.heading("Roll Number", text="Roll Number")
                self.tree.heading("Date", text="Date")
                self.tree.heading("Status", text="Status")
                self.tree.pack(fill=tk.BOTH, expand=True)
                for record in records:
                    self.tree.insert("", tk.END, values=record)
            else:
                messagebox.showinfo("No Records", "No attendance records found for the specified date")
        else:
            messagebox.showerror("Error", "Please enter a date")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()

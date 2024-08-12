import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class StudentInformationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Information System")
        self.root.geometry("1000x700")

        self.students = []

        self.create_widgets()

    def create_widgets(self):
        # Add Student
        tk.Label(self.root, text="Add/Update Student", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Student ID:").pack(pady=5)
        self.student_id_entry = tk.Entry(self.root, width=50)
        self.student_id_entry.pack(pady=5)

        tk.Label(self.root, text="Name:").pack(pady=5)
        self.name_entry = tk.Entry(self.root, width=50)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="Age:").pack(pady=5)
        self.age_entry = tk.Entry(self.root, width=50)
        self.age_entry.pack(pady=5)

        tk.Label(self.root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.root, width=50)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Address:").pack(pady=5)
        self.address_entry = tk.Entry(self.root, width=50)
        self.address_entry.pack(pady=5)

        self.add_student_button = tk.Button(self.root, text="Add Student", command=self.add_student)
        self.add_student_button.pack(pady=10)

        # Student Table
        self.student_table = ttk.Treeview(self.root, columns=("ID", "Name", "Age", "Email", "Address"), show='headings')
        self.student_table.heading("ID", text="Student ID")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Age", text="Age")
        self.student_table.heading("Email", text="Email")
        self.student_table.heading("Address", text="Address")
        self.student_table.pack(fill=tk.BOTH, expand=True, pady=10)

        self.update_button = tk.Button(self.root, text="Update Student", command=self.update_student)
        self.update_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.delete_button = tk.Button(self.root, text="Delete Student", command=self.delete_student)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Search Functionality
        tk.Label(self.root, text="Search by ID or Name:").pack(pady=5)
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_student)
        self.search_button.pack(pady=5)

        # Generate Report
        self.generate_report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.generate_report_button.pack(pady=10)

    def add_student(self):
        student_id = self.student_id_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if student_id and name and age.isdigit() and email and address:
            age = int(age)
            self.students.append({
                "id": student_id,
                "name": name,
                "age": age,
                "email": email,
                "address": address
            })
            self.student_table.insert("", tk.END, values=(student_id, name, age, email, address))
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Please enter valid student details")

    def clear_entries(self):
        self.student_id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def update_student(self):
        selected_item = self.student_table.selection()
        if selected_item:
            item = self.student_table.item(selected_item)
            student_id, name, age, email, address = item['values']

            update_window = tk.Toplevel(self.root)
            update_window.title("Update Student")
            update_window.geometry("300x300")

            tk.Label(update_window, text="Student ID:").pack(pady=5)
            id_entry = tk.Entry(update_window, width=30)
            id_entry.pack(pady=5)
            id_entry.insert(0, student_id)
            id_entry.config(state=tk.DISABLED)

            tk.Label(update_window, text="Name:").pack(pady=5)
            name_entry = tk.Entry(update_window, width=30)
            name_entry.pack(pady=5)
            name_entry.insert(0, name)

            tk.Label(update_window, text="Age:").pack(pady=5)
            age_entry = tk.Entry(update_window, width=30)
            age_entry.pack(pady=5)
            age_entry.insert(0, age)

            tk.Label(update_window, text="Email:").pack(pady=5)
            email_entry = tk.Entry(update_window, width=30)
            email_entry.pack(pady=5)
            email_entry.insert(0, email)

            tk.Label(update_window, text="Address:").pack(pady=5)
            address_entry = tk.Entry(update_window, width=30)
            address_entry.pack(pady=5)
            address_entry.insert(0, address)

            def save_changes():
                new_name = name_entry.get()
                new_age = age_entry.get()
                new_email = email_entry.get()
                new_address = address_entry.get()

                if new_name and new_age.isdigit() and new_email and new_address:
                    new_age = int(new_age)
                    index = self.student_table.index(selected_item[0])
                    self.students[index] = {
                        "id": student_id,
                        "name": new_name,
                        "age": new_age,
                        "email": new_email,
                        "address": new_address
                    }
                    self.display_students()
                    update_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter valid student details")

            tk.Button(update_window, text="Save Changes", command=save_changes).pack(pady=20)
        else:
            messagebox.showerror("Error", "Please select a student to update")

    def delete_student(self):
        selected_item = self.student_table.selection()
        if selected_item:
            index = self.student_table.index(selected_item[0])
            del self.students[index]
            self.display_students()
        else:
            messagebox.showerror("Error", "Please select a student to delete")

    def search_student(self):
        search_term = self.search_entry.get().lower()
        filtered_students = [s for s in self.students if search_term in s['id'].lower() or search_term in s['name'].lower()]
        self.display_filtered_students(filtered_students)

    def display_students(self):
        self.student_table.delete(*self.student_table.get_children())
        for student in self.students:
            self.student_table.insert("", tk.END, values=(student['id'], student['name'], student['age'], student['email'], student['address']))

    def display_filtered_students(self, students_list):
        self.student_table.delete(*self.student_table.get_children())
        for student in students_list:
            self.student_table.insert("", tk.END, values=(student['id'], student['name'], student['age'], student['email'], student['address']))

    def generate_report(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Student ID", "Name", "Age", "Email", "Address"])
                for student in self.students:
                    writer.writerow([student['id'], student['name'], student['age'], student['email'], student['address']])
            messagebox.showinfo("Success", "Report generated successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentInformationSystem(root)
    root.mainloop()

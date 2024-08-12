import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

class TimeTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Table Generator")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        # Frame for adding subjects
        self.add_subject_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.add_subject_frame.pack(pady=20)

        self.subject_label = tk.Label(self.add_subject_frame, text="Subject:", bg="#f0f0f0")
        self.subject_label.grid(row=0, column=0, padx=10, pady=5)
        self.subject_entry = tk.Entry(self.add_subject_frame, width=20)
        self.subject_entry.grid(row=0, column=1, padx=10, pady=5)

        self.time_label = tk.Label(self.add_subject_frame, text="Time (HH:MM):", bg="#f0f0f0")
        self.time_label.grid(row=0, column=2, padx=10, pady=5)
        self.time_entry = tk.Entry(self.add_subject_frame, width=15)
        self.time_entry.grid(row=0, column=3, padx=10, pady=5)

        self.day_label = tk.Label(self.add_subject_frame, text="Day:", bg="#f0f0f0")
        self.day_label.grid(row=0, column=4, padx=10, pady=5)
        self.day_combo = ttk.Combobox(self.add_subject_frame, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        self.day_combo.grid(row=0, column=5, padx=10, pady=5)

        self.add_button = tk.Button(self.add_subject_frame, text="Add Subject", command=self.add_subject)
        self.add_button.grid(row=0, column=6, padx=10, pady=5)

        # Frame for timetable display
        self.timetable_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.timetable_frame.pack(pady=20)

        self.tree = ttk.Treeview(self.timetable_frame, columns=("Subject", "Time", "Day"), show='headings')
        self.tree.heading("Subject", text="Subject")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Day", text="Day")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Frame for subject operations
        self.subject_ops_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.subject_ops_frame.pack(pady=20)

        self.edit_button = tk.Button(self.subject_ops_frame, text="Edit Subject", command=self.edit_subject)
        self.edit_button.grid(row=0, column=0, padx=10, pady=5)
        self.delete_button = tk.Button(self.subject_ops_frame, text="Delete Subject", command=self.delete_subject)
        self.delete_button.grid(row=0, column=1, padx=10, pady=5)

        # Frame for file operations
        self.file_ops_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.file_ops_frame.pack(pady=20)

        self.save_button = tk.Button(self.file_ops_frame, text="Save Time Table", command=self.save_time_table)
        self.save_button.grid(row=0, column=0, padx=10, pady=5)
        self.load_button = tk.Button(self.file_ops_frame, text="Load Time Table", command=self.load_time_table)
        self.load_button.grid(row=0, column=1, padx=10, pady=5)
        self.clear_button = tk.Button(self.file_ops_frame, text="Clear Time Table", command=self.clear_time_table)
        self.clear_button.grid(row=0, column=2, padx=10, pady=5)

        self.subjects = []

    def add_subject(self):
        subject = self.subject_entry.get()
        time = self.time_entry.get()
        day = self.day_combo.get()
        if subject and time and day:
            self.subjects.append({"subject": subject, "time": time, "day": day})
            self.subject_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            self.day_combo.set('')
            self.display_timetable()
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def edit_subject(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            subject_details = item['values']
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Subject")
            edit_window.geometry("400x300")

            tk.Label(edit_window, text="Subject:").pack(pady=5)
            subject_entry = tk.Entry(edit_window, width=30)
            subject_entry.pack(pady=5)
            subject_entry.insert(0, subject_details[0])

            tk.Label(edit_window, text="Time (HH:MM):").pack(pady=5)
            time_entry = tk.Entry(edit_window, width=15)
            time_entry.pack(pady=5)
            time_entry.insert(0, subject_details[1])

            tk.Label(edit_window, text="Day:").pack(pady=5)
            day_combo = ttk.Combobox(edit_window, values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
            day_combo.pack(pady=5)
            day_combo.set(subject_details[2])

            def save_changes():
                new_subject = subject_entry.get()
                new_time = time_entry.get()
                new_day = day_combo.get()
                if new_subject and new_time and new_day:
                    index = self.tree.index(selected_item[0])
                    self.subjects[index] = {"subject": new_subject, "time": new_time, "day": new_day}
                    self.display_timetable()
                    edit_window.destroy()
                else:
                    messagebox.showerror("Error", "Please fill in all fields")

            tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=20)
        else:
            messagebox.showerror("Error", "Please select a subject to edit")

    def delete_subject(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item[0])
            del self.subjects[index]
            self.display_timetable()
        else:
            messagebox.showerror("Error", "Please select a subject to delete")

    def display_timetable(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, subject in enumerate(self.subjects):
            self.tree.insert("", tk.END, iid=idx, values=(subject['subject'], subject['time'], subject['day']))

    def save_time_table(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.subjects, file)
            messagebox.showinfo("Success", "Time table saved successfully")

    def load_time_table(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                self.subjects = json.load(file)
            self.display_timetable()
            messagebox.showinfo("Success", "Time table loaded successfully")

    def clear_time_table(self):
        self.subjects = []
        self.display_timetable()

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeTableApp(root)
    root.mainloop()

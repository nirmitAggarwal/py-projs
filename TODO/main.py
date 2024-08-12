import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List Organizer")
        self.root.geometry("800x600")
        self.root.configure(bg="#e6e6e6")

        # Frame for adding tasks
        self.add_task_frame = tk.Frame(self.root, bg="#e6e6e6")
        self.add_task_frame.pack(pady=20)

        self.task_label = tk.Label(self.add_task_frame, text="Task:", bg="#e6e6e6")
        self.task_label.grid(row=0, column=0, padx=10, pady=5)
        self.task_entry = tk.Entry(self.add_task_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=10, pady=5)

        self.priority_label = tk.Label(self.add_task_frame, text="Priority:", bg="#e6e6e6")
        self.priority_label.grid(row=0, column=2, padx=10, pady=5)
        self.priority_combo = ttk.Combobox(self.add_task_frame, values=["Low", "Medium", "High"])
        self.priority_combo.grid(row=0, column=3, padx=10, pady=5)

        self.due_date_label = tk.Label(self.add_task_frame, text="Due Date (YYYY-MM-DD):", bg="#e6e6e6")
        self.due_date_label.grid(row=0, column=4, padx=10, pady=5)
        self.due_date_entry = tk.Entry(self.add_task_frame, width=15)
        self.due_date_entry.grid(row=0, column=5, padx=10, pady=5)

        self.add_button = tk.Button(self.add_task_frame, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=6, padx=10, pady=5)

        # Frame for task list
        self.task_list_frame = tk.Frame(self.root, bg="#e6e6e6")
        self.task_list_frame.pack(pady=20)

        self.tree = ttk.Treeview(self.task_list_frame, columns=("Task", "Priority", "Due Date", "Status"), show='headings')
        self.tree.heading("Task", text="Task")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Status", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Frame for task operations
        self.task_ops_frame = tk.Frame(self.root, bg="#e6e6e6")
        self.task_ops_frame.pack(pady=20)

        self.edit_button = tk.Button(self.task_ops_frame, text="Edit Task", command=self.edit_task)
        self.edit_button.grid(row=0, column=0, padx=10, pady=5)
        self.delete_button = tk.Button(self.task_ops_frame, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=0, column=1, padx=10, pady=5)
        self.complete_button = tk.Button(self.task_ops_frame, text="Mark as Complete", command=self.mark_as_complete)
        self.complete_button.grid(row=0, column=2, padx=10, pady=5)
        self.incomplete_button = tk.Button(self.task_ops_frame, text="Mark as Incomplete", command=self.mark_as_incomplete)
        self.incomplete_button.grid(row=0, column=3, padx=10, pady=5)

        # Frame for filter and sort operations
        self.filter_sort_frame = tk.Frame(self.root, bg="#e6e6e6")
        self.filter_sort_frame.pack(pady=20)

        self.filter_label = tk.Label(self.filter_sort_frame, text="Filter by Status:", bg="#e6e6e6")
        self.filter_label.grid(row=0, column=0, padx=10, pady=5)
        self.filter_combo = ttk.Combobox(self.filter_sort_frame, values=["All", "Complete", "Incomplete"])
        self.filter_combo.grid(row=0, column=1, padx=10, pady=5)
        self.filter_button = tk.Button(self.filter_sort_frame, text="Filter", command=self.filter_tasks)
        self.filter_button.grid(row=0, column=2, padx=10, pady=5)

        self.sort_label = tk.Label(self.filter_sort_frame, text="Sort by:", bg="#e6e6e6")
        self.sort_label.grid(row=0, column=3, padx=10, pady=5)
        self.sort_combo = ttk.Combobox(self.filter_sort_frame, values=["Due Date", "Priority"])
        self.sort_combo.grid(row=0, column=4, padx=10, pady=5)
        self.sort_button = tk.Button(self.filter_sort_frame, text="Sort", command=self.sort_tasks)
        self.sort_button.grid(row=0, column=5, padx=10, pady=5)

        # Frame for file operations
        self.file_ops_frame = tk.Frame(self.root, bg="#e6e6e6")
        self.file_ops_frame.pack(pady=20)

        self.save_button = tk.Button(self.file_ops_frame, text="Save Tasks", command=self.save_tasks)
        self.save_button.grid(row=0, column=0, padx=10, pady=5)
        self.load_button = tk.Button(self.file_ops_frame, text="Load Tasks", command=self.load_tasks)
        self.load_button.grid(row=0, column=1, padx=10, pady=5)

        self.tasks = []

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_combo.get()
        due_date = self.due_date_entry.get()
        if task and priority and due_date:
            self.tasks.append({"task": task, "priority": priority, "due_date": due_date, "status": "Incomplete"})
            self.task_entry.delete(0, tk.END)
            self.priority_combo.set('')
            self.due_date_entry.delete(0, tk.END)
            self.display_tasks()
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def edit_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            task_details = item['values']
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Task")
            edit_window.geometry("400x300")

            tk.Label(edit_window, text="Task:").pack(pady=5)
            task_entry = tk.Entry(edit_window, width=30)
            task_entry.pack(pady=5)
            task_entry.insert(0, task_details[0])

            tk.Label(edit_window, text="Priority:").pack(pady=5)
            priority_combo = ttk.Combobox(edit_window, values=["Low", "Medium", "High"])
            priority_combo.pack(pady=5)
            priority_combo.set(task_details[1])

            tk.Label(edit_window, text="Due Date (YYYY-MM-DD):").pack(pady=5)
            due_date_entry = tk.Entry(edit_window, width=15)
            due_date_entry.pack(pady=5)
            due_date_entry.insert(0, task_details[2])

            def save_changes():
                new_task = task_entry.get()
                new_priority = priority_combo.get()
                new_due_date = due_date_entry.get()
                if new_task and new_priority and new_due_date:
                    self.tasks[selected_item[0]] = {"task": new_task, "priority": new_priority, "due_date": new_due_date, "status": task_details[3]}
                    self.display_tasks()
                    edit_window.destroy()
                else:
                    messagebox.showerror("Error", "Please fill in all fields")

            tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=20)
        else:
            messagebox.showerror("Error", "Please select a task to edit")

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            del self.tasks[selected_item[0]]
            self.display_tasks()
        else:
            messagebox.showerror("Error", "Please select a task to delete")

    def mark_as_complete(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tasks[selected_item[0]]['status'] = "Complete"
            self.display_tasks()
        else:
            messagebox.showerror("Error", "Please select a task to mark as complete")

    def mark_as_incomplete(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tasks[selected_item[0]]['status'] = "Incomplete"
            self.display_tasks()
        else:
            messagebox.showerror("Error", "Please select a task to mark as incomplete")

    def filter_tasks(self):
        filter_status = self.filter_combo.get()
        if filter_status:
            filtered_tasks = [task for task in self.tasks if filter_status == "All" or task['status'] == filter_status]
            self.display_tasks(filtered_tasks)
        else:
            messagebox.showerror("Error", "Please select a status to filter by")

    def sort_tasks(self):
        sort_by = self.sort_combo.get()
        if sort_by:
            if sort_by == "Due Date":
                sorted_tasks = sorted(self.tasks, key=lambda x: datetime.strptime(x['due_date'], '%Y-%m-%d'))
            else:
                priority_map = {"Low": 1, "Medium": 2, "High": 3}
                sorted_tasks = sorted(self.tasks, key=lambda x: priority_map[x['priority']])
            self.display_tasks(sorted_tasks)
        else:
            messagebox.showerror("Error", "Please select a sort criteria")

    def display_tasks(self, tasks=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if tasks is None:
            tasks = self.tasks
        for idx, task in enumerate(tasks):
            self.tree.insert("", tk.END, iid=idx, values=(task['task'], task['priority'], task['due_date'], task['status']))

    def save_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.tasks, file)
            messagebox.showinfo("Success", "Tasks saved successfully")

    def load_tasks(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                self.tasks = json.load(file)
            self.display_tasks()
            messagebox.showinfo("Success", "Tasks loaded successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

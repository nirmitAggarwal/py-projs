import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class AlumniInformationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Alumni Information System")
        self.root.geometry("900x600")

        self.alumni_data = []

        self.create_widgets()

    def create_widgets(self):
        # Add Alumni
        tk.Label(self.root, text="Name:").pack(pady=5)
        self.name_entry = tk.Entry(self.root, width=50)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="Graduation Year:").pack(pady=5)
        self.grad_year_entry = tk.Entry(self.root, width=50)
        self.grad_year_entry.pack(pady=5)

        tk.Label(self.root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(self.root, width=50)
        self.email_entry.pack(pady=5)

        tk.Label(self.root, text="Phone Number:").pack(pady=5)
        self.phone_entry = tk.Entry(self.root, width=50)
        self.phone_entry.pack(pady=5)

        tk.Label(self.root, text="Address:").pack(pady=5)
        self.address_entry = tk.Entry(self.root, width=50)
        self.address_entry.pack(pady=5)

        self.add_alumni_button = tk.Button(self.root, text="Add Alumni", command=self.add_alumni)
        self.add_alumni_button.pack(pady=10)

        # Alumni Table
        self.alumni_table = ttk.Treeview(self.root, columns=("Name", "Graduation Year", "Email", "Phone", "Address"), show='headings')
        self.alumni_table.heading("Name", text="Name")
        self.alumni_table.heading("Graduation Year", text="Graduation Year")
        self.alumni_table.heading("Email", text="Email")
        self.alumni_table.heading("Phone", text="Phone Number")
        self.alumni_table.heading("Address", text="Address")
        self.alumni_table.pack(fill=tk.BOTH, expand=True, pady=10)

        self.edit_button = tk.Button(self.root, text="Edit Alumni", command=self.edit_alumni)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.delete_button = tk.Button(self.root, text="Delete Alumni", command=self.delete_alumni)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Search Functionality
        tk.Label(self.root, text="Search by Name:").pack(pady=5)
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_alumni)
        self.search_button.pack(pady=5)

        # Generate Report
        self.generate_report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.generate_report_button.pack(pady=10)

    def add_alumni(self):
        name = self.name_entry.get()
        grad_year = self.grad_year_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()

        if name and grad_year.isdigit() and email and phone and address:
            self.alumni_data.append({
                "name": name,
                "grad_year": int(grad_year),
                "email": email,
                "phone": phone,
                "address": address
            })
            self.alumni_table.insert("", tk.END, values=(name, grad_year, email, phone, address))
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Please enter valid details")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.grad_year_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def edit_alumni(self):
        selected_item = self.alumni_table.selection()
        if selected_item:
            item = self.alumni_table.item(selected_item)
            name, grad_year, email, phone, address = item['values']

            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Alumni")
            edit_window.geometry("300x300")

            tk.Label(edit_window, text="Name:").pack(pady=5)
            name_entry = tk.Entry(edit_window, width=30)
            name_entry.pack(pady=5)
            name_entry.insert(0, name)

            tk.Label(edit_window, text="Graduation Year:").pack(pady=5)
            grad_year_entry = tk.Entry(edit_window, width=30)
            grad_year_entry.pack(pady=5)
            grad_year_entry.insert(0, grad_year)

            tk.Label(edit_window, text="Email:").pack(pady=5)
            email_entry = tk.Entry(edit_window, width=30)
            email_entry.pack(pady=5)
            email_entry.insert(0, email)

            tk.Label(edit_window, text="Phone Number:").pack(pady=5)
            phone_entry = tk.Entry(edit_window, width=30)
            phone_entry.pack(pady=5)
            phone_entry.insert(0, phone)

            tk.Label(edit_window, text="Address:").pack(pady=5)
            address_entry = tk.Entry(edit_window, width=30)
            address_entry.pack(pady=5)
            address_entry.insert(0, address)

            def save_changes():
                new_name = name_entry.get()
                new_grad_year = grad_year_entry.get()
                new_email = email_entry.get()
                new_phone = phone_entry.get()
                new_address = address_entry.get()

                if new_name and new_grad_year.isdigit() and new_email and new_phone and new_address:
                    index = self.alumni_table.index(selected_item[0])
                    self.alumni_data[index] = {
                        "name": new_name,
                        "grad_year": int(new_grad_year),
                        "email": new_email,
                        "phone": new_phone,
                        "address": new_address
                    }
                    self.display_alumni()
                    edit_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter valid details")

            tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=20)
        else:
            messagebox.showerror("Error", "Please select an alumni record to edit")

    def delete_alumni(self):
        selected_item = self.alumni_table.selection()
        if selected_item:
            index = self.alumni_table.index(selected_item[0])
            del self.alumni_data[index]
            self.display_alumni()
        else:
            messagebox.showerror("Error", "Please select an alumni record to delete")

    def search_alumni(self):
        search_name = self.search_entry.get()
        filtered_alumni = [a for a in self.alumni_data if search_name.lower() in a['name'].lower()]
        self.display_filtered_alumni(filtered_alumni)

    def display_alumni(self):
        self.alumni_table.delete(*self.alumni_table.get_children())
        for alumni in self.alumni_data:
            self.alumni_table.insert("", tk.END, values=(alumni['name'], alumni['grad_year'], alumni['email'], alumni['phone'], alumni['address']))

    def display_filtered_alumni(self, alumni_list):
        self.alumni_table.delete(*self.alumni_table.get_children())
        for alumni in alumni_list:
            self.alumni_table.insert("", tk.END, values=(alumni['name'], alumni['grad_year'], alumni['email'], alumni['phone'], alumni['address']))

    def generate_report(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Graduation Year", "Email", "Phone Number", "Address"])
                for alumni in self.alumni_data:
                    writer.writerow([alumni['name'], alumni['grad_year'], alumni['email'], alumni['phone'], alumni['address']])
            messagebox.showinfo("Success", "Report generated successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlumniInformationSystem(root)
    root.mainloop()

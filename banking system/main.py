import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv

class BankingManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Banking Management System")
        self.root.geometry("1200x800")

        self.accounts = []

        self.create_widgets()

    def create_widgets(self):
        # Account Management
        tk.Label(self.root, text="Account Management", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Account Number:").pack(pady=5)
        self.account_number_entry = tk.Entry(self.root, width=50)
        self.account_number_entry.pack(pady=5)

        tk.Label(self.root, text="Account Holder Name:").pack(pady=5)
        self.account_holder_name_entry = tk.Entry(self.root, width=50)
        self.account_holder_name_entry.pack(pady=5)

        tk.Label(self.root, text="Initial Balance:").pack(pady=5)
        self.initial_balance_entry = tk.Entry(self.root, width=50)
        self.initial_balance_entry.pack(pady=5)

        self.create_account_button = tk.Button(self.root, text="Create Account", command=self.create_account)
        self.create_account_button.pack(pady=10)

        self.update_account_button = tk.Button(self.root, text="Update Account", command=self.update_account)
        self.update_account_button.pack(pady=5)
        self.delete_account_button = tk.Button(self.root, text="Delete Account", command=self.delete_account)
        self.delete_account_button.pack(pady=5)

        # Account Table
        self.account_table = ttk.Treeview(self.root, columns=("Account Number", "Holder Name", "Balance"), show='headings')
        self.account_table.heading("Account Number", text="Account Number")
        self.account_table.heading("Holder Name", text="Holder Name")
        self.account_table.heading("Balance", text="Balance")
        self.account_table.pack(fill=tk.BOTH, expand=True, pady=10)

        # Transactions
        tk.Label(self.root, text="Transactions", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Transaction Type:").pack(pady=5)
        self.transaction_type = tk.StringVar()
        self.transaction_type.set("Deposit")
        tk.Radiobutton(self.root, text="Deposit", variable=self.transaction_type, value="Deposit").pack(pady=5)
        tk.Radiobutton(self.root, text="Withdraw", variable=self.transaction_type, value="Withdraw").pack(pady=5)

        tk.Label(self.root, text="Amount:").pack(pady=5)
        self.amount_entry = tk.Entry(self.root, width=50)
        self.amount_entry.pack(pady=5)

        self.perform_transaction_button = tk.Button(self.root, text="Perform Transaction", command=self.perform_transaction)
        self.perform_transaction_button.pack(pady=10)

        # Transaction History
        tk.Label(self.root, text="Transaction History", font=("Arial", 16)).pack(pady=10)

        self.transaction_history_table = ttk.Treeview(self.root, columns=("Account Number", "Type", "Amount", "Balance"), show='headings')
        self.transaction_history_table.heading("Account Number", text="Account Number")
        self.transaction_history_table.heading("Type", text="Type")
        self.transaction_history_table.heading("Amount", text="Amount")
        self.transaction_history_table.heading("Balance", text="Balance")
        self.transaction_history_table.pack(fill=tk.BOTH, expand=True, pady=10)

        # Search Functionality
        tk.Label(self.root, text="Search Account by Number:").pack(pady=5)
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_account)
        self.search_button.pack(pady=5)

        # Generate Report
        self.generate_report_button = tk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.generate_report_button.pack(pady=10)

    def create_account(self):
        account_number = self.account_number_entry.get()
        holder_name = self.account_holder_name_entry.get()
        initial_balance = self.initial_balance_entry.get()

        if account_number and holder_name and initial_balance.replace('.', '', 1).isdigit():
            initial_balance = float(initial_balance)
            self.accounts.append({
                "number": account_number,
                "holder": holder_name,
                "balance": initial_balance
            })
            self.account_table.insert("", tk.END, values=(account_number, holder_name, initial_balance))
            self.clear_account_entries()
        else:
            messagebox.showerror("Error", "Please enter valid account details")

    def clear_account_entries(self):
        self.account_number_entry.delete(0, tk.END)
        self.account_holder_name_entry.delete(0, tk.END)
        self.initial_balance_entry.delete(0, tk.END)

    def update_account(self):
        selected_item = self.account_table.selection()
        if selected_item:
            item = self.account_table.item(selected_item)
            account_number, holder_name, balance = item['values']

            update_window = tk.Toplevel(self.root)
            update_window.title("Update Account")
            update_window.geometry("300x300")

            tk.Label(update_window, text="Account Number:").pack(pady=5)
            id_entry = tk.Entry(update_window, width=30)
            id_entry.pack(pady=5)
            id_entry.insert(0, account_number)
            id_entry.config(state=tk.DISABLED)

            tk.Label(update_window, text="Holder Name:").pack(pady=5)
            name_entry = tk.Entry(update_window, width=30)
            name_entry.pack(pady=5)
            name_entry.insert(0, holder_name)

            tk.Label(update_window, text="Balance:").pack(pady=5)
            balance_entry = tk.Entry(update_window, width=30)
            balance_entry.pack(pady=5)
            balance_entry.insert(0, balance)

            def save_changes():
                new_holder_name = name_entry.get()
                new_balance = balance_entry.get()

                if new_holder_name and new_balance.replace('.', '', 1).isdigit():
                    new_balance = float(new_balance)
                    index = self.account_table.index(selected_item[0])
                    self.accounts[index] = {
                        "number": account_number,
                        "holder": new_holder_name,
                        "balance": new_balance
                    }
                    self.display_accounts()
                    update_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter valid account details")

            tk.Button(update_window, text="Save Changes", command=save_changes).pack(pady=20)
        else:
            messagebox.showerror("Error", "Please select an account to update")

    def delete_account(self):
        selected_item = self.account_table.selection()
        if selected_item:
            index = self.account_table.index(selected_item[0])
            del self.accounts[index]
            self.display_accounts()
        else:
            messagebox.showerror("Error", "Please select an account to delete")

    def perform_transaction(self):
        selected_item = self.account_table.selection()
        if selected_item:
            item = self.account_table.item(selected_item)
            account_number, holder_name, balance = item['values']
            transaction_type = self.transaction_type.get()
            amount = self.amount_entry.get()

            if amount.replace('.', '', 1).isdigit():
                amount = float(amount)
                if transaction_type == "Deposit":
                    new_balance = balance + amount
                elif transaction_type == "Withdraw":
                    if amount <= balance:
                        new_balance = balance - amount
                    else:
                        messagebox.showerror("Error", "Insufficient funds")
                        return
                else:
                    messagebox.showerror("Error", "Invalid transaction type")
                    return

                # Update account balance
                for account in self.accounts:
                    if account["number"] == account_number:
                        account["balance"] = new_balance
                        break

                self.display_accounts()

                # Log transaction
                self.transaction_history_table.insert("", tk.END, values=(account_number, transaction_type, amount, new_balance))
                self.amount_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Please enter a valid amount")
        else:
            messagebox.showerror("Error", "Please select an account for transaction")

    def search_account(self):
        search_number = self.search_entry.get()
        filtered_accounts = [a for a in self.accounts if search_number in a['number']]
        self.display_filtered_accounts(filtered_accounts)

    def display_accounts(self):
        self.account_table.delete(*self.account_table.get_children())
        for account in self.accounts:
            self.account_table.insert("", tk.END, values=(account['number'], account['holder'], account['balance']))

    def display_filtered_accounts(self, accounts_list):
        self.account_table.delete(*self.account_table.get_children())
        for account in accounts_list:
            self.account_table.insert("", tk.END, values=(account['number'], account['holder'], account['balance']))

    def generate_report(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Account Number", "Holder Name", "Balance"])
                for account in self.accounts:
                    writer.writerow([account['number'], account['holder'], account['balance']])
            messagebox.showinfo("Success", "Report generated successfully")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingManagementSystem(root)
    root.mainloop()

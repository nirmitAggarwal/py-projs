import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import base64
from cryptography.fernet import Fernet

# Generate and save a key for encryption
def generate_key():
    return Fernet.generate_key()

def load_key():
    try:
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        key = generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

def encrypt_message(message, key):
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, key):
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("800x600")

        self.key = load_key()

        self.create_widgets()
        self.passwords = []

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Title:")
        self.title_label.pack(pady=5)
        self.title_entry = tk.Entry(self.root, width=50)
        self.title_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, width=50, show="*")
        self.password_entry.pack(pady=5)

        self.add_button = tk.Button(self.root, text="Add Password", command=self.add_password)
        self.add_button.pack(pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Title", "Password"), show='headings')
        self.tree.heading("Title", text="Title")
        self.tree.heading("Password", text="Password")
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.edit_button = tk.Button(self.root, text="Edit Password", command=self.edit_password)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.delete_button = tk.Button(self.root, text="Delete Password", command=self.delete_password)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.save_button = tk.Button(self.root, text="Save Passwords", command=self.save_passwords)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.load_button = tk.Button(self.root, text="Load Passwords", command=self.load_passwords)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.search_entry = tk.Entry(self.root, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_passwords)
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)

    def add_password(self):
        title = self.title_entry.get()
        password = self.password_entry.get()
        if title and password:
            encrypted_password = encrypt_message(password, self.key)
            self.passwords.append({"title": title, "password": encrypted_password})
            self.title_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.display_passwords()
        else:
            messagebox.showerror("Error", "Please enter both title and password")

    def edit_password(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            title = item['values'][0]
            password = decrypt_message(item['values'][1].encode(), self.key)

            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Password")
            edit_window.geometry("300x200")

            tk.Label(edit_window, text="Title:").pack(pady=5)
            title_entry = tk.Entry(edit_window, width=30)
            title_entry.pack(pady=5)
            title_entry.insert(0, title)

            tk.Label(edit_window, text="Password:").pack(pady=5)
            password_entry = tk.Entry(edit_window, width=30, show="*")
            password_entry.pack(pady=5)
            password_entry.insert(0, password)

            def save_changes():
                new_title = title_entry.get()
                new_password = password_entry.get()
                if new_title and new_password:
                    encrypted_password = encrypt_message(new_password, self.key)
                    index = self.tree.index(selected_item[0])
                    self.passwords[index] = {"title": new_title, "password": encrypted_password}
                    self.display_passwords()
                    edit_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter both title and password")

            tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=20)
        else:
            messagebox.showerror("Error", "Please select a password to edit")

    def delete_password(self):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item[0])
            del self.passwords[index]
            self.display_passwords()
        else:
            messagebox.showerror("Error", "Please select a password to delete")

    def display_passwords(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for password in self.passwords:
            decrypted_password = decrypt_message(password['password'], self.key)
            self.tree.insert("", tk.END, values=(password['title'], decrypted_password))

    def save_passwords(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(self.passwords, file)
            messagebox.showinfo("Success", "Passwords saved successfully")

    def load_passwords(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                self.passwords = json.load(file)
            self.display_passwords()
            messagebox.showinfo("Success", "Passwords loaded successfully")

    def search_passwords(self):
        search_title = self.search_entry.get()
        filtered_passwords = [pwd for pwd in self.passwords if search_title.lower() in pwd['title'].lower()]
        self.display_filtered_passwords(filtered_passwords)

    def display_filtered_passwords(self, passwords):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for password in passwords:
            decrypted_password = decrypt_message(password['password'], self.key)
            self.tree.insert("", tk.END, values=(password['title'], decrypted_password))

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()

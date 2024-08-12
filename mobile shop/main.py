import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json

class OnlineMobileShop:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Mobile Shop")
        self.root.geometry("1000x700")

        self.products = []
        self.cart = []

        self.create_widgets()

    def create_widgets(self):
        # Product Management
        tk.Label(self.root, text="Add/Update Product", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Product Name:").pack(pady=5)
        self.product_name_entry = tk.Entry(self.root, width=50)
        self.product_name_entry.pack(pady=5)

        tk.Label(self.root, text="Brand:").pack(pady=5)
        self.brand_entry = tk.Entry(self.root, width=50)
        self.brand_entry.pack(pady=5)

        tk.Label(self.root, text="Price:").pack(pady=5)
        self.price_entry = tk.Entry(self.root, width=50)
        self.price_entry.pack(pady=5)

        tk.Label(self.root, text="Description:").pack(pady=5)
        self.description_entry = tk.Entry(self.root, width=50)
        self.description_entry.pack(pady=5)

        self.add_product_button = tk.Button(self.root, text="Add Product", command=self.add_product)
        self.add_product_button.pack(pady=10)

        # Product Table
        self.product_table = ttk.Treeview(self.root, columns=("Name", "Brand", "Price", "Description"), show='headings')
        self.product_table.heading("Name", text="Name")
        self.product_table.heading("Brand", text="Brand")
        self.product_table.heading("Price", text="Price")
        self.product_table.heading("Description", text="Description")
        self.product_table.pack(fill=tk.BOTH, expand=True, pady=10)

        self.update_button = tk.Button(self.root, text="Update Product", command=self.update_product)
        self.update_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.delete_button = tk.Button(self.root, text="Delete Product", command=self.delete_product)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Search and Filter
        tk.Label(self.root, text="Search by Name:").pack(pady=5)
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_product)
        self.search_button.pack(pady=5)

        tk.Label(self.root, text="Filter by Price Range:").pack(pady=5)
        self.min_price_entry = tk.Entry(self.root, width=20)
        self.min_price_entry.pack(side=tk.LEFT, padx=5)
        self.max_price_entry = tk.Entry(self.root, width=20)
        self.max_price_entry.pack(side=tk.LEFT, padx=5)
        self.filter_button = tk.Button(self.root, text="Filter", command=self.filter_products)
        self.filter_button.pack(pady=5)

        # Shopping Cart
        tk.Label(self.root, text="Shopping Cart", font=("Arial", 14)).pack(pady=10)

        self.cart_table = ttk.Treeview(self.root, columns=("Name", "Brand", "Price"), show='headings')
        self.cart_table.heading("Name", text="Name")
        self.cart_table.heading("Brand", text="Brand")
        self.cart_table.heading("Price", text="Price")
        self.cart_table.pack(fill=tk.BOTH, expand=True, pady=10)

        self.add_to_cart_button = tk.Button(self.root, text="Add to Cart", command=self.add_to_cart)
        self.add_to_cart_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.checkout_button = tk.Button(self.root, text="Checkout", command=self.checkout)
        self.checkout_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Status Bar
        self.status_label = tk.Label(self.root, text="Total Price: $0.00", anchor="w")
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def add_product(self):
        name = self.product_name_entry.get()
        brand = self.brand_entry.get()
        price = self.price_entry.get()
        description = self.description_entry.get()

        if name and brand and price.replace('.', '', 1).isdigit() and description:
            price = float(price)
            self.products.append({"name": name, "brand": brand, "price": price, "description": description})
            self.product_table.insert("", tk.END, values=(name, brand, price, description))
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Please enter valid product details")

    def update_product(self):
        selected_item = self.product_table.selection()
        if selected_item:
            item = self.product_table.item(selected_item)
            name, brand, price, description = item['values']

            update_window = tk.Toplevel(self.root)
            update_window.title("Update Product")
            update_window.geometry("300x300")

            tk.Label(update_window, text="Product Name:").pack(pady=5)
            name_entry = tk.Entry(update_window, width=30)
            name_entry.pack(pady=5)
            name_entry.insert(0, name)

            tk.Label(update_window, text="Brand:").pack(pady=5)
            brand_entry = tk.Entry(update_window, width=30)
            brand_entry.pack(pady=5)
            brand_entry.insert(0, brand)

            tk.Label(update_window, text="Price:").pack(pady=5)
            price_entry = tk.Entry(update_window, width=30)
            price_entry.pack(pady=5)
            price_entry.insert(0, price)

            tk.Label(update_window, text="Description:").pack(pady=5)
            description_entry = tk.Entry(update_window, width=30)
            description_entry.pack(pady=5)
            description_entry.insert(0, description)

            def save_changes():
                new_name = name_entry.get()
                new_brand = brand_entry.get()
                new_price = price_entry.get()
                new_description = description_entry.get()

                if new_name and new_brand and new_price.replace('.', '', 1).isdigit() and new_description:
                    new_price = float(new_price)
                    index = self.product_table.index(selected_item[0])
                    self.products[index] = {"name": new_name, "brand": new_brand, "price": new_price, "description": new_description}
                    self.display_products()
                    update_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter valid product details")

            tk.Button(update_window, text="Save Changes", command=save_changes).pack(pady=20)
        else:
            messagebox.showerror("Error", "Please select a product to update")

    def delete_product(self):
        selected_item = self.product_table.selection()
        if selected_item:
            index = self.product_table.index(selected_item[0])
            del self.products[index]
            self.display_products()
        else:
            messagebox.showerror("Error", "Please select a product to delete")

    def search_product(self):
        search_name = self.search_entry.get()
        filtered_products = [p for p in self.products if search_name.lower() in p['name'].lower()]
        self.display_filtered_products(filtered_products)

    def filter_products(self):
        min_price = self.min_price_entry.get()
        max_price = self.max_price_entry.get()
        if min_price.replace('.', '', 1).isdigit() and max_price.replace('.', '', 1).isdigit():
            min_price = float(min_price)
            max_price = float(max_price)
            filtered_products = [p for p in self.products if min_price <= p['price'] <= max_price]
            self.display_filtered_products(filtered_products)
        else:
            messagebox.showerror("Error", "Please enter valid price range")

    def display_products(self):
        self.product_table.delete(*self.product_table.get_children())
        for product in self.products:
            self.product_table.insert("", tk.END, values=(product['name'], product['brand'], product['price'], product['description']))

    def display_filtered_products(self, products):
        self.product_table.delete(*self.product_table.get_children())
        for product in products:
            self.product_table.insert("", tk.END, values=(product['name'], product['brand'], product['price'], product['description']))

    def add_to_cart(self):
        selected_item = self.product_table.selection()
        if selected_item:
            item = self.product_table.item(selected_item)
            name, brand, price, _ = item['values']
            self.cart.append({"name": name, "brand": brand, "price": price})
            self.cart_table.insert("", tk.END, values=(name, brand, price))
            self.update_status()
        else:
            messagebox.showerror("Error", "Please select a product to add to the cart")

    def update_status(self):
        total_price = sum(item['price'] for item in self.cart)
        self.status_label.config(text=f"Total Price: ${total_price:.2f}")

    def checkout(self):
        if self.cart:
            total_price = sum(item['price'] for item in self.cart)
            confirmation = messagebox.askyesno("Checkout", f"Your total is ${total_price:.2f}. Proceed to checkout?")
            if confirmation:
                self.cart = []
                self.cart_table.delete(*self.cart_table.get_children())
                self.update_status()
                messagebox.showinfo("Success", "Thank you for your purchase!")
        else:
            messagebox.showerror("Error", "Your cart is empty")

    def clear_entries(self):
        self.product_name_entry.delete(0, tk.END)
        self.brand_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = OnlineMobileShop(root)
    root.mainloop()

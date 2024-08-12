import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fpdf import FPDF
import json

class GSTBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GST Billing System")
        self.root.geometry("900x700")

        self.products = []
        self.gst_rate = 18
        self.company_name = "Your Company"
        self.company_address = "123 Business St, Business City, BC"

        self.create_widgets()

    def create_widgets(self):
        # Company Information
        tk.Label(self.root, text="Company Name:").pack(pady=5)
        self.company_name_entry = tk.Entry(self.root, width=50)
        self.company_name_entry.insert(0, self.company_name)
        self.company_name_entry.pack(pady=5)

        tk.Label(self.root, text="Company Address:").pack(pady=5)
        self.company_address_entry = tk.Entry(self.root, width=50)
        self.company_address_entry.insert(0, self.company_address)
        self.company_address_entry.pack(pady=5)

        # Product Details
        tk.Label(self.root, text="Product Name:").pack(pady=5)
        self.product_name_entry = tk.Entry(self.root, width=50)
        self.product_name_entry.pack(pady=5)

        tk.Label(self.root, text="Quantity:").pack(pady=5)
        self.quantity_entry = tk.Entry(self.root, width=50)
        self.quantity_entry.pack(pady=5)

        tk.Label(self.root, text="Unit Price:").pack(pady=5)
        self.unit_price_entry = tk.Entry(self.root, width=50)
        self.unit_price_entry.pack(pady=5)

        self.add_product_button = tk.Button(self.root, text="Add Product", command=self.add_product)
        self.add_product_button.pack(pady=10)

        # Product Table
        self.product_table = ttk.Treeview(self.root, columns=("Product", "Quantity", "Unit Price", "Total"), show='headings')
        self.product_table.heading("Product", text="Product")
        self.product_table.heading("Quantity", text="Quantity")
        self.product_table.heading("Unit Price", text="Unit Price")
        self.product_table.heading("Total", text="Total")
        self.product_table.pack(fill=tk.BOTH, expand=True, pady=10)

        self.edit_button = tk.Button(self.root, text="Edit Product", command=self.edit_product)
        self.edit_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.delete_button = tk.Button(self.root, text="Delete Product", command=self.delete_product)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Bill Summary
        self.total_label = tk.Label(self.root, text="Total: $0.00")
        self.total_label.pack(pady=5)

        self.gst_label = tk.Label(self.root, text="GST (18%): $0.00")
        self.gst_label.pack(pady=5)

        self.grand_total_label = tk.Label(self.root, text="Grand Total: $0.00")
        self.grand_total_label.pack(pady=5)

        self.generate_invoice_button = tk.Button(self.root, text="Generate Invoice", command=self.generate_invoice)
        self.generate_invoice_button.pack(pady=10)

        self.save_invoice_button = tk.Button(self.root, text="Save Invoice", command=self.save_invoice)
        self.save_invoice_button.pack(pady=10)

        # GST Rate Management
        tk.Label(self.root, text="GST Rate (%):").pack(pady=5)
        self.gst_rate_entry = tk.Entry(self.root, width=10)
        self.gst_rate_entry.insert(0, str(self.gst_rate))
        self.gst_rate_entry.pack(pady=5)
        self.update_gst_rate_button = tk.Button(self.root, text="Update GST Rate", command=self.update_gst_rate)
        self.update_gst_rate_button.pack(pady=10)

        # Search Functionality
        tk.Label(self.root, text="Search Product:").pack(pady=5)
        self.search_entry = tk.Entry(self.root, width=50)
        self.search_entry.pack(pady=5)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_product)
        self.search_button.pack(pady=5)

    def add_product(self):
        name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        unit_price = self.unit_price_entry.get()

        if name and quantity.isdigit() and unit_price.replace('.', '', 1).isdigit():
            quantity = int(quantity)
            unit_price = float(unit_price)
            total = quantity * unit_price
            self.products.append({"name": name, "quantity": quantity, "unit_price": unit_price, "total": total})

            self.product_table.insert("", tk.END, values=(name, quantity, unit_price, total))
            self.update_summary()
        else:
            messagebox.showerror("Error", "Please enter valid product details")

    def edit_product(self):
        selected_item = self.product_table.selection()
        if selected_item:
            item = self.product_table.item(selected_item)
            name = item['values'][0]
            quantity = item['values'][1]
            unit_price = item['values'][2]

            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Product")
            edit_window.geometry("300x200")

            tk.Label(edit_window, text="Product Name:").pack(pady=5)
            name_entry = tk.Entry(edit_window, width=30)
            name_entry.pack(pady=5)
            name_entry.insert(0, name)

            tk.Label(edit_window, text="Quantity:").pack(pady=5)
            quantity_entry = tk.Entry(edit_window, width=30)
            quantity_entry.pack(pady=5)
            quantity_entry.insert(0, quantity)

            tk.Label(edit_window, text="Unit Price:").pack(pady=5)
            unit_price_entry = tk.Entry(edit_window, width=30)
            unit_price_entry.pack(pady=5)
            unit_price_entry.insert(0, unit_price)

            def save_changes():
                new_name = name_entry.get()
                new_quantity = quantity_entry.get()
                new_unit_price = unit_price_entry.get()
                if new_name and new_quantity.isdigit() and new_unit_price.replace('.', '', 1).isdigit():
                    new_quantity = int(new_quantity)
                    new_unit_price = float(new_unit_price)
                    new_total = new_quantity * new_unit_price

                    index = self.product_table.index(selected_item[0])
                    self.products[index] = {"name": new_name, "quantity": new_quantity, "unit_price": new_unit_price, "total": new_total}
                    self.display_products()
                    edit_window.destroy()
                else:
                    messagebox.showerror("Error", "Please enter valid product details")

            tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=20)
        else:
            messagebox.showerror("Error", "Please select a product to edit")

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

    def display_products(self):
        self.product_table.delete(*self.product_table.get_children())
        for product in self.products:
            self.product_table.insert("", tk.END, values=(product['name'], product['quantity'], product['unit_price'], product['total']))
        self.update_summary()

    def display_filtered_products(self, products):
        self.product_table.delete(*self.product_table.get_children())
        for product in products:
            self.product_table.insert("", tk.END, values=(product['name'], product['quantity'], product['unit_price'], product['total']))

    def update_summary(self):
        total_amount = sum(product['total'] for product in self.products)
        gst_amount = total_amount * (self.gst_rate / 100)
        grand_total = total_amount + gst_amount

        self.total_label.config(text=f"Total: ${total_amount:.2f}")
        self.gst_label.config(text=f"GST ({self.gst_rate}%): ${gst_amount:.2f}")
        self.grand_total_label.config(text=f"Grand Total: ${grand_total:.2f}")

    def generate_invoice(self):
        invoice = {
            "company": self.company_name_entry.get(),
            "address": self.company_address_entry.get(),
            "products": self.products,
            "total": self.total_label.cget("text"),
            "gst": self.gst_label.cget("text"),
            "grand_total": self.grand_total_label.cget("text")
        }
        invoice_text = json.dumps(invoice, indent=4)
        self.invoice_text = invoice_text
        messagebox.showinfo("Invoice Generated", "Invoice has been generated. You can now save it.")

    def save_invoice(self):
        if hasattr(self, 'invoice_text'):
            file_type = [('JSON files', '*.json'), ('PDF files', '*.pdf')]
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=file_type)
            if file_path:
                if file_path.endswith('.json'):
                    with open(file_path, 'w') as file:
                        file.write(self.invoice_text)
                elif file_path.endswith('.pdf'):
                    self.generate_pdf(file_path)
                messagebox.showinfo("Success", "Invoice saved successfully")
        else:
            messagebox.showerror("Error", "No invoice to save. Generate an invoice first.")

    def update_gst_rate(self):
        new_rate = self.gst_rate_entry.get()
        if new_rate.replace('.', '', 1).isdigit():
            self.gst_rate = float(new_rate)
            self.update_summary()
        else:
            messagebox.showerror("Error", "Please enter a valid GST rate")

    def generate_pdf(self, file_path):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt=f"Company: {self.company_name_entry.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Address: {self.company_address_entry.get()}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)

        pdf.cell(200, 10, txt="Products:", ln=True)
        for product in self.products:
            pdf.cell(200, 10, txt=f"{product['name']} | {product['quantity']} | {product['unit_price']} | {product['total']}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)

        pdf.cell(200, 10, txt=f"Total: {self.total_label.cget('text')}", ln=True)
        pdf.cell(200, 10, txt=f"GST ({self.gst_rate}%): {self.gst_label.cget('text')}", ln=True)
        pdf.cell(200, 10, txt=f"Grand Total: {self.grand_total_label.cget('text')}", ln=True)

        pdf.output(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = GSTBillingApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import sqlite3

# Initialize Database
def init_db():
    conn = sqlite3.connect('hotel_management.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL,
            price REAL NOT NULL,
            available BOOLEAN NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT NOT NULL,
            guest_name TEXT NOT NULL,
            check_in TEXT NOT NULL,
            check_out TEXT NOT NULL,
            FOREIGN KEY (room_number) REFERENCES rooms (room_number)
        )
    ''')
    conn.commit()
    conn.close()

# GUI
class HotelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("800x600")
        self.root.configure(bg='#e6e6e6')

        self.title_label = tk.Label(root, text="Hotel Management System", font=("Helvetica", 16), bg='#e6e6e6')
        self.title_label.pack(pady=10)

        # Create a main frame
        self.main_frame = tk.Frame(root, bg='#e6e6e6')
        self.main_frame.pack(pady=20)

        self.button_frame = tk.Frame(self.main_frame, bg='#e6e6e6')
        self.button_frame.grid(row=0, column=0, padx=10, pady=10)

        self.add_room_button = tk.Button(self.button_frame, text="Add Room", command=self.add_room, bg='#4CAF50', fg='white')
        self.add_room_button.grid(row=0, column=0, padx=5, pady=5)

        self.update_room_button = tk.Button(self.button_frame, text="Update Room", command=self.update_room, bg='#FFC107', fg='white')
        self.update_room_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_room_button = tk.Button(self.button_frame, text="Delete Room", command=self.delete_room, bg='#FF5722', fg='white')
        self.delete_room_button.grid(row=0, column=2, padx=5, pady=5)

        self.book_room_button = tk.Button(self.button_frame, text="Book Room", command=self.book_room, bg='#2196F3', fg='white')
        self.book_room_button.grid(row=1, column=0, padx=5, pady=5)

        self.check_out_button = tk.Button(self.button_frame, text="Check-Out Room", command=self.check_out, bg='#9C27B0', fg='white')
        self.check_out_button.grid(row=1, column=1, padx=5, pady=5)

        self.view_bookings_button = tk.Button(self.button_frame, text="View Bookings", command=self.view_bookings, bg='#FF9800', fg='white')
        self.view_bookings_button.grid(row=1, column=2, padx=5, pady=5)

        self.check_availability_button = tk.Button(self.button_frame, text="Check Availability", command=self.check_availability, bg='#4CAF50', fg='white')
        self.check_availability_button.grid(row=2, column=0, padx=5, pady=5)

        self.search_bookings_button = tk.Button(self.button_frame, text="Search Bookings", command=self.search_bookings, bg='#607D8B', fg='white')
        self.search_bookings_button.grid(row=2, column=1, padx=5, pady=5)

    def add_room(self):
        room_number = simpledialog.askstring("Input", "Enter room number:")
        room_type = simpledialog.askstring("Input", "Enter room type (e.g., Single, Double):")
        price = simpledialog.askfloat("Input", "Enter room price:")
        if room_number and room_type and price is not None:
            conn = sqlite3.connect('hotel_management.db')
            c = conn.cursor()
            try:
                c.execute('''
                    INSERT INTO rooms (room_number, type, price, available)
                    VALUES (?, ?, ?, ?)
                ''', (room_number, room_type, price, True))
                conn.commit()
                messagebox.showinfo("Success", "Room added successfully!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Room number already exists!")
            finally:
                conn.close()

    def update_room(self):
        room_number = simpledialog.askstring("Input", "Enter room number to update:")
        conn = sqlite3.connect('hotel_management.db')
        c = conn.cursor()
        c.execute('SELECT * FROM rooms WHERE room_number = ?', (room_number,))
        room = c.fetchone()
        if room:
            new_room_number = simpledialog.askstring("Input", "Enter new room number:", initialvalue=room[1])
            new_type = simpledialog.askstring("Input", "Enter new room type:", initialvalue=room[2])
            new_price = simpledialog.askfloat("Input", "Enter new room price:", initialvalue=room[3])
            if new_room_number and new_type and new_price is not None:
                c.execute('''
                    UPDATE rooms SET room_number = ?, type = ?, price = ?
                    WHERE room_number = ?
                ''', (new_room_number, new_type, new_price, room_number))
                conn.commit()
                messagebox.showinfo("Success", "Room details updated successfully!")
            else:
                messagebox.showerror("Error", "All fields are required.")
        else:
            messagebox.showerror("Error", "Room not found!")
        conn.close()

    def delete_room(self):
        room_number = simpledialog.askstring("Input", "Enter room number to delete:")
        conn = sqlite3.connect('hotel_management.db')
        c = conn.cursor()
        c.execute('SELECT * FROM rooms WHERE room_number = ?', (room_number,))
        room = c.fetchone()
        if room:
            c.execute('DELETE FROM rooms WHERE room_number = ?', (room_number,))
            c.execute('DELETE FROM bookings WHERE room_number = ?', (room_number,))
            conn.commit()
            messagebox.showinfo("Success", "Room deleted successfully!")
        else:
            messagebox.showerror("Error", "Room not found!")
        conn.close()

    def book_room(self):
        room_number = simpledialog.askstring("Input", "Enter room number:")
        guest_name = simpledialog.askstring("Input", "Enter guest name:")
        check_in = simpledialog.askstring("Input", "Enter check-in date (YYYY-MM-DD):")
        check_out = simpledialog.askstring("Input", "Enter check-out date (YYYY-MM-DD):")

        if room_number and guest_name and check_in and check_out:
            conn = sqlite3.connect('hotel_management.db')
            c = conn.cursor()
            c.execute('SELECT available FROM rooms WHERE room_number = ?', (room_number,))
            result = c.fetchone()
            if result and result[0]:
                c.execute('''
                    INSERT INTO bookings (room_number, guest_name, check_in, check_out)
                    VALUES (?, ?, ?, ?)
                ''', (room_number, guest_name, check_in, check_out))
                c.execute('UPDATE rooms SET available = ? WHERE room_number = ?', (False, room_number))
                conn.commit()
                messagebox.showinfo("Success", "Room booked successfully!")
            else:
                messagebox.showerror("Error", "Room is not available or does not exist!")
            conn.close()

    def check_out(self):
        room_number = simpledialog.askstring("Input", "Enter room number to check-out:")
        conn = sqlite3.connect('hotel_management.db')
        c = conn.cursor()
        c.execute('SELECT available FROM rooms WHERE room_number = ?', (room_number,))
        result = c.fetchone()
        if result is not None:
            if not result[0]:
                c.execute('UPDATE rooms SET available = ? WHERE room_number = ?', (True, room_number))
                conn.commit()
                messagebox.showinfo("Success", "Room checked out successfully!")
            else:
                messagebox.showerror("Error", "Room is already available or does not exist!")
        else:
            messagebox.showerror("Error", "Room not found!")
        conn.close()

    def view_bookings(self):
        conn = sqlite3.connect('hotel_management.db')
        c = conn.cursor()
        c.execute('SELECT * FROM bookings')
        bookings = c.fetchall()
        conn.close()

        if bookings:
            booking_list = "\n".join([f"Booking ID: {b[0]}, Room: {b[1]}, Guest: {b[2]}, Check-In: {b[3]}, Check-Out: {b[4]}" for b in bookings])
            messagebox.showinfo("Bookings", booking_list)
        else:
            messagebox.showinfo("Bookings", "No bookings found.")

    def check_availability(self):
        room_type = simpledialog.askstring("Input", "Enter room type to check availability (e.g., Single, Double):")
        if room_type:
            conn = sqlite3.connect('hotel_management.db')
            c = conn.cursor()
            c.execute('SELECT room_number FROM rooms WHERE type = ? AND available = ?', (room_type, True))
            available_rooms = c.fetchall()
            conn.close()

            if available_rooms:
                available_rooms_list = "\n".join([room[0] for room in available_rooms])
                messagebox.showinfo("Available Rooms", f"Available rooms for type {room_type}:\n{available_rooms_list}")
            else:
                messagebox.showinfo("Available Rooms", f"No available rooms for type {room_type}.")

    def search_bookings(self):
        search_term = simpledialog.askstring("Input", "Enter guest name or room number to search:")
        conn = sqlite3.connect('hotel_management.db')
        c = conn.cursor()
        c.execute('''
            SELECT * FROM bookings WHERE guest_name LIKE ? OR room_number LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%'))
        results = c.fetchall()
        conn.close()

        if results:
            results_list = "\n".join([f"Booking ID: {r[0]}, Room: {r[1]}, Guest: {r[2]}, Check-In: {r[3]}, Check-Out: {r[4]}" for r in results])
            messagebox.showinfo("Search Results", results_list)
        else:
            messagebox.showinfo("Search Results", "No bookings found.")

# Initialize the app
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = HotelManagementApp(root)
    root.mainloop()

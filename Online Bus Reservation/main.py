import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import sqlite3

# Initialize Database
def init_db():
    conn = sqlite3.connect('bus_reservation.db')
    c = conn.cursor()
    
    # Create table for buses
    c.execute('''
        CREATE TABLE IF NOT EXISTS buses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_number TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            total_seats INTEGER NOT NULL,
            available_seats INTEGER NOT NULL
        )
    ''')
    
    # Create table for reservations
    c.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_number TEXT NOT NULL,
            passenger_name TEXT NOT NULL,
            seat_number INTEGER NOT NULL,
            FOREIGN KEY (bus_number) REFERENCES buses (bus_number)
        )
    ''')
    
    conn.commit()
    conn.close()

# GUI
class BusReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Bus Reservation System")
        self.root.geometry("800x600")
        self.root.configure(bg='#f5f5f5')

        self.title_label = tk.Label(root, text="Online Bus Reservation System", font=("Helvetica", 16), bg='#f5f5f5')
        self.title_label.pack(pady=10)

        # Create a main frame
        self.main_frame = tk.Frame(root, bg='#f5f5f5')
        self.main_frame.pack(pady=20)

        self.button_frame = tk.Frame(self.main_frame, bg='#f5f5f5')
        self.button_frame.grid(row=0, column=0, padx=10, pady=10)

        self.add_bus_button = tk.Button(self.button_frame, text="Add Bus", command=self.add_bus, bg='#4CAF50', fg='white')
        self.add_bus_button.grid(row=0, column=0, padx=5, pady=5)

        self.update_bus_button = tk.Button(self.button_frame, text="Update Bus", command=self.update_bus, bg='#FFC107', fg='white')
        self.update_bus_button.grid(row=0, column=1, padx=5, pady=5)

        self.delete_bus_button = tk.Button(self.button_frame, text="Delete Bus", command=self.delete_bus, bg='#FF5722', fg='white')
        self.delete_bus_button.grid(row=0, column=2, padx=5, pady=5)

        self.book_seat_button = tk.Button(self.button_frame, text="Book Seat", command=self.book_seat, bg='#2196F3', fg='white')
        self.book_seat_button.grid(row=1, column=0, padx=5, pady=5)

        self.cancel_reservation_button = tk.Button(self.button_frame, text="Cancel Reservation", command=self.cancel_reservation, bg='#9C27B0', fg='white')
        self.cancel_reservation_button.grid(row=1, column=1, padx=5, pady=5)

        self.view_buses_button = tk.Button(self.button_frame, text="View Buses", command=self.view_buses, bg='#FF9800', fg='white')
        self.view_buses_button.grid(row=1, column=2, padx=5, pady=5)

        self.search_reservations_button = tk.Button(self.button_frame, text="Search Reservations", command=self.search_reservations, bg='#607D8B', fg='white')
        self.search_reservations_button.grid(row=2, column=0, padx=5, pady=5)

    def add_bus(self):
        bus_number = simpledialog.askstring("Input", "Enter bus number:")
        source = simpledialog.askstring("Input", "Enter source:")
        destination = simpledialog.askstring("Input", "Enter destination:")
        departure_time = simpledialog.askstring("Input", "Enter departure time (YYYY-MM-DD HH:MM):")
        arrival_time = simpledialog.askstring("Input", "Enter arrival time (YYYY-MM-DD HH:MM):")
        total_seats = simpledialog.askinteger("Input", "Enter total number of seats:")
        available_seats = total_seats
        
        if all([bus_number, source, destination, departure_time, arrival_time, total_seats is not None]):
            conn = sqlite3.connect('bus_reservation.db')
            c = conn.cursor()
            try:
                c.execute('''
                    INSERT INTO buses (bus_number, source, destination, departure_time, arrival_time, total_seats, available_seats)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (bus_number, source, destination, departure_time, arrival_time, total_seats, available_seats))
                conn.commit()
                messagebox.showinfo("Success", "Bus added successfully!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Bus number already exists!")
            finally:
                conn.close()

    def update_bus(self):
        bus_number = simpledialog.askstring("Input", "Enter bus number to update:")
        conn = sqlite3.connect('bus_reservation.db')
        c = conn.cursor()
        c.execute('SELECT * FROM buses WHERE bus_number = ?', (bus_number,))
        bus = c.fetchone()
        if bus:
            new_source = simpledialog.askstring("Input", "Enter new source:", initialvalue=bus[2])
            new_destination = simpledialog.askstring("Input", "Enter new destination:", initialvalue=bus[3])
            new_departure_time = simpledialog.askstring("Input", "Enter new departure time (YYYY-MM-DD HH:MM):", initialvalue=bus[4])
            new_arrival_time = simpledialog.askstring("Input", "Enter new arrival time (YYYY-MM-DD HH:MM):", initialvalue=bus[5])
            new_total_seats = simpledialog.askinteger("Input", "Enter new total number of seats:", initialvalue=bus[6])
            new_available_seats = simpledialog.askinteger("Input", "Enter new available number of seats:", initialvalue=bus[7])
            
            if all([new_source, new_destination, new_departure_time, new_arrival_time, new_total_seats is not None, new_available_seats is not None]):
                c.execute('''
                    UPDATE buses SET source = ?, destination = ?, departure_time = ?, arrival_time = ?, total_seats = ?, available_seats = ?
                    WHERE bus_number = ?
                ''', (new_source, new_destination, new_departure_time, new_arrival_time, new_total_seats, new_available_seats, bus_number))
                conn.commit()
                messagebox.showinfo("Success", "Bus details updated successfully!")
            else:
                messagebox.showerror("Error", "All fields are required.")
        else:
            messagebox.showerror("Error", "Bus not found!")
        conn.close()

    def delete_bus(self):
        bus_number = simpledialog.askstring("Input", "Enter bus number to delete:")
        conn = sqlite3.connect('bus_reservation.db')
        c = conn.cursor()
        c.execute('SELECT * FROM buses WHERE bus_number = ?', (bus_number,))
        bus = c.fetchone()
        if bus:
            c.execute('DELETE FROM buses WHERE bus_number = ?', (bus_number,))
            c.execute('DELETE FROM reservations WHERE bus_number = ?', (bus_number,))
            conn.commit()
            messagebox.showinfo("Success", "Bus deleted successfully!")
        else:
            messagebox.showerror("Error", "Bus not found!")
        conn.close()

    def book_seat(self):
        bus_number = simpledialog.askstring("Input", "Enter bus number:")
        passenger_name = simpledialog.askstring("Input", "Enter passenger name:")
        seat_number = simpledialog.askinteger("Input", "Enter seat number:")
        
        if bus_number and passenger_name and seat_number is not None:
            conn = sqlite3.connect('bus_reservation.db')
            c = conn.cursor()
            c.execute('SELECT available_seats FROM buses WHERE bus_number = ?', (bus_number,))
            result = c.fetchone()
            if result:
                available_seats = result[0]
                if available_seats > 0:
                    c.execute('''
                        INSERT INTO reservations (bus_number, passenger_name, seat_number)
                        VALUES (?, ?, ?)
                    ''', (bus_number, passenger_name, seat_number))
                    c.execute('UPDATE buses SET available_seats = ? WHERE bus_number = ?', (available_seats - 1, bus_number))
                    conn.commit()
                    messagebox.showinfo("Success", "Seat booked successfully!")
                else:
                    messagebox.showerror("Error", "No available seats!")
            else:
                messagebox.showerror("Error", "Bus not found!")
            conn.close()

    def cancel_reservation(self):
        reservation_id = simpledialog.askinteger("Input", "Enter reservation ID to cancel:")
        conn = sqlite3.connect('bus_reservation.db')
        c = conn.cursor()
        c.execute('SELECT bus_number, seat_number FROM reservations WHERE id = ?', (reservation_id,))
        reservation = c.fetchone()
        if reservation:
            bus_number, seat_number = reservation
            c.execute('DELETE FROM reservations WHERE id = ?', (reservation_id,))
            c.execute('UPDATE buses SET available_seats = available_seats + 1 WHERE bus_number = ?', (bus_number,))
            conn.commit()
            messagebox.showinfo("Success", "Reservation canceled successfully!")
        else:
            messagebox.showerror("Error", "Reservation not found!")
        conn.close()

    def view_buses(self):
        conn = sqlite3.connect('bus_reservation.db')
        c = conn.cursor()
        c.execute('SELECT * FROM buses')
        buses = c.fetchall()
        conn.close()

        if buses:
            bus_list = "\n".join([f"Bus Number: {b[1]}, Source: {b[2]}, Destination: {b[3]}, Departure: {b[4]}, Arrival: {b[5]}, Total Seats: {b[6]}, Available Seats: {b[7]}" for b in buses])
            messagebox.showinfo("Buses", bus_list)
        else:
            messagebox.showinfo("Buses", "No buses available.")

    def search_reservations(self):
        search_term = simpledialog.askstring("Input", "Enter bus number or passenger name to search:")
        conn = sqlite3.connect('bus_reservation.db')
        c = conn.cursor()
        c.execute('''
            SELECT * FROM reservations WHERE bus_number LIKE ? OR passenger_name LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%'))
        results = c.fetchall()
        conn.close()

        if results:
            results_list = "\n".join([f"Reservation ID: {r[0]}, Bus Number: {r[1]}, Passenger: {r[2]}, Seat Number: {r[3]}" for r in results])
            messagebox.showinfo("Search Results", results_list)
        else:
            messagebox.showinfo("Search Results", "No reservations found.")

# Initialize the app
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = BusReservationApp(root)
    root.mainloop()

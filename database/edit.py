import tkinter as tk
from tkinter import messagebox
import pyodbc

# Function to retrieve and display all user data from SQL Server
def retrieve_user_data():
    username = username_entry.get()

    # Establish a connection to your SQL Server database
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-TJJ8VK0K;DATABASE=KonkorRegistration;Trusted_Connection=yes;')
    cursor = conn.cursor()

    try:
        # Execute SQL query to retrieve all user data
        cursor.execute(f"SELECT * FROM RegistrationDetails WHERE FirstName=N'{username}'")
        user_data = cursor.fetchone()

        if user_data:
            # Display all information using messagebox
            info_message = f"User Information:\n\n"
            for column_name, column_value in zip(cursor.description, user_data):
                info_message += f"{column_name[0]}: {column_value}\n"

            messagebox.showinfo("User Information", info_message)
        else:
            messagebox.showerror("Error", "User not found!")

    except pyodbc.Error as e:
        messagebox.showerror("Error", f"Error retrieving user data: {e}")

    finally:
        conn.close()

# GUI setup
root = tk.Tk()
root.title("User Information Retrieval")

# Username entry
username_label = tk.Label(root, text="Enter your name:")
username_label.pack(pady=10)
username_entry = tk.Entry(root)
username_entry.pack(pady=10)

# Button to retrieve user data
retrieve_button = tk.Button(root, text="Retrieve User Data", command=retrieve_user_data)
retrieve_button.pack(pady=20)

# Run the GUI
root.mainloop()

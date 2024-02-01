import tkinter as tk
from tkinter import messagebox
import pyodbc

# Database Connection
def connect_to_db():
    connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-TJJ8VK0K;DATABASE=KonkorRegistration;Trusted_Connection=yes;'
    connection = pyodbc.connect(connection_string)\
    
    return connection
# Sign Up User
def sign_up_user(username, password, email):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (Username, Password, Email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        messagebox.showinfo("Success", "Sign up successful")
    except pyodbc.Error as e:
        messagebox.showerror("Error", "Failed to sign up: " + str(e))
    finally:
        cursor.close()
        conn.close()
# Login User
def login_user(username, password):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT UserID FROM Users WHERE Username = ? AND Password = ?", (username, password))
        user_id = cursor.fetchone()
        if user_id:
            open_konkoor_registration_form() # Open Konkoor Registration Form
        else:
            messagebox.showerror("Error", "Login failed: Incorrect username or password")
    except pyodbc.Error as e:
        messagebox.showerror("Error", "Failed to login: " + str(e))
    finally:
        cursor.close()
        conn.close()

# Open Konkoor Registration Form
def open_konkoor_registration_form():
    def submit_form():
        try:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO RegistrationDetails (
                    codemelli, FirstName, LastName, FatherName, shomareh_shenasnameh, 
                    sodoor_shensnameh_id, gender, BirthDate, EducationCode_id, 
                    ExamCode_id, PostalCode, MobilePhone, HomePhone, Email
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    form_entries['codemelli'].get(),
                    form_entries['FirstName'].get(),
                    form_entries['LastName'].get(),
                    form_entries['FatherName'].get(),
                    form_entries['shomareh shenasnameh'].get(),
                    int(form_entries['sodoor shensnameh_id'].get()), # Casted to int
                    form_entries['gender'].get(),
                    form_entries['BirthDate'].get(),
                    int(form_entries['EducationCode_id'].get()), # Casted to int
                    int(form_entries['ExamCode_id'].get()) if form_entries['ExamCode_id'].get() else None, # Casted to int or None
                    form_entries['PostalCode'].get(),
                    form_entries['MobilePhone'].get(),
                    form_entries['HomePhone'].get(),
                    form_entries['Email'].get()
                )
            )
            conn.commit()
            messagebox.showinfo("Success", "Successfully registered for Konkoor.")
        except pyodbc.Error as e:
            messagebox.showerror("Error", "Failed to register for Konkoor: " + str(e))
        finally:
            cursor.close()
            conn.close()

    konkoor_window = tk.Toplevel()
    konkoor_window.title("Konkoor Registration Form")

    # Define form fields
    fields = ['codemelli', 'FirstName', 'LastName', 'FatherName', 'shomareh shenasnameh','sodoor shensnameh_id','gender',
              'BirthDate', 'EducationCode_id', 'ExamCode_id', 'PostalCode',
              'MobilePhone', 'HomePhone', 'Email']

    form_entries = {}
    for field in fields:
        row = tk.Frame(konkoor_window)
        label = tk.Label(row, width=15, text=field.replace('_', ' '), anchor='w')
        entry = tk.Entry(row)
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        label.pack(side=tk.LEFT)
        entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        form_entries[field] = entry

    submit_button = tk.Button(konkoor_window, text="Submit", command=submit_form)
    submit_button.pack()

# Create Login and Sign Up Windows
def create_login_window():
    login_window = tk.Toplevel(root)
    login_window.title("Login")
    tk.Label(login_window, text="Username").grid(row=0, column=0)
    tk.Label(login_window, text="Password").grid(row=1, column=0)

    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)

    login_button = tk.Button(login_window, text="Login", command=lambda: login_user(username_entry.get(), password_entry.get()))
    login_button.grid(row=2, column=0, columnspan=2)

def create_sign_up_window():
    sign_up_window = tk.Toplevel(root)
    sign_up_window.title("Sign Up")
    tk.Label(sign_up_window, text="Username").grid(row=0, column=0)
    tk.Label(sign_up_window, text="Password").grid(row=1, column=0)
    tk.Label(sign_up_window, text="Email").grid(row=2, column=0)

    username_entry = tk.Entry(sign_up_window)
    username_entry.grid(row=0, column=1)
    password_entry = tk.Entry(sign_up_window, show="*")
    password_entry.grid(row=1, column=1)
    email_entry = tk.Entry(sign_up_window)
    email_entry.grid(row=2, column=1)

    sign_up_button = tk.Button(sign_up_window,
                               text="Sign Up",
                               command=lambda: sign_up_user(username_entry.get(), password_entry.get(), email_entry.get()))
    sign_up_button.grid(row=3, column=0, columnspan=2)

# Main Application Window
root = tk.Tk()
root.title("Konkoor Registration System")
tk.Button(root, text="Login", command=create_login_window).pack()
tk.Button(root, text="Sign Up", command=create_sign_up_window).pack()
root.mainloop()
from tkinter import *
import customtkinter as ctk
import tkinter.messagebox as tkmb
import mysql.connector

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1350x700+0+0")
app.title("LOGIN")

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'harsh@123',
    'database': 'assettracking'
}
import subprocess

def login():
    # Get username and password from the entry fields
    entered_username = user_entry.get()
    entered_password = user_pass.get()

    print("Entered Username:", entered_username)  # Debug print

    # Connect to the database
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Query to fetch user details based on name
        query = "SELECT * FROM users WHERE name = %s"
        cursor.execute(query, (entered_username,))

        user_data = cursor.fetchone()

        if user_data:
            db_username, db_password = user_data[1], user_data[5]  # Assuming the 'name' and 'password' columns are at index 1 and 5 respectively
            if entered_password == db_password:
                tkmb.showinfo(title="Login Successful", message="Welcome to Asset Management System")
                # Open the dashboard.py script
                subprocess.Popen(["python", "dashboard.py"])
                app.destroy()  # Close the login window
            else:
                tkmb.showerror(title="Login Failed", message="Incorrect password")
        else:
            tkmb.showerror(title="Login Failed", message="User not found")

    except mysql.connector.Error as err:
        print("Database Error:", err)
        tkmb.showerror(title="Database Error", message="Could not connect to the database")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


label = ctk.CTkLabel(app, text="LOGIN", font=("times new roman", 45, "bold"))
label.pack(pady=20)

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

label = ctk.CTkLabel(master=frame, text='Please Enter Username & Password')
label.pack(pady=12, padx=10)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Username")
user_entry.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
user_pass.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text='Login', command=login)
button.pack(pady=12, padx=10)

checkbox = ctk.CTkCheckBox(master=frame, text='Remember Me')
checkbox.pack(pady=12, padx=10)

app.mainloop()

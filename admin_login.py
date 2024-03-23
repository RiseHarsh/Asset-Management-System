from tkinter import *
import customtkinter as ctk
import tkinter.messagebox as tkmb
import subprocess

# Function to handle login
def login():
    # Get email and password from the entry fields
    entered_email = user_entry.get()
    entered_password = user_pass.get()

    if entered_email == "admin@gmail.com" and entered_password == "admin123":
        tkmb.showinfo(title="Login Successful", message="Welcome to Asset Management System")
        # Open the admin_dashboard.py script
        subprocess.Popen(["python", "admin_dashboard.py"])
        app.destroy()  # Close the login window
    else:
        tkmb.showerror(title="Login Failed", message="Incorrect email or password")

# Function to go back to the previous page
def go_back():
    # Add functionality to go back to the previous page (replace "previous_page.py" with the actual previous page)
    subprocess.Popen(["python", "previous_page.py"])
    app.destroy()  # Close the current window

# Initialize the application window
app = ctk.CTk()
app.geometry("1350x700+0+0")
app.title("LOGIN")

# Create "Go back" button
back_button = Button(app, text="⬅", command=go_back, font=("times new roman", 15), bg="#03A9F4")
back_button.place(x=10, y=10)

# Create label, frame, entry fields, and login button
label = ctk.CTkLabel(app, text=" ADMIN LOGIN", font=("times new roman", 45, "bold"))
label.pack(pady=20)

frame = ctk.CTkFrame(master=app)
frame.pack(pady=20, padx=40, fill='both', expand=True)

label = ctk.CTkLabel(master=frame, text='Please Enter Email & Password')
label.pack(pady=12, padx=10)

user_entry = ctk.CTkEntry(master=frame, placeholder_text="Email")
user_entry.pack(pady=12, padx=10)

user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
user_pass.pack(pady=12, padx=10)

button = ctk.CTkButton(master=frame, text='Login', command=login)
button.pack(pady=12, padx=10)

app.mainloop()

import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from PIL import Image, ImageTk
import subprocess
from check_assets import check_assets

def open_statistics():
    subprocess.Popen(["python", "statistics.py"])

def logout():
    root.destroy()
    subprocess.Popen(["python","common_login.py"])

def run_api():
    subprocess.Popen(["python", "add_assets.py"])

def exit_fullscreen():
    root.attributes('-fullscreen', False)  # Disable fullscreen
    root.destroy()  # Destroy the window

# Create main window
root = tk.Tk()
root.title("Asset Tracking Management System")

# Set window size to 1920x1080
root.geometry("1920x1080")

# Load and resize background image
background_image = Image.open("images/asset4.jpg")
background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
background_photo = ImageTk.PhotoImage(background_image)

# Create label to display background image
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Create a frame to hold other widgets
frame = tk.Frame(root, bg="lightblue")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Create buttons, labels, etc. inside the frame as per your requirement
label = tk.Label(frame, text="Asset Tracking Management System", font=("times new roman", 30, "underline"), bg="lightblue")
label.place(relx=0.5, rely=0.05, anchor="n")

# Load profile image
profile_image = tk.PhotoImage(file="images/logo.png")
profile_image = profile_image.subsample(4)

# Create profile icon
canvas = tk.Canvas(root, width=100, height=100)
canvas.pack(padx=60, pady=20, anchor='nw')
canvas.create_image(50, 50, image=profile_image)

# Create frame to hold buttons
button_frame = tk.Frame(root, bg="light blue")
button_frame.pack(side=tk.LEFT, padx=20, pady=20, anchor='nw')

# Create menu buttons
add_assets_btn = tk.Button(button_frame, text="Add Assets", padx=20, pady=10, font=('Arial', 14), command=run_api, bd=0, bg="light blue")
add_assets_btn.pack(fill=tk.X, padx=10, pady=5)

check_assets_btn = tk.Button(button_frame, text="Check Assets", padx=20, pady=10, font=('Arial', 14), command=check_assets, bd=0, bg="light blue")
check_assets_btn.pack(fill=tk.X, padx=10, pady=5)

statistics_btn = tk.Button(button_frame, text="Statistics", padx=20, pady=10, font=('Arial', 14), command=open_statistics, bd=0, bg="light blue")
statistics_btn.pack(fill=tk.X, padx=10, pady=5)

help_btn = tk.Button(button_frame, text="Help!", padx=20, pady=10, font=('Arial', 14), bd=0, bg="light blue")
help_btn.pack(fill=tk.X, padx=10, pady=5)

# Create logout button
logout_btn = tk.Button(root, text="Logout", padx=5, pady=5, font=('Arial', 14), command=logout, bg="light blue")
logout_btn.place(relx=1.0, rely=0.0, anchor='ne', x=-20, y=60)

# Create exit button
exit_btn = tk.Button(root, text="Exit", padx=65, pady=10, font=('Arial', 14), command=exit_fullscreen, bg="light blue")
exit_btn.place(relx=1.0, rely=0.0, anchor='n', x=-1420, y=515)


root.mainloop()

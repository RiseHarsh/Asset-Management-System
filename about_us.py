import tkinter as tk

# Create the main window
root = tk.Tk()

# Set window title
root.title("About Us")

# Calculate the dimensions of the window
window_width = 800
window_height = 400

# Set the window size
root.geometry(f"{window_width}x{window_height}")

# Create a Canvas widget to cover the entire window and set its background color
canvas = tk.Canvas(root, bg="light blue", width=window_width, height=window_height)
canvas.pack()

# Create a frame to hold the text boxes and set its background color
frame = tk.Frame(canvas, bg="light blue")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Calculate box dimensions
box_width = 200  # Reduced box width
box_height = 150  # Set height to 150 pixels

# Calculate horizontal and vertical spacing
horizontal_spacing = 30  # Increased horizontal spacing
vertical_spacing = 30

# Calculate the initial x-coordinate for box placement
initial_x = (window_width - 3 * box_width - 2 * horizontal_spacing) / 2

# Create a mission box
mission_box = tk.Frame(frame, width=box_width, height=box_height, relief="solid", borderwidth=2)
mission_box.grid(row=0, column=0, padx=horizontal_spacing)

mission_title_text = "MISSION"
mission_title_label = tk.Label(mission_box, text=mission_title_text, font=("Arial", 14, "bold"), fg="blue")
mission_title_label.pack(pady=(10, 0))

mission_text = "We are dedicated to providing small businesses, entrepreneurs, and individuals with an intuitive and efficient platform to manage their digital assets seamlessly."
mission_label = tk.Label(mission_box, text=mission_text, wraplength=box_width - 20, justify='left')
mission_label.pack(pady=(10, 0))

# Create a service providers box
solution_box = tk.Frame(frame, width=box_width, height=box_height, relief="solid", borderwidth=2)
solution_box.grid(row=0, column=1, padx=horizontal_spacing)

solution_title_text = "User-Friendly Solution"
solution_title_label = tk.Label(solution_box, text=solution_title_text, font=("Arial", 14, "bold"), fg="blue")
solution_title_label.pack(pady=(10, 0))

solution_text = "Our team aims to offer a user-friendly and easy-to-use application that simplifies the process of tracking and monitoring digital assets such as stocks and Bitcoin."
solution_label = tk.Label(solution_box, text=solution_text, wraplength=box_width - 20, justify='left')
solution_label.pack(pady=(10, 0))

# Create a customer satisfaction box
comm_box = tk.Frame(frame, width=box_width, height=box_height, relief="solid", borderwidth=2)
comm_box.grid(row=0, column=2, padx=horizontal_spacing)

comm_title_text = "Join Our Community"
comm_title_label = tk.Label(comm_box, text=comm_title_text, font=("Arial", 14, "bold"), fg="blue")
comm_title_label.pack(pady=(10, 0))

comm_text = "We invite you to join our community of users who are taking control of their financial future with our Asset Management System. Start managing your digital assets effectively today!"
comm_label = tk.Label(comm_box, text=comm_text, wraplength=box_width - 20, justify='left')
comm_label.pack(pady=(10, 0))

# Start the tkinter event loop
root.mainloop()

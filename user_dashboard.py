from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import subprocess
from check_assets import check_assets
import webbrowser
import os

class AMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Asset Management System")
        self.root.config(bg="#E3FDFD")

        # Load and resize background image
        bg_image = Image.open("images/ubg.png")
        bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))

        # Create a semi-transparent color
        bg_color = Image.new('RGBA', bg_image.size, (0, 0, 0, 100))

        # Blend the background image with the semi-transparent color
        self.bg_photo = Image.alpha_composite(bg_image.convert('RGBA'), bg_color)
        self.bg_photo = ImageTk.PhotoImage(self.bg_photo)

        # Create a label to hold the background image
        self.bg_label = Label(root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Make the window full screen
        self.root.attributes('-fullscreen', True)

        # Title
        self.icon_title = PhotoImage(file="images/logo1.png")
        title = Label(self.root, text="Asset Management System", image=self.icon_title, compound=LEFT,
                      font=("times new roman", 40, "bold"), bg="#71C9CE", fg="white", anchor="w", padx=20)
        title.pack(fill=X)

        # Button logout
        btn_logout = Button(self.root, text="Logout", command=self.logout, font=("times new roman", 15, "bold"),
                            bg="#579BB1", cursor="hand2")
        btn_logout.place(x=1380, y=10, height=50, width=150)

        # Adjusting colors based on background image
        self.match_colors()


        # Menu
        self.MenuLogo = Image.open("images/menu_im.png")
        self.MenuLogo = self.MenuLogo.resize((200, 200), Image.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="#A6E3E9")
        LeftMenu.place(x=0, y=70, width=200, height=250)

        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#71C9CE")
        lbl_menu.pack(side=TOP, fill=X)

        button_frame = Frame(root)
        button_frame.pack(side=LEFT, padx=2, pady=205, anchor='sw')

        # Create menu buttons
        add_assets_btn = Button(button_frame, text="Add Assets", padx=22, pady=5, font=('Arial', 14),
                                command=self.run_api, bg="#9DA0A7")
        add_assets_btn.pack(fill=X, padx=10, pady=5, anchor='w')

        check_assets_btn = Button(button_frame, text="Check Assets", padx=22, pady=5, font=('Arial', 14),
                                  command=check_assets, bg="#9DA0A7")
        check_assets_btn.pack(fill=X, padx=10, pady=5, anchor='w')

        statistics_btn = Button(button_frame, text="Statistics", padx=22, pady=5, font=('Arial', 14),
                                command=self.open_statistics, bg="#9DA0A7")
        statistics_btn.pack(fill=X, padx=10, pady=5, anchor='w')

        help_btn = Button(button_frame, text="Help!", padx=22, pady=5, font=('Arial', 14), bg="#9DA0A7",
                          command=self.show_help_video)
        help_btn.pack(fill=X, padx=10, pady=5, anchor='w')

        about_us_btn = Button(button_frame, text="About Us", padx=22, pady=5, font=('Arial', 14), bg="#9DA0A7",
                              command=self.open_about_us)
        about_us_btn.pack(fill=X, padx=10, pady=5, anchor='w')

        exit_btn = Button(button_frame, text="Exit", padx=22, pady=5, font=('Arial', 14), command=self.exit_program,
                          bg="#9DA0A7")
        exit_btn.pack(fill=X, padx=10, pady=5, anchor='w')

    def match_colors(self):
        # Sample colors from the background image
        # Adjust other elements' colors accordingly
        self.root.config(bg="#9DA0A7")

    def run_api(self):
        subprocess.Popen(["python", "add_assets.py"])

    def open_statistics(self):
        subprocess.Popen(["python", "statistics.py"])

    def logout(self):
        self.root.destroy()
        subprocess.Popen(["python", "common_login.py"])

    def exit_program(self):
        root.destroy()  # Close the window


    def show_help_video(self):
        help_window = Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("800x600")

        # Embed a video player here, for example:
        # You can use a web browser to play the video from a URL or a local file
        # Here's an example of playing a YouTube video using the web browser
        # Replace 'YOUR_YOUTUBE_VIDEO_ID' with the actual YouTube video ID
        video_url = "https://youtu.be/NOwQy2WTee0?feature=shared"
        webbrowser.open(video_url)

    def open_about_us(self):
        # Open the "about_us.py" file directly
        about_us_file = "about_us.py"
        subprocess.Popen(["python", about_us_file])


if __name__ == "__main__":
    root = Tk()
    obj = AMS(root)
    root.mainloop()

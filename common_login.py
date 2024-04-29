import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import os
import smtplib
from email.mime.text import MIMEText
import random

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page | Asset Management System")
        self.root.geometry("1350x700")  # Set initial size
        self.root.config(bg="#fafafa")

        self.otp = ""
        self.logged_in_user = None

        self.phone_image = ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_Phone_image = Label(self.root, image=self.phone_image, bd=0)
        self.lbl_Phone_image.place(x=200, y=50)

        self.email = StringVar()
        self.password = StringVar()

        login_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        login_frame.place(x=650, y=90, width=350, height=460)

        title = Label(login_frame, text="Login System", font=("Elephant", 30, "bold"), bg="white")
        title.place(x=0, y=30, relwidth=1)

        lbl_user = Label(login_frame, text="Email", font=("Andalus", 15), bg="white", fg="#767171")
        lbl_user.place(x=50, y=100)
        txt_user_email = Entry(login_frame, textvariable=self.email, font=("times new roman", 15), bg="#ECECEC")
        txt_user_email.place(x=50, y=140, width=250)

        lbl_pass = Label(login_frame, text="Password", font=("Andalus", 15), bg="white", fg="#767171")
        lbl_pass.place(x=50, y=200)
        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("times new roman", 15), bg="#ECECEC")
        txt_pass.place(x=50, y=240, width=250)

        btn_login = Button(login_frame, command=self.login, text="Log In", font=("Arial Rounded MT Bold", 15),
                           bg="#00B0F0", activebackground="#00B0F0", fg="white", activeforeground="white",
                           cursor="hand2")
        btn_login.place(x=50, y=300, width=250, height=35)

        hr = Label(login_frame, bg="lightgray")
        hr.place(x=50, y=370, width=250, height=2)

        or_ = Label(login_frame, text="OR", bg="white", fg="lightgray", font=("times new roman", 15, "bold"))
        or_.place(x=150, y=355)

        btn_forget = Button(login_frame, text="Forget Password?", command=self.forget_win,
                            font=("times new roman", 13), bg="white", fg="#00759E", bd=0,
                            activebackground="white", activeforeground="#00759E")
        btn_forget.place(x=100, y=390)

        self.im1 = ImageTk.PhotoImage(file="images/im1.png")
        self.im2 = ImageTk.PhotoImage(file="images/im2.png")
        self.im3 = ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image = Label(self.root, bg="white")
        self.lbl_change_image.place(x=367, y=153, width=240, height=428)
        self.animate()

    def animate(self):
        self.im = self.im1
        self.im1 = self.im2
        self.im2 = self.im3
        self.im3 = self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000, self.animate)

    def login(self):
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="harsh@123", database="assettracking")
            cur = con.cursor()
            if self.email.get() == "" or self.password.get() == "":
                messagebox.showerror('Error', "All fields are required", parent=self.root)
            else:
                cur.execute("SELECT * FROM users WHERE email=%s AND password=%s",
                            (self.email.get(), self.password.get()))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror("Error", "Invalid USERNAME/PASSWORD", parent=self.root)
                else:
                    self.logged_in_user = user  # Set the logged-in user
                    if self.email.get() == "admin@gmail.com" and self.password.get() == "admin123":
                        self.root.destroy()
                        os.system("python admin_dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python user_dashboard.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def forget_win(self):
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="harsh@123", database="assettracking")
            cur = con.cursor()

            if self.email.get() == "":
                messagebox.showerror('Error', "Email must be required", parent=self.root)
            else:
                cur.execute("SELECT email FROM users WHERE email=%s", (self.email.get(),))
                email = cur.fetchone()
                if email is None:
                    messagebox.showerror('Error', "Invalid Email, try again", parent=self.root)
                else:
                    # Forget window
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()
                    # Call send email_function()
                    chk = self.send_email(email[0])
                    if chk == 'f':
                        messagebox.showerror("Error", "Connection Error, try again", parent=self.root)
                    else:
                        self.forget_win = Toplevel(self.root)
                        self.forget_win.title("RESET PASSWORD")
                        self.forget_win.geometry('400x350+500+180')
                        self.forget_win.focus_force()

                        title = Label(self.forget_win, text="Reset Password", font=("goudy old style", 15, 'bold'),bg="#3f51b5", fg="white")
                        title.pack(side=TOP, fill=X)
                        lbl_reset = Label(self.forget_win, text="Enter OTP Sent on Registered Email",font=("times new roman", 15)).place(x=20, y=60)
                        txt_reset = Entry(self.forget_win, textvariable=self.var_otp, font=("times new roman", 15),bg="lightyellow")
                        txt_reset.place(x=20, y=100, width=250, height=30)

                        self.btn_reset = Button(self.forget_win, text="SUBMIT", command=self.validate_otp,font=("times new roman", 15), bg="lightblue")
                        self.btn_reset.place(x=280, y=100, width=100, height=30)

                        lbl_new_pass = Label(self.forget_win, text="New Password", font=("times new roman", 15)).place( x=20, y=160)
                        txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass, show="*", font=("times new roman", 15), bg="lightyellow")
                        txt_new_pass.place(x=20, y=200, width=250, height=30)

                        lbl_conf_pass = Label(self.forget_win, text="Confirm Password", font=("times new roman", 15)).place(x=20, y=240)
                        txt_conf_pass = Entry(self.forget_win, textvariable=self.var_conf_pass, show="*", font=("times new roman", 15), bg="lightyellow")
                        txt_conf_pass.place(x=20, y=280, width=250, height=30)

                        self.btn_update = Button(self.forget_win, text="UPDATE", command=self.update_password, state=DISABLED, font=("times new roman", 15), bg="lightblue")
                        self.btn_update.place(x=150, y=320, width=100, height=30)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error connecting to database: {err}", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)

    def send_email(self, recipient_email):
        try:
            # Generate a random 6-digit OTP
            otp = str(random.randint(100000, 999999))

            # Your email and password
            sender_email = "mr.karkar45@gmail.com"  # Replace with your email address
            sender_password = "untc wych qhkm dgsf"       # Replace with your email password

            # Email body
            subject = "Reset Password OTP"
            body = f"Your OTP for resetting the password is: {otp}"

            # Create message object
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient_email

            # Connect to SMTP server
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(sender_email, sender_password)

            # Send email
            server.sendmail(sender_email, recipient_email, msg.as_string())

            # Close connection
            server.quit()

            # Store the OTP in the instance variable
            self.otp = otp

            return 's'  # Success
        except Exception as e:
            print("Error sending email:", e)
            return 'f'  # Failure

    def validate_otp(self):
        # Placeholder logic for OTP validation
        entered_otp = self.var_otp.get()
        if entered_otp == self.otp:
            self.btn_update.config(state=NORMAL)
        else:
            messagebox.showerror("Error", "Invalid OTP, please try again", parent=self.forget_win)

    def update_password(self):
        new_pass = self.var_new_pass.get()
        conf_pass = self.var_conf_pass.get()
        if new_pass == "" or conf_pass == "":
            messagebox.showerror("Error", "All fields are required", parent=self.forget_win)
        elif new_pass != conf_pass:
            messagebox.showerror("Error", "Passwords do not match", parent=self.forget_win)
        else:
            try:
                con = mysql.connector.connect(host="localhost", user="root", password="harsh@123", database="assettracking")
                cur = con.cursor()
                cur.execute("UPDATE users SET password=%s WHERE email=%s", (new_pass, self.email.get()))
                con.commit()
                messagebox.showinfo("Success", "Password updated successfully", parent=self.forget_win)
                self.forget_win.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error updating password: {err}", parent=self.forget_win)
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.forget_win)

root = Tk()
obj = Login_System(root)

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set geometry to fit screen
root.geometry(f"{screen_width}x{screen_height}")

root.mainloop()

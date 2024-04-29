import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import requests
import mysql.connector

class AddAssetsWindow:
    def __init__(self, window_box):
        self.window_box = window_box

        self.Asset_id_int = tk.IntVar()
        self.Asset_Types_var = tk.StringVar()
        self.Category_var = tk.StringVar()
        self.No_of_assets_var = tk.IntVar()
        self.Purchase_date_var = tk.StringVar()

        # Create a LabelFrame for entering asset details
        self.frame = tk.LabelFrame(self.window_box, text="Enter Asset Details", padx=50, pady=50, bg="#9DA0A7")
        self.frame.pack(padx=50, pady=50, fill=tk.X)

        # Change font size and background color of labels
        self.label_font = ('Helvetica', 12)
        self.label_bg = "#9DA0A7"

        # Entry widgets for asset details
        tk.Label(self.frame, text="Asset ID:", width=20, height=4, font=self.label_font, bg=self.label_bg).grid(row=0, column=0, padx=(0, 10))
        tk.Entry(self.frame, textvariable=self.Asset_id_int, width=30).grid(row=0, column=1)

        # Dropdown menu for selecting title
        Asset_Types_options = ['Bitcoin', 'Stocks']
        tk.Label(self.frame, text="Asset Types:", width=20, height=4, font=self.label_font, bg=self.label_bg).grid(row=1, column=0, padx=(0, 10))
        Asset_Types_dropdown = tk.OptionMenu(self.frame, self.Asset_Types_var, *Asset_Types_options)
        Asset_Types_dropdown.grid(row=1, column=1)

        tk.Label(self.frame, text="Category:", width=20, height=4, font=self.label_font, bg=self.label_bg).grid(row=2, column=0, padx=(0, 10))
        tk.Entry(self.frame, textvariable=self.Category_var, width=30).grid(row=2, column=1)

        tk.Label(self.frame, text="Number of assets:", width=20, height=4, font=self.label_font, bg=self.label_bg).grid(row=3, column=0, padx=(0, 10))
        tk.Entry(self.frame, textvariable=self.No_of_assets_var, width=30).grid(row=3, column=1)

        tk.Label(self.frame, text="Purchase Date(yy/mm/dd):", width=20, height=4, font=self.label_font, bg=self.label_bg).grid(row=4, column=0, padx=(0, 10))
        cal = DateEntry(self.frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        cal.grid(row=4, column=1)
        cal.bind("<<DateEntrySelected>>", self.save_date)

        # Save button
        save_button = tk.Button(self.frame, text="Save Asset", command=self.save_asset, width=20)
        save_button.grid(row=7, columnspan=2)

    def save_asset(self):
        Asset_id = self.Asset_id_int.get()
        Asset_Types = self.Asset_Types_var.get()
        Category = self.Category_var.get()
        No_of_assets = self.No_of_assets_var.get()
        Purchase_date = self.Purchase_date_var.get()

        if Asset_Types == 'Bitcoin':
            api_url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
            try:
                response = requests.get(api_url)
                response.raise_for_status()  # Check for HTTP errors
                data = response.json()
                if 'bpi' not in data or 'USD' not in data['bpi']:
                    raise ValueError("Price not found in response")
                api_value = data['bpi']['USD']['rate_float']
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Failed to fetch Bitcoin price: {e}")
                return
            except (ValueError, KeyError) as e:
                messagebox.showerror("Error", f"Failed to parse Bitcoin price: {e}")
                return
        elif Asset_Types == 'Stocks':
            api_url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={Category}&apikey=T9WT2SEE3DESWBOX'
            try:
                response = requests.get(api_url)
                response.raise_for_status()
                data = response.json()
                if 'Global Quote' not in data or '05. price' not in data['Global Quote']:
                    raise ValueError("Invalid Category")
                api_value = data['Global Quote']['05. price']
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"Failed to fetch stock price: {e}")
                return
            except (ValueError, KeyError) as e:
                messagebox.showerror("Error", f"select a valid asset type and category.")
                return
        else:
            api_value = None

        if not all([Asset_id, Asset_Types, Category, No_of_assets, Purchase_date]) or api_value is None:
            messagebox.showwarning("Warning", "Please fill in all the fields or select a valid asset type and category.")
            return
        Asset_value = No_of_assets * float(api_value)

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="harsh@123",
                database="assettracking"
            )

            cursor = connection.cursor()
            query = "INSERT INTO assets (Asset_id, Asset_Types, Category, No_of_assets, Purchase_date, Asset_value, Api_value) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (Asset_id, Asset_Types, Category, No_of_assets, Purchase_date, Asset_value, api_value)
            cursor.execute(query, values)

            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Asset details saved successfully!")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error: {e}")

    def save_date(self, event):
        selected_date = cal.get_date()
        self.Purchase_date_var.set(selected_date)

    def go_back(self):
        root.destroy()

if __name__ == "__main__":
    root = tk.Toplevel()
    add_assets_window = AddAssetsWindow(root)
    root.mainloop()

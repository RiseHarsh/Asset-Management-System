import requests
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

root = tk.Tk()

Asset_id_int = tk.IntVar()
Asset_Types_var = tk.StringVar()
Category_var = tk.StringVar()
No_of_assets_var = tk.IntVar()
Purchase_date_var = tk.StringVar()

# Function to save asset details
def save_asset():
    Asset_id = Asset_id_int.get()
    Asset_Types = Asset_Types_var.get()
    Category = Category_var.get()
    No_of_assets = No_of_assets_var.get()
    Purchase_date = Purchase_date_var.get()

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
        response = requests.get(api_url)
        data = response.json()
        api_value = data['Global Quote']['05. price']
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

# Function to check assets
def check_assets():
    assets_window = tk.Toplevel(root)
    assets_window.title("Assets")
    assets_window.geometry("800x400")

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harsh@123",
            database="assettracking"
        )

        cursor = connection.cursor()

        cursor.execute("SELECT Asset_id, Asset_Types, Category, No_of_assets, Purchase_date, Api_value, Asset_value FROM assets")
        assets = cursor.fetchall()

        if not assets:
            messagebox.showinfo("No Assets", "There are no assets in the database.")
            return

        tree = ttk.Treeview(assets_window, columns=("Asset ID", "Asset Types", "Category", "No of Assets", "Purchase Date", "Api Value", "Asset Value"))

        tree.heading("Asset ID", text="Asset ID")
        tree.heading("Asset Types", text="Asset Types")
        tree.heading("Category", text="Category")
        tree.heading("No of Assets", text="No of Assets")
        tree.heading("Purchase Date", text="Purchase Date")
        tree.heading("Api Value", text="Api Value")
        tree.heading("Asset Value", text="Asset Value")

        for asset in assets:
            asset_value = asset[6]
            if isinstance(asset_value, str):
                try:
                    asset_value = float(asset_value)
                except ValueError:
                    messagebox.showwarning("Warning", f"Invalid asset value: {asset_value}")
                    continue
            asset_value_with_dollar = "${:.2f}".format(asset_value)  # Formatting asset value with 2 decimal places and dollar sign
            tree.insert("", "end", text=asset[0], values=(asset[0], asset[1], asset[2], asset[3], asset[4], float(asset[5]), asset_value_with_dollar))

        tree.pack(expand=True, fill="both")

        connection.commit()
        connection.close()

    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error: {e}")

# Create the main window
root.title("Asset Management System")
root.geometry("1350x700+0+0")

# Change background color of root window
root.configure(bg="light blue")

# Create a LabelFrame for entering asset details
frame = tk.LabelFrame(root, text="Enter Asset Details", padx=50, pady=50, bg="light blue")
frame.pack(padx=50, pady=50, fill=tk.X)

# Change font size and background color of labels
label_font = ('Helvetica', 12)
label_bg = "light blue"

# Entry widgets for asset details
tk.Label(frame, text="Asset ID:", width=20, height=4, font=label_font, bg=label_bg).grid(row=0, column=0, padx=(0, 10))
tk.Entry(frame, textvariable=Asset_id_int, width=30).grid(row=0, column=1)

# Dropdown menu for selecting title
Asset_Types_options = ['Bitcoin', 'Stocks']
tk.Label(frame, text="Asset Types:", width=20, height=4, font=label_font, bg=label_bg).grid(row=1, column=0, padx=(0, 10))
Asset_Types_dropdown = tk.OptionMenu(frame, Asset_Types_var, *Asset_Types_options)
Asset_Types_dropdown.grid(row=1, column=1)

tk.Label(frame, text="Category:", width=20, height=4, font=label_font, bg=label_bg).grid(row=2, column=0, padx=(0, 10))
tk.Entry(frame, textvariable=Category_var, width=30).grid(row=2, column=1)

tk.Label(frame, text="Number of assets:", width=20, height=4, font=label_font, bg=label_bg).grid(row=3, column=0, padx=(0, 10))
tk.Entry(frame, textvariable=No_of_assets_var, width=30).grid(row=3, column=1)

tk.Label(frame, text="Purchase Date(yyyy/mm/dd):", width=20, height=4, font=label_font, bg=label_bg).grid(row=4, column=0, padx=(0, 10))
tk.Entry(frame, textvariable=Purchase_date_var, width=30).grid(row=4, column=1)

# Save button
save_button = tk.Button(frame, text="Save Asset", command=save_asset, width=20)
save_button.grid(row=7, columnspan=2)

# Check Assets button
check_assets_button = tk.Button(root, text="Check Assets", command=check_assets, width=20)
check_assets_button.pack(side=tk.BOTTOM, pady=20)

root.mainloop()
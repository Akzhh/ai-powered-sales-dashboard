import sqlite3
from openpyxl import Workbook
from tkinter import messagebox

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

# -----------------------------
# Get Data
# -----------------------------
cursor.execute("SELECT * FROM sales")
rows = cursor.fetchall()

# -----------------------------
# Create Excel Workbook
# -----------------------------
wb = Workbook()
ws = wb.active
ws.title = "Sales Report"

# Header
headers = [
    "ID",
    "Date",
    "Product",
    "Category",
    "Quantity",
    "Price",
    "Total",
    "Profit"
]

ws.append(headers)

# Data
for row in rows:
    ws.append(row)

# -----------------------------
# Save Excel File
# -----------------------------
file_name = "Sales_Report.xlsx"
wb.save(file_name)

conn.close()

messagebox.showinfo(
    "Success",
    f"Excel file saved successfully.\n\nFile: {file_name}"
)

print("Sales_Report.xlsx created successfully.")
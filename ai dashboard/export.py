import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
import _services.database as db
from openpyxl import Workbook
from tkinter import messagebox

# -----------------------------
# Get Data
# -----------------------------
try:
    rows = db.view_sales()
except Exception as e:
    messagebox.showerror("Error", f"Could not fetch sales data: {e}")
    sys.exit(1)

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

messagebox.showinfo(
    "Success",
    f"Excel file saved successfully.\n\nFile: {file_name}"
)

print("Sales_Report.xlsx created successfully.")
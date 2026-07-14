import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
import _services.database as db

# Create Window
root = tk.Tk()
root.title("Sales History")
root.geometry("700x400")

title = tk.Label(root, text="Sales History", font=("Arial", 18, "bold"))
title.pack(pady=10)

# Treeview
columns = ("ID", "Product", "Quantity", "Price", "Total")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill="both", expand=True)

# Fetch Data
try:
    rows = db.view_sales()
    for row in rows:
        id, date, product, category, quantity, price, total, profit = row
        tree.insert("", tk.END, values=(id, product, quantity, price, total))
except Exception as e:
    print(f"Error fetching sales: {e}")

root.mainloop()
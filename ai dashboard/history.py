import tkinter as tk
from tkinter import ttk
import sqlite3

# Database Connection
conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

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
cursor.execute("SELECT * FROM sales")

for row in cursor.fetchall():
    id, product, quantity, price = row
    total = quantity * price
    tree.insert("", tk.END, values=(id, product, quantity, price, total))

conn.close()

root.mainloop()
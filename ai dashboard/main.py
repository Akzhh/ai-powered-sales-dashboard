import tkinter as tk
from tkinter import messagebox
import subprocess


# -----------------------------
# Functions
# -----------------------------
def open_login():
    subprocess.Popen(["python", "login.py"])


def open_dashboard():
    subprocess.Popen(["python", "dashboard.py"])


def open_sales():
    subprocess.Popen(["python", "sales.py"])


def open_prediction():
    subprocess.Popen(["python", "prediction.py"])


def open_graph():
    subprocess.Popen(["python", "graph.py"])


def open_history():
    subprocess.Popen(["python", "history.py"])


def open_report():
    subprocess.Popen(["python", "report.py"])


def open_export():
    subprocess.Popen(["python", "export.py"])


def exit_project():
    if messagebox.askyesno("Exit", "Do you want to exit the project?"):
        root.destroy()


# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()
root.title("AI Sales Forecasting Dashboard")
root.geometry("500x650")
root.configure(bg="#E6F2FF")

title = tk.Label(
    root,
    text="AI SALES FORECASTING DASHBOARD",
    font=("Arial", 16, "bold"),
    bg="#E6F2FF",
    fg="darkblue"
)
title.pack(pady=20)


buttons = [
    ("Login", open_login),
    ("Dashboard", open_dashboard),
    ("Sales Management", open_sales),
    ("Prediction", open_prediction),
    ("Sales Graph", open_graph),
    ("Sales History", open_history),
    ("Generate PDF Report", open_report),
    ("Export to Excel", open_export),
]

for text, command in buttons:
    tk.Button(
        root,
        text=text,
        width=25,
        height=2,
        font=("Arial", 12),
        command=command
    ).pack(pady=8)

tk.Button(
    root,
    text="Exit",
    width=25,
    height=2,
    font=("Arial", 12),
    bg="red",
    fg="white",
    command=exit_project
).pack(pady=20)

root.mainloop()
from tkinter import *
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from model import predict_sales


# ==========================================
# Load Dataset
# ==========================================

try:
    data = pd.read_csv("dataset/sales.csv")
except:
    messagebox.showerror("Error", "sales.csv file not found.")
    exit()


# ==========================================
# Line Chart
# ==========================================

def line_chart():

    plt.figure(figsize=(8,5))

    plt.plot(
        data["Month"],
        data["Sales"],
        marker="o",
        linewidth=2
    )

    plt.title("Monthly Sales Trend")

    plt.xlabel("Month")

    plt.ylabel("Sales")

    plt.grid(True)

    plt.show()


# ==========================================
# Bar Chart
# ==========================================

def bar_chart():

    plt.figure(figsize=(8,5))

    plt.bar(
        data["Month"],
        data["Sales"]
    )

    plt.title("Monthly Sales")

    plt.xlabel("Month")

    plt.ylabel("Sales")

    plt.show()


# ==========================================
# Actual vs Predicted
# ==========================================

def prediction_chart():

    months = list(data["Month"])

    actual = list(data["Sales"])

    future_month = 13

    predicted = predict_sales(future_month)

    months.append(future_month)

    actual.append(predicted)

    plt.figure(figsize=(8,5))

    plt.plot(
        months,
        actual,
        marker="o"
    )

    plt.title("Actual vs Predicted Sales")

    plt.xlabel("Month")

    plt.ylabel("Sales")

    plt.grid(True)

    plt.show()
    # ==========================================
# Dashboard
# ==========================================

def open_dashboard():

    root.destroy()

    import dashboard


# ==========================================
# Exit
# ==========================================

def exit_app():

    if messagebox.askyesno(
        "Exit",
        "Do you want to Exit?"
    ):
        root.destroy()


# ==========================================
# Main Window
# ==========================================

root = Tk()

root.title("Sales Graph Analysis")

root.geometry("700x500")

root.configure(bg="#F4F6F8")

root.resizable(False, False)


# ==========================================
# Heading
# ==========================================

Label(
    root,
    text="SALES ANALYSIS DASHBOARD",
    font=("Arial",22,"bold"),
    bg="#0B3D91",
    fg="white",
    pady=15
).pack(fill=X)


# ==========================================
# Buttons Frame
# ==========================================

frame = Frame(root, bg="#F4F6F8")
frame.pack(pady=50)


Button(
    frame,
    text="Monthly Sales Trend",
    font=("Arial",12,"bold"),
    width=25,
    height=2,
    bg="#3498DB",
    fg="white",
    command=line_chart
).pack(pady=10)


Button(
    frame,
    text="Monthly Sales Bar Chart",
    font=("Arial",12,"bold"),
    width=25,
    height=2,
    bg="#27AE60",
    fg="white",
    command=bar_chart
).pack(pady=10)


Button(
    frame,
    text="Actual vs Predicted",
    font=("Arial",12,"bold"),
    width=25,
    height=2,
    bg="#9B59B6",
    fg="white",
    command=prediction_chart
).pack(pady=10)


Button(
    frame,
    text="Dashboard",
    font=("Arial",12,"bold"),
    width=25,
    height=2,
    bg="#E67E22",
    fg="white",
    command=open_dashboard
).pack(pady=10)


Button(
    frame,
    text="Exit",
    font=("Arial",12,"bold"),
    width=25,
    height=2,
    bg="red",
    fg="white",
    command=exit_app
).pack(pady=10)


# ==========================================
# Footer
# ==========================================

Label(
    root,
    text="AI Sales Forecasting Dashboard | Graph Analysis",
    bg="#F4F6F8",
    fg="gray",
    font=("Arial",10)
).pack(side=BOTTOM, pady=10)


# ==========================================
# Start Application
# ==========================================

root.mainloop()

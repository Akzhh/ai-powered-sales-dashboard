from tkinter import *
from tkinter import messagebox
import sqlite3


# ---------------------------------
# Database Summary
# ---------------------------------
def load_dashboard():

    conn = sqlite3.connect("database/sales.db")
    cursor = conn.cursor()

    # Total Sales Amount
    cursor.execute("SELECT IFNULL(SUM(total),0) FROM sales")
    total_sales = cursor.fetchone()[0]

    # Total Profit
    cursor.execute("SELECT IFNULL(SUM(profit),0) FROM sales")
    total_profit = cursor.fetchone()[0]

    # Total Orders
    cursor.execute("SELECT COUNT(*) FROM sales")
    total_orders = cursor.fetchone()[0]

    conn.close()

    lbl_sales.config(text="₹ {:.2f}".format(total_sales))
    lbl_profit.config(text="₹ {:.2f}".format(total_profit))
    lbl_orders.config(text=str(total_orders))


# ---------------------------------
# Open Sales Window
# ---------------------------------
def open_sales():
    root.destroy()
    import sales


# ---------------------------------
# Open Prediction
# ---------------------------------
def open_prediction():
    root.destroy()
    import prediction


# ---------------------------------
# Open Graph
# ---------------------------------
def open_graph():
    root.destroy()
    import graph


# ---------------------------------
# Open Report
# ---------------------------------
def open_report():
    root.destroy()
    import report


# ---------------------------------
# Logout
# ---------------------------------
def logout():

    ans = messagebox.askyesno(
        "Logout",
        "Do you want to Logout?"
    )

    if ans:
        root.destroy()
        import login


# ---------------------------------
# Main Window
# ---------------------------------
root = Tk()

root.title("AI Sales Forecasting Dashboard")

root.geometry("1000x650")

root.configure(bg="#F4F6F8")

root.resizable(False, False)


# ---------------------------------
# Title
# ---------------------------------
Label(
    root,
    text="AI SALES FORECASTING DASHBOARD",
    font=("Arial", 22, "bold"),
    bg="#0B3D91",
    fg="white",
    pady=15
).pack(fill=X)


# ---------------------------------
# Cards Frame
# ---------------------------------
card_frame = Frame(root, bg="#F4F6F8")
card_frame.pack(pady=30)


# ===== Sales Card =====

Frame1 = Frame(card_frame, bg="#3498DB", width=250, height=130)
Frame1.grid(row=0, column=0, padx=20)

Frame1.pack_propagate(False)

Label(
    Frame1,
    text="TOTAL SALES",
    bg="#3498DB",
    fg="white",
    font=("Arial",16,"bold")
).pack(pady=10)

lbl_sales = Label(
    Frame1,
    text="₹ 0",
    bg="#3498DB",
    fg="white",
    font=("Arial",22,"bold")
)

lbl_sales.pack()


# ===== Orders Card =====

Frame2 = Frame(card_frame, bg="#27AE60", width=250, height=130)
Frame2.grid(row=0, column=1, padx=20)

Frame2.pack_propagate(False)

Label(
    Frame2,
    text="TOTAL ORDERS",
    bg="#27AE60",
    fg="white",
    font=("Arial",16,"bold")
).pack(pady=10)

lbl_orders = Label(
    Frame2,
    text="0",
    bg="#27AE60",
    fg="white",
    font=("Arial",22,"bold")
)

lbl_orders.pack()


# ===== Profit Card =====

Frame3 = Frame(card_frame, bg="#E67E22", width=250, height=130)
Frame3.grid(row=0, column=2, padx=20)

Frame3.pack_propagate(False)

Label(
    Frame3,
    text="TOTAL PROFIT",
    bg="#E67E22",
    fg="white",
    font=("Arial",16,"bold")
).pack(pady=10)

lbl_profit = Label(
    Frame3,
    text="₹ 0",
    bg="#E67E22",
    fg="white",
    font=("Arial",22,"bold")
)

lbl_profit.pack()


# ---------------------------------
# Buttons
# ---------------------------------
button_frame = Frame(root, bg="#F4F6F8")
button_frame.pack(pady=30)

Button(
    button_frame,
    text="Sales Management",
    width=20,
    height=2,
    bg="#2980B9",
    fg="white",
    font=("Arial",12,"bold"),
    command=open_sales
).grid(row=0,column=0,padx=15,pady=15)

Button(
    button_frame,
    text="AI Prediction",
    width=20,
    height=2,
    bg="#8E44AD",
    fg="white",
    font=("Arial",12,"bold"),
    command=open_prediction
).grid(row=0,column=1,padx=15,pady=15)

Button(
    button_frame,
    text="Sales Graph",
    width=20,
    height=2,
    bg="#16A085",
    fg="white",
    font=("Arial",12,"bold"),
    command=open_graph
).grid(row=1,column=0,padx=15,pady=15)

Button(
    button_frame,
    text="Reports",
    width=20,
    height=2,
    bg="#D35400",
    fg="white",
    font=("Arial",12,"bold"),
    command=open_report
).grid(row=1,column=1,padx=15,pady=15)


Button(
    root,
    text="Logout",
    width=18,
    bg="red",
    fg="white",
    font=("Arial",12,"bold"),
    command=logout
).pack(pady=20)


# ---------------------------------
# Footer
# ---------------------------------
Label(
    root,
    text="Developed using Python + AI/ML",
    bg="#F4F6F8",
    fg="gray",
    font=("Arial",10)
).pack(side=BOTTOM,pady=10)


# Load Dashboard Data
load_dashboard()

root.mainloop()
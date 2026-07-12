from tkinter import *
from tkinter import messagebox
from model import predict_sales


# ==========================================
# Predict Function
# ==========================================

def predict():

    month = txt_month.get()

    if month == "":
        messagebox.showerror(
            "Error",
            "Please Enter Month"
        )
        return

    try:

        month = int(month)

        if month <= 0:

            messagebox.showerror(
                "Error",
                "Month must be greater than 0"
            )

            return

        sales = predict_sales(month)

        lbl_result.config(
            text="₹ {:.2f}".format(sales)
        )

    except:

        messagebox.showerror(
            "Error",
            "Invalid Month"
        )


# ==========================================
# Dashboard
# ==========================================

def dashboard():

    root.destroy()

    import dashboard


# ==========================================
# Clear
# ==========================================

def clear():

    txt_month.delete(0, END)

    lbl_result.config(text="₹ 0.00")


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
# Window
# ==========================================

root = Tk()

root.title("AI Sales Prediction")

root.geometry("600x450")

root.configure(bg="#F4F6F8")

root.resizable(False, False)


Label(

    root,

    text="AI SALES FORECASTING",

    bg="#0B3D91",

    fg="white",

    font=("Arial",22,"bold"),

    pady=15

).pack(fill=X)


frame = Frame(

    root,

    bg="white",

    bd=3,

    relief=RIDGE

)

frame.pack(

    padx=40,

    pady=40,

    fill=BOTH,

    expand=True

)


Label(

    frame,

    text="Enter Future Month",

    bg="white",

    font=("Arial",14,"bold")

).pack(pady=20)


txt_month = Entry(

    frame,

    font=("Arial",14),

    justify=CENTER,

    width=20

)

txt_month.pack()
# ==========================================
# Predict Button
# ==========================================

Button(

    frame,

    text="Predict Sales",

    font=("Arial",12,"bold"),

    bg="green",

    fg="white",

    width=20,

    command=predict

).pack(pady=15)


# ==========================================
# Result Label
# ==========================================

Label(

    frame,

    text="Predicted Sales",

    bg="white",

    font=("Arial",14,"bold")

).pack(pady=10)


lbl_result = Label(

    frame,

    text="₹ 0.00",

    bg="white",

    fg="blue",

    font=("Arial",24,"bold")

)

lbl_result.pack(pady=10)


# ==========================================
# Buttons Frame
# ==========================================

button_frame = Frame(

    frame,

    bg="white"

)

button_frame.pack(pady=25)


Button(

    button_frame,

    text="Clear",

    width=12,

    font=("Arial",11,"bold"),

    bg="orange",

    fg="white",

    command=clear

).grid(row=0,column=0,padx=10)


Button(

    button_frame,

    text="Dashboard",

    width=12,

    font=("Arial",11,"bold"),

    bg="#2980B9",

    fg="white",

    command=dashboard

).grid(row=0,column=1,padx=10)


Button(

    button_frame,

    text="Exit",

    width=12,

    font=("Arial",11,"bold"),

    bg="red",

    fg="white",

    command=exit_app

).grid(row=0,column=2,padx=10)


# ==========================================
# Footer
# ==========================================

Label(

    root,

    text="AI Sales Forecasting Dashboard | Python + Machine Learning",

    bg="#F4F6F8",

    fg="gray",

    font=("Arial",10)

).pack(side=BOTTOM,pady=10)


# ==========================================
# Start Application
# ==========================================

root.mainloop()

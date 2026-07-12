from tkinter import *
from tkinter import messagebox

# -------------------------
# Login Function
# -------------------------
def login():

    username = txt_user.get()
    password = txt_pass.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All Fields are Required")
        return

    if username == "admin" and password == "admin123":

        messagebox.showinfo("Success", "Login Successful")

        root.destroy()

        import dashboard

    else:
        messagebox.showerror("Error", "Invalid Username or Password")


# -------------------------
# Clear Fields
# -------------------------
def clear():

    txt_user.delete(0, END)
    txt_pass.delete(0, END)


# -------------------------
# Show / Hide Password
# -------------------------
def show_password():

    if chk_value.get() == 1:
        txt_pass.config(show="")
    else:
        txt_pass.config(show="*")


# -------------------------
# Exit Application
# -------------------------
def exit_app():

    result = messagebox.askyesno("Exit", "Do you want to Exit?")

    if result:
        root.destroy()


# -------------------------
# Main Window
# -------------------------
root = Tk()

root.title("AI Sales Forecasting Dashboard - Login")

root.geometry("500x500")

root.resizable(False, False)

root.configure(bg="#EAF4FC")


# -------------------------
# Heading
# -------------------------
title = Label(
    root,
    text="AI SALES FORECASTING DASHBOARD",
    font=("Arial", 18, "bold"),
    bg="#EAF4FC",
    fg="navy"
)

title.pack(pady=25)


# -------------------------
# Login Frame
# -------------------------
frame = Frame(
    root,
    bg="white",
    bd=3,
    relief=RIDGE
)

frame.pack(pady=20, padx=30, fill=BOTH)


# -------------------------
# Username
# -------------------------
Label(
    frame,
    text="Username",
    font=("Arial", 12, "bold"),
    bg="white"
).pack(pady=10)

txt_user = Entry(
    frame,
    font=("Arial", 12),
    width=30
)

txt_user.pack()


# -------------------------
# Password
# -------------------------
Label(
    frame,
    text="Password",
    font=("Arial", 12, "bold"),
    bg="white"
).pack(pady=10)

txt_pass = Entry(
    frame,
    font=("Arial", 12),
    width=30,
    show="*"
)

txt_pass.pack()


# -------------------------
# Show Password
# -------------------------
chk_value = IntVar()

Checkbutton(
    frame,
    text="Show Password",
    variable=chk_value,
    bg="white",
    command=show_password
).pack(pady=10)


# -------------------------
# Buttons
# -------------------------
Button(
    frame,
    text="Login",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    width=20,
    command=login
).pack(pady=8)

Button(
    frame,
    text="Clear",
    font=("Arial", 12, "bold"),
    bg="orange",
    fg="white",
    width=20,
    command=clear
).pack(pady=8)

Button(
    frame,
    text="Exit",
    font=("Arial", 12, "bold"),
    bg="red",
    fg="white",
    width=20,
    command=exit_app
).pack(pady=8)


# -------------------------
# Footer
# -------------------------
Label(
    root,
    text="Developed Using Python + AI/ML",
    bg="#EAF4FC",
    fg="gray",
    font=("Arial", 10)
).pack(side=BOTTOM, pady=15)


root.mainloop()
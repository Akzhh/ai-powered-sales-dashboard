from tkinter import *
from tkinter import ttk, messagebox
import database


# ==========================================
# Main Window
# ==========================================

root = Tk()

root.title("Sales Management")

root.geometry("1100x700")

root.configure(bg="#F4F6F8")

root.resizable(False, False)


# ==========================================
# Variables
# ==========================================

selected_id = None


# ==========================================
# Heading
# ==========================================

title = Label(
    root,
    text="SALES MANAGEMENT",
    font=("Arial", 22, "bold"),
    bg="#0B3D91",
    fg="white",
    pady=15
)

title.pack(fill=X)


# ==========================================
# Form Frame
# ==========================================

form_frame = LabelFrame(
    root,
    text="Sales Details",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=15,
    bg="white"
)

form_frame.pack(fill=X, padx=20, pady=20)


# ==========================================
# Date
# ==========================================

Label(
    form_frame,
    text="Date",
    bg="white",
    font=("Arial", 11, "bold")
).grid(row=0, column=0, padx=10, pady=10)

txt_date = Entry(
    form_frame,
    font=("Arial", 11),
    width=25
)

txt_date.grid(row=0, column=1)


# ==========================================
# Product
# ==========================================

Label(
    form_frame,
    text="Product",
    bg="white",
    font=("Arial", 11, "bold")
).grid(row=1, column=0, padx=10, pady=10)

txt_product = Entry(
    form_frame,
    font=("Arial", 11),
    width=25
)

txt_product.grid(row=1, column=1)


# ==========================================
# Category
# ==========================================

Label(
    form_frame,
    text="Category",
    bg="white",
    font=("Arial", 11, "bold")
).grid(row=2, column=0, padx=10, pady=10)

txt_category = Entry(
    form_frame,
    font=("Arial", 11),
    width=25
)

txt_category.grid(row=2, column=1)


# ==========================================
# Quantity
# ==========================================

Label(
    form_frame,
    text="Quantity",
    bg="white",
    font=("Arial", 11, "bold")
).grid(row=0, column=2, padx=20)

txt_quantity = Entry(
    form_frame,
    font=("Arial", 11),
    width=25
)

txt_quantity.grid(row=0, column=3)


# ==========================================
# Price
# ==========================================

Label(
    form_frame,
    text="Price",
    bg="white",
    font=("Arial", 11, "bold")
).grid(row=1, column=2, padx=20)

txt_price = Entry(
    form_frame,
    font=("Arial", 11),
    width=25
)

txt_price.grid(row=1, column=3)
# ==========================================
# Buttons Frame
# ==========================================

button_frame = Frame(root, bg="#F4F6F8")
button_frame.pack(pady=15)


btn_add = Button(
    button_frame,
    text="Add Sale",
    font=("Arial", 11, "bold"),
    bg="green",
    fg="white",
    width=15
)
btn_add.grid(row=0, column=0, padx=10)


btn_update = Button(
    button_frame,
    text="Update",
    font=("Arial", 11, "bold"),
    bg="#3498DB",
    fg="white",
    width=15
)
btn_update.grid(row=0, column=1, padx=10)


btn_delete = Button(
    button_frame,
    text="Delete",
    font=("Arial", 11, "bold"),
    bg="red",
    fg="white",
    width=15
)
btn_delete.grid(row=0, column=2, padx=10)


btn_search = Button(
    button_frame,
    text="Search",
    font=("Arial", 11, "bold"),
    bg="#8E44AD",
    fg="white",
    width=15
)
btn_search.grid(row=0, column=3, padx=10)


btn_refresh = Button(
    button_frame,
    text="Refresh",
    font=("Arial", 11, "bold"),
    bg="#F39C12",
    fg="white",
    width=15
)
btn_refresh.grid(row=0, column=4, padx=10)


btn_dashboard = Button(
    button_frame,
    text="Dashboard",
    font=("Arial", 11, "bold"),
    bg="#2C3E50",
    fg="white",
    width=15
)
btn_dashboard.grid(row=1, column=1, pady=15)


btn_clear = Button(
    button_frame,
    text="Clear",
    font=("Arial", 11, "bold"),
    bg="#16A085",
    fg="white",
    width=15
)
btn_clear.grid(row=1, column=2, pady=15)


btn_exit = Button(
    button_frame,
    text="Exit",
    font=("Arial", 11, "bold"),
    bg="#7F0000",
    fg="white",
    width=15,
    command=root.destroy
)
btn_exit.grid(row=1, column=3, pady=15)


# ==========================================
# Table Frame
# ==========================================

table_frame = Frame(root)
table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)


scroll_y = Scrollbar(table_frame, orient=VERTICAL)
scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)


table = ttk.Treeview(
    table_frame,
    columns=(
        "ID",
        "Date",
        "Product",
        "Category",
        "Quantity",
        "Price",
        "Total",
        "Profit"
    ),
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)


scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.pack(side=BOTTOM, fill=X)

scroll_y.config(command=table.yview)
scroll_x.config(command=table.xview)


table.heading("ID", text="ID")
table.heading("Date", text="Date")
table.heading("Product", text="Product")
table.heading("Category", text="Category")
table.heading("Quantity", text="Quantity")
table.heading("Price", text="Price")
table.heading("Total", text="Total")
table.heading("Profit", text="Profit")


table.column("ID", width=60, anchor=CENTER)
table.column("Date", width=120, anchor=CENTER)
table.column("Product", width=180)
table.column("Category", width=150)
table.column("Quantity", width=100, anchor=CENTER)
table.column("Price", width=100, anchor=CENTER)
table.column("Total", width=120, anchor=CENTER)
table.column("Profit", width=120, anchor=CENTER)


table["show"] = "headings"

table.pack(fill=BOTH, expand=True)


# ==========================================
# Footer
# ==========================================

footer = Label(
    root,
    text="AI Sales Forecasting Dashboard | Python + SQLite + Machine Learning",
    bg="#F4F6F8",
    fg="gray",
    font=("Arial", 10)
)

footer.pack(side=BOTTOM, pady=10)
# ==========================================
# Clear Fields
# ==========================================

def clear_fields():

    global selected_id

    selected_id = None

    txt_date.delete(0, END)
    txt_product.delete(0, END)
    txt_category.delete(0, END)
    txt_quantity.delete(0, END)
    txt_price.delete(0, END)


# ==========================================
# Add Sale
# ==========================================

def add_sale():

    if txt_date.get() == "" or \
       txt_product.get() == "" or \
       txt_category.get() == "" or \
       txt_quantity.get() == "" or \
       txt_price.get() == "":

        messagebox.showerror(
            "Error",
            "All Fields are Required"
        )

        return

    try:

        quantity = int(txt_quantity.get())
        price = float(txt_price.get())

        total = quantity * price

        # 20% Profit
        profit = total * 0.20

        database.insert_sale(

            txt_date.get(),
            txt_product.get(),
            txt_category.get(),
            quantity,
            price,
            total,
            profit

        )

        messagebox.showinfo(
            "Success",
            "Sale Added Successfully"
        )

        clear_fields()

        show_data()

    except:

        messagebox.showerror(
            "Error",
            "Quantity and Price must be Numeric."
        )


# ==========================================
# Display Records
# ==========================================

def show_data():

    table.delete(*table.get_children())

    rows = database.view_sales()

    for row in rows:

        table.insert(
            "",
            END,
            values=row
        )


# ==========================================
# Select Record
# ==========================================

def select_record(event):

    global selected_id

    selected = table.focus()

    values = table.item(
        selected,
        "values"
    )

    if values:

        selected_id = values[0]

        clear_fields()

        txt_date.insert(0, values[1])
        txt_product.insert(0, values[2])
        txt_category.insert(0, values[3])
        txt_quantity.insert(0, values[4])
        txt_price.insert(0, values[5])


# ==========================================
# Refresh
# ==========================================

def refresh():

    clear_fields()

    show_data()


# ==========================================
# Open Dashboard
# ==========================================

def open_dashboard():

    root.destroy()

    import dashboard


# ==========================================
# Button Commands
# ==========================================

btn_add.config(command=add_sale)

btn_refresh.config(command=refresh)

btn_clear.config(command=clear_fields)

btn_dashboard.config(command=open_dashboard)

table.bind(
    "<ButtonRelease-1>",
    select_record
)


# ==========================================
# Load Records
# ==========================================

show_data()
# ==========================================
# Search Sale
# ==========================================

def search_sale():

    product = txt_product.get().strip()

    if product == "":
        messagebox.showerror(
            "Error",
            "Enter Product Name to Search"
        )
        return

    table.delete(*table.get_children())

    rows = database.search_sale(product)

    for row in rows:
        table.insert("", END, values=row)


# ==========================================
# Update Sale
# ==========================================

def update_sale():

    global selected_id

    if selected_id is None:
        messagebox.showerror(
            "Error",
            "Please Select a Record"
        )
        return

    try:

        quantity = int(txt_quantity.get())
        price = float(txt_price.get())

        total = quantity * price
        profit = total * 0.20

        database.update_sale(

            selected_id,

            txt_date.get(),
            txt_product.get(),
            txt_category.get(),
            quantity,
            price,
            total,
            profit

        )

        messagebox.showinfo(
            "Success",
            "Record Updated Successfully"
        )

        refresh()

    except ValueError:

        messagebox.showerror(
            "Error",
            "Invalid Quantity or Price"
        )


# ==========================================
# Delete Sale
# ==========================================

def delete_sale():

    global selected_id

    if selected_id is None:

        messagebox.showerror(
            "Error",
            "Select a Record"
        )

        return

    result = messagebox.askyesno(
        "Delete",
        "Do you want to Delete this Record?"
    )

    if result:

        database.delete_sale(selected_id)

        messagebox.showinfo(
            "Deleted",
            "Record Deleted Successfully"
        )

        refresh()


# ==========================================
# Exit Application
# ==========================================

def exit_app():

    result = messagebox.askyesno(
        "Exit",
        "Do you want to Exit?"
    )

    if result:
        root.destroy()


# ==========================================
# Connect Remaining Buttons
# ==========================================

btn_search.config(command=search_sale)

btn_update.config(command=update_sale)

btn_delete.config(command=delete_sale)

btn_exit.config(command=exit_app)


# ==========================================
# Start Application
# ==========================================

show_data()

root.mainloop()
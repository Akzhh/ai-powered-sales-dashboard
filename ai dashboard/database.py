import sqlite3

# -----------------------------
# Database Connection
# -----------------------------
def connect_db():
    conn = sqlite3.connect("sales.db")
    return conn


# -----------------------------
# Create Sales Table
# -----------------------------
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            product TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            total REAL NOT NULL,
            profit REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Insert Sales Record
# -----------------------------
def insert_sale(date, product, category, quantity, price, total, profit):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sales
        (date, product, category, quantity, price, total, profit)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (date, product, category, quantity, price, total, profit))

    conn.commit()
    conn.close()


# -----------------------------
# View All Records
# -----------------------------
def view_sales():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sales")
    rows = cursor.fetchall()

    conn.close()
    return rows


# -----------------------------
# Search Product
# -----------------------------
def search_sale(product):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM sales WHERE product LIKE ?",
        ('%' + product + '%',)
    )

    rows = cursor.fetchall()

    conn.close()
    return rows


# -----------------------------
# Update Record
# -----------------------------
def update_sale(id, date, product, category, quantity, price, total, profit):

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE sales
        SET
            date=?,
            product=?,
            category=?,
            quantity=?,
            price=?,
            total=?,
            profit=?
        WHERE id=?
    """, (
        date,
        product,
        category,
        quantity,
        price,
        total,
        profit,
        id
    ))

    conn.commit()
    conn.close()

# -----------------------------
# Delete Record
# -----------------------------
def delete_sale(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM sales WHERE id=?", (id,))

    conn.commit()
    conn.close()


# -----------------------------
# Create Database Automatically
# -----------------------------
create_table()
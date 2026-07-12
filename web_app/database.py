import sqlite3
from pathlib import Path

# Database path relative to this file
DB_PATH = Path(__file__).resolve().parent / "sales.db"

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

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

def view_sales():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales")
    rows = cursor.fetchall()
    conn.close()
    return rows

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
    """, (date, product, category, quantity, price, total, profit, id))
    conn.commit()
    conn.close()

def delete_sale(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sales WHERE id=?", (id,))
    conn.commit()
    conn.close()

# Auto create table
create_table()

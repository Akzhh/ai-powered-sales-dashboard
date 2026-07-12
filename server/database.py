import os
import sqlite3
from pathlib import Path

# ----------------------------------------
# Database path relative to this file
# ----------------------------------------
DB_PATH = Path(__file__).resolve().parent / "sales.db"


def connect_db():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        import psycopg2
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        return psycopg2.connect(db_url)
    else:
        return sqlite3.connect(DB_PATH)


def is_postgres(conn):
    return conn.__class__.__module__.startswith('psycopg2')


# ----------------------------------------
# Create Sales Table
# ----------------------------------------
def create_table():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        if is_postgres(conn):
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales(
                    id SERIAL PRIMARY KEY,
                    date TEXT NOT NULL,
                    product TEXT NOT NULL,
                    category TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price DOUBLE PRECISION NOT NULL,
                    total DOUBLE PRECISION NOT NULL,
                    profit DOUBLE PRECISION NOT NULL
                )
            """)
        else:
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
    finally:
        conn.close()


# ----------------------------------------
# Insert Sales Record
# ----------------------------------------
def insert_sale(date, product, category, quantity, price, total, profit):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO sales
            (date, product, category, quantity, price, total, profit)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        if is_postgres(conn):
            query = query.replace('?', '%s')
        cursor.execute(query, (date, product, category, quantity, price, total, profit))
        conn.commit()
    finally:
        conn.close()


# ----------------------------------------
# View All Records
# ----------------------------------------
def view_sales():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()


# ----------------------------------------
# Search Product
# ----------------------------------------
def search_sale(product):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM sales WHERE product LIKE ?"
        if is_postgres(conn):
            query = query.replace('?', '%s')
        cursor.execute(query, ('%' + product + '%',))
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()


# ----------------------------------------
# Update Record
# ----------------------------------------
def update_sale(id, date, product, category, quantity, price, total, profit):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        query = """
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
        """
        if is_postgres(conn):
            query = query.replace('?', '%s')
        cursor.execute(query, (date, product, category, quantity, price, total, profit, id))
        conn.commit()
    finally:
        conn.close()


# ----------------------------------------
# Delete Record
# ----------------------------------------
def delete_sale(id):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        query = "DELETE FROM sales WHERE id=?"
        if is_postgres(conn):
            query = query.replace('?', '%s')
        cursor.execute(query, (id,))
        conn.commit()
    finally:
        conn.close()


# ----------------------------------------
# Auto-create table on import
# ----------------------------------------
try:
    create_table()
except Exception as e:
    print(f"Database initialization warning: {e}")

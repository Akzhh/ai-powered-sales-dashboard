import os
import sqlite3
from pathlib import Path
from datetime import datetime

# Database path relative to this file
DB_PATH = Path(__file__).resolve().parent.parent / "sales.db"


def connect_db():
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        import psycopg2
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        return psycopg2.connect(db_url)
    else:
        return sqlite3.connect(DB_PATH, timeout=20)


def is_postgres(conn):
    return conn.__class__.__module__.startswith('psycopg2')


def init_db():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        is_pg = is_postgres(conn)

        # 1. Sales table (backward compatibility)
        if is_pg:
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

        # 2. Users table (for authentication)
        if is_pg:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)

        # 3. Uploaded Datasets table
        if is_pg:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS uploaded_datasets(
                    id SERIAL PRIMARY KEY,
                    filename VARCHAR(255) NOT NULL,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    record_count INTEGER NOT NULL
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS uploaded_datasets(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    record_count INTEGER NOT NULL
                )
            """)

        # 4. Prediction History table
        if is_pg:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prediction_history(
                    id SERIAL PRIMARY KEY,
                    month INTEGER NOT NULL,
                    predicted_sales DOUBLE PRECISION NOT NULL,
                    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prediction_history(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    month INTEGER NOT NULL,
                    predicted_sales REAL NOT NULL,
                    predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

        # 5. Model Metadata table
        if is_pg:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS model_metadata(
                    id SERIAL PRIMARY KEY,
                    accuracy DOUBLE PRECISION NOT NULL,
                    algorithm VARCHAR(100) NOT NULL,
                    training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    dataset_size INTEGER NOT NULL
                )
            """)
        else:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS model_metadata(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    accuracy REAL NOT NULL,
                    algorithm TEXT NOT NULL,
                    training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    dataset_size INTEGER NOT NULL
                )
            """)

        # Seed default admin user
        query_check = "SELECT * FROM users WHERE username = ?"
        if is_pg:
            query_check = query_check.replace('?', '%s')
        cursor.execute(query_check, ('admin',))
        if not cursor.fetchone():
            query_insert = "INSERT INTO users (username, password) VALUES (?, ?)"
            if is_pg:
                query_insert = query_insert.replace('?', '%s')
            cursor.execute(query_insert, ('admin', 'admin123'))

        conn.commit()
    finally:
        conn.close()


# ----------------------------------------
# Sales CRUD Operations
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


def view_sales():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()


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
# User Authentication
# ----------------------------------------
def check_user_credentials(username, password):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        query = "SELECT password FROM users WHERE username = ?"
        if is_postgres(conn):
            query = query.replace('?', '%s')
        cursor.execute(query, (username,))
        row = cursor.fetchone()
        if row and row[0] == password:
            return True
        return False
    finally:
        conn.close()


# ----------------------------------------
# Logs & Metadata
# ----------------------------------------
def log_uploaded_dataset(filename, record_count):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        query = "INSERT INTO uploaded_datasets (filename, record_count) VALUES (?, ?)"
        if is_postgres(conn):
            query = query.replace('?', '%s')
        cursor.execute(query, (filename, record_count))
        conn.commit()
    finally:
        conn.close()


def log_prediction(month, predicted_sales):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        query = "INSERT INTO prediction_history (month, predicted_sales) VALUES (?, ?)"
        if is_postgres(conn):
            query = query.replace('?', '%s')
        cursor.execute(query, (month, predicted_sales))
        conn.commit()
    finally:
        conn.close()


def save_model_metadata(accuracy, algorithm, dataset_size):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO model_metadata (accuracy, algorithm, training_date, dataset_size)
            VALUES (?, ?, ?, ?)
        """
        if is_postgres(conn):
            query = query.replace('?', '%s')
        cursor.execute(query, (accuracy, algorithm, datetime.now(), dataset_size))
        conn.commit()
    finally:
        conn.close()


def get_latest_model_metadata():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT accuracy, algorithm, training_date, dataset_size FROM model_metadata ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row:
            t_date = row[2]
            if isinstance(t_date, str):
                try:
                    dt = datetime.fromisoformat(t_date.replace('Z', '+00:00'))
                    t_date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    t_date_str = t_date
            else:
                t_date_str = t_date.strftime("%Y-%m-%d %H:%M:%S") if t_date else "Unknown"

            return {
                "accuracy": round(float(row[0]), 4),
                "algorithm": row[1],
                "training_date": t_date_str,
                "dataset_size": row[3]
            }
        return None
    finally:
        conn.close()


# Auto-create tables on startup/import
try:
    init_db()
except Exception as e:
    print(f"Database initialization warning: {e}")

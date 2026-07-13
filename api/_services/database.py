import logging
import psycopg2
from datetime import datetime
from _services.config import DATABASE_URL
from _services.utils import hash_password, verify_hashed_password

logger = logging.getLogger(__name__)


def _get_database_url():
    """Get DATABASE_URL from config, converting postgres:// to postgresql:// if needed."""
    db_url = DATABASE_URL
    if not db_url:
        raise RuntimeError(
            "DATABASE_URL environment variable is not set. "
            "Please configure it with your Supabase PostgreSQL connection string."
        )
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return db_url


def connect_db():
    """Create and return a new PostgreSQL connection."""
    return psycopg2.connect(_get_database_url())


# ----------------------------------------
# Database Initialization
# ----------------------------------------
def init_db():
    """Create all required tables if they do not exist and seed default admin user."""
    conn = connect_db()
    try:
        cursor = conn.cursor()

        # 1. Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)

        # 2. Sales table
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

        # 3. Dataset rows table (Month/Sales from CSV uploads)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dataset_rows(
                id SERIAL PRIMARY KEY,
                month INTEGER NOT NULL,
                sales DOUBLE PRECISION NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 4. Uploaded datasets metadata
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uploaded_datasets(
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                record_count INTEGER NOT NULL
            )
        """)

        # 5. Prediction history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS prediction_history(
                id SERIAL PRIMARY KEY,
                month INTEGER NOT NULL,
                predicted_sales DOUBLE PRECISION NOT NULL,
                predicted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 6. Model metadata
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_metadata(
                id SERIAL PRIMARY KEY,
                accuracy DOUBLE PRECISION NOT NULL,
                algorithm VARCHAR(100) NOT NULL,
                training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                dataset_size INTEGER NOT NULL
            )
        """)

        # Seed default admin user (hashed password)
        cursor.execute("SELECT id FROM users WHERE username = %s", ('admin',))
        if not cursor.fetchone():
            hashed_pw = hash_password('admin123')
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                ('admin', hashed_pw)
            )
            logger.info("Seeded default admin user.")

        conn.commit()
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Database initialization error: {e}")
        raise
    finally:
        conn.close()


# ----------------------------------------
# User Authentication
# ----------------------------------------
def get_user_by_username(username):
    """Return user dict with id, username, password (hashed) or None."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password FROM users WHERE username = %s",
            (username,)
        )
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "username": row[1], "password": row[2]}
        return None
    finally:
        conn.close()


def check_user_credentials(username, password):
    """Validate username/password. Supports both hashed and legacy plaintext passwords."""
    user = get_user_by_username(username)
    if not user:
        return False

    stored_pw = user["password"]

    # Support hashed passwords (werkzeug format)
    if stored_pw.startswith(("pbkdf2:", "scrypt:")):
        return verify_hashed_password(stored_pw, password)

    # Fallback: legacy plaintext comparison
    return stored_pw == password


# ----------------------------------------
# Sales CRUD Operations
# ----------------------------------------
def insert_sale(date, product, category, quantity, price, total, profit):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO sales (date, product, category, quantity, price, total, profit)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (date, product, category, quantity, price, total, profit)
        )
        conn.commit()
    finally:
        conn.close()


def view_sales():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales ORDER BY id ASC")
        return cursor.fetchall()
    finally:
        conn.close()


def search_sale(product):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM sales WHERE product ILIKE %s",
            ('%' + product + '%',)
        )
        return cursor.fetchall()
    finally:
        conn.close()


def update_sale(id, date, product, category, quantity, price, total, profit):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE sales
            SET date=%s, product=%s, category=%s, quantity=%s,
                price=%s, total=%s, profit=%s
            WHERE id=%s
            """,
            (date, product, category, quantity, price, total, profit, id)
        )
        conn.commit()
    finally:
        conn.close()


def delete_sale(id):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sales WHERE id=%s", (id,))
        conn.commit()
    finally:
        conn.close()


# ----------------------------------------
# Dataset Rows (CSV upload storage)
# ----------------------------------------
def save_dataset_rows(rows):
    """
    Replace all existing dataset rows with new ones.
    rows: list of dicts with 'month' and 'sales' keys.
    """
    conn = connect_db()
    try:
        cursor = conn.cursor()
        # Clear existing rows before inserting new dataset
        cursor.execute("DELETE FROM dataset_rows")
        for row in rows:
            cursor.execute(
                "INSERT INTO dataset_rows (month, sales) VALUES (%s, %s)",
                (int(row['month']), float(row['sales']))
            )
        conn.commit()
        logger.info(f"Saved {len(rows)} dataset rows to database.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error saving dataset rows: {e}")
        raise
    finally:
        conn.close()


def get_dataset_rows():
    """Fetch all dataset rows, ordered by month."""
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT month, sales FROM dataset_rows ORDER BY month ASC")
        rows = cursor.fetchall()
        return [{"Month": r[0], "Sales": r[1]} for r in rows]
    finally:
        conn.close()


# ----------------------------------------
# Logs & Metadata
# ----------------------------------------
def log_uploaded_dataset(filename, record_count):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO uploaded_datasets (filename, record_count) VALUES (%s, %s)",
            (filename, record_count)
        )
        conn.commit()
    finally:
        conn.close()


def log_prediction(month, predicted_sales):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prediction_history (month, predicted_sales) VALUES (%s, %s)",
            (month, predicted_sales)
        )
        conn.commit()
    finally:
        conn.close()


def save_model_metadata(accuracy, algorithm, dataset_size):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO model_metadata (accuracy, algorithm, training_date, dataset_size)
            VALUES (%s, %s, %s, %s)
            """,
            (accuracy, algorithm, datetime.now(), dataset_size)
        )
        conn.commit()
    finally:
        conn.close()


def get_latest_model_metadata():
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT accuracy, algorithm, training_date, dataset_size "
            "FROM model_metadata ORDER BY id DESC LIMIT 1"
        )
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

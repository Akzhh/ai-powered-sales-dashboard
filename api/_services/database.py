import logging
import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from datetime import datetime
from _services.config import DATABASE_URL
from _services.utils import hash_password, verify_hashed_password

logger = logging.getLogger(__name__)

# Global connection pool
db_pool = None

def _get_database_url():
    """Parse and configure DATABASE_URL for Serverless/Supabase compatibility."""
    db_url = DATABASE_URL
    
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    # Supabase Vercel IPv4 Fix: Convert direct port 5432 to pooler port 6543
    if "supabase.co:5432" in db_url:
        logger.info("Auto-converting Supabase URL to use Session Pooler (port 6543) for Serverless IPv4 compatibility.")
        db_url = db_url.replace("supabase.co:5432", "supabase.co:6543")
        
    # Ensure SSL is required
    if "sslmode=" not in db_url:
        separator = "&" if "?" in db_url else "?"
        db_url = f"{db_url}{separator}sslmode=require"
        
    return db_url

def init_pool():
    """Initialize the PostgreSQL connection pool."""
    global db_pool
    if db_pool is None:
        try:
            db_pool = psycopg2.pool.SimpleConnectionPool(1, 20, _get_database_url())
        except psycopg2.Error as e:
            logger.error("Failed to initialize database connection pool.")
            raise RuntimeError("Database connection error") from e

@contextmanager
def get_db_connection():
    """Context manager to lease and return connections from the pool."""
    if db_pool is None:
        init_pool()
        
    conn = None
    try:
        conn = db_pool.getconn()
        yield conn
    except psycopg2.Error as e:
        logger.error(f"PostgreSQL Database Error: {e.pgcode} - {e.pgerror}")
        if conn:
            conn.rollback()
        raise RuntimeError("A database error occurred while processing the request.") from e
    finally:
        if conn:
            db_pool.putconn(conn)

# ----------------------------------------
# Database Initialization
# ----------------------------------------
def init_db():
    """Create all required tables if they do not exist and seed default admin user."""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
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


# ----------------------------------------
# User Authentication
# ----------------------------------------
def get_user_by_username(username):
    """Return user dict with id, username, password (hashed) or None."""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, password FROM users WHERE username = %s",
                (username,)
            )
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "username": row[1], "password": row[2]}
            return None


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
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO sales (date, product, category, quantity, price, total, profit)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (date, product, category, quantity, price, total, profit)
            )
        conn.commit()


def view_sales():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM sales ORDER BY id ASC")
            return cursor.fetchall()


def search_sale(product):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM sales WHERE product ILIKE %s",
                ('%' + product + '%',)
            )
            return cursor.fetchall()


def update_sale(id, date, product, category, quantity, price, total, profit):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
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


def delete_sale(id):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM sales WHERE id=%s", (id,))
        conn.commit()


# ----------------------------------------
# Dataset Rows (CSV upload storage)
# ----------------------------------------
def save_dataset_rows(rows):
    """Replace all existing dataset rows with new ones."""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM dataset_rows")
            for row in rows:
                cursor.execute(
                    "INSERT INTO dataset_rows (month, sales) VALUES (%s, %s)",
                    (int(row['month']), float(row['sales']))
                )
        conn.commit()
        logger.info(f"Saved {len(rows)} dataset rows to database.")


def get_dataset_rows():
    """Fetch all dataset rows, ordered by month."""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT month, sales FROM dataset_rows ORDER BY month ASC")
            rows = cursor.fetchall()
            return [{"Month": r[0], "Sales": r[1]} for r in rows]


# ----------------------------------------
# Logs & Metadata
# ----------------------------------------
def log_uploaded_dataset(filename, record_count):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO uploaded_datasets (filename, record_count) VALUES (%s, %s)",
                (filename, record_count)
            )
        conn.commit()


def log_prediction(month, predicted_sales):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO prediction_history (month, predicted_sales) VALUES (%s, %s)",
                (month, predicted_sales)
            )
        conn.commit()


def save_model_metadata(accuracy, algorithm, dataset_size):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO model_metadata (accuracy, algorithm, training_date, dataset_size)
                VALUES (%s, %s, %s, %s)
                """,
                (accuracy, algorithm, datetime.now(), dataset_size)
            )
        conn.commit()


def get_latest_model_metadata():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
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

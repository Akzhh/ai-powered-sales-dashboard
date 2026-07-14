import sys
import os

# Link to the centralized PostgreSQL module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))
import _services.database as db

def connect_db():
    return db.get_db_connection()

def create_table():
    db.init_db()

def insert_sale(date, product, category, quantity, price, total, profit):
    db.insert_sale(date, product, category, quantity, price, total, profit)

def view_sales():
    return db.view_sales()

def search_sale(product):
    return db.search_sale(product)

def update_sale(id, date, product, category, quantity, price, total, profit):
    db.update_sale(id, date, product, category, quantity, price, total, profit)

def delete_sale(id):
    db.delete_sale(id)

# Initialize database tables on load
create_table()
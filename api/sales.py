import os
import sys
import re
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add the root api directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import services.database as database
from services.auth_service import require_auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'ai-sales-forecasting-dashboard-secret-key-2026')

# Enable CORS
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    re.compile(r"^https://.*\.vercel\.app$")
]
if os.environ.get("ALLOWED_ORIGINS"):
    cors_origins.extend(os.environ.get("ALLOWED_ORIGINS").split(","))
CORS(app, supports_credentials=True, origins=cors_origins)

@app.route('/api/sales', methods=['GET'])
@app.route('/sales', methods=['GET'])
@require_auth
def get_sales():
    try:
        rows = database.view_sales()
        sales_list = []
        for r in rows:
            sales_list.append({
                'id': r[0],
                'date': r[1],
                'product': r[2],
                'category': r[3],
                'quantity': r[4],
                'price': r[5],
                'total': r[6],
                'profit': r[7]
            })
        return jsonify(sales_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sales', methods=['POST'])
@app.route('/sales', methods=['POST'])
@require_auth
def add_sale():
    data = request.get_json() or {}
    date = data.get('date')
    product = data.get('product')
    category = data.get('category')
    quantity = data.get('quantity')
    price = data.get('price')

    if not all([date, product, category, quantity, price]):
        return jsonify({'error': 'All fields are required'}), 400

    try:
        qty = int(quantity)
        prc = float(price)
        if qty <= 0 or prc <= 0:
            return jsonify({'error': 'Quantity and Price must be positive numbers'}), 400

        total = qty * prc
        profit = total * 0.20

        database.insert_sale(date, product, category, qty, prc, total, profit)
        return jsonify({'success': True, 'message': 'Sale added successfully'})
    except ValueError:
        return jsonify({'error': 'Quantity and Price must be numeric'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sales/<int:sale_id>', methods=['PUT'])
@app.route('/sales/<int:sale_id>', methods=['PUT'])
@require_auth
def update_sale(sale_id):
    data = request.get_json() or {}
    date = data.get('date')
    product = data.get('product')
    category = data.get('category')
    quantity = data.get('quantity')
    price = data.get('price')

    if not all([date, product, category, quantity, price]):
        return jsonify({'error': 'All fields are required'}), 400

    try:
        qty = int(quantity)
        prc = float(price)
        if qty <= 0 or prc <= 0:
            return jsonify({'error': 'Quantity and Price must be positive numbers'}), 400

        total = qty * prc
        profit = total * 0.20

        database.update_sale(sale_id, date, product, category, qty, prc, total, profit)
        return jsonify({'success': True, 'message': 'Sale updated successfully'})
    except ValueError:
        return jsonify({'error': 'Quantity and Price must be numeric'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sales/<int:sale_id>', methods=['DELETE'])
@app.route('/sales/<int:sale_id>', methods=['DELETE'])
@require_auth
def delete_sale(sale_id):
    try:
        database.delete_sale(sale_id)
        return jsonify({'success': True, 'message': 'Sale deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sales/search', methods=['GET'])
@app.route('/sales/search', methods=['GET'])
@require_auth
def search_sales():
    product = request.args.get('product', '').strip()
    if not product:
        return jsonify([])

    try:
        rows = database.search_sale(product)
        sales_list = []
        for r in rows:
            sales_list.append({
                'id': r[0],
                'date': r[1],
                'product': r[2],
                'category': r[3],
                'quantity': r[4],
                'price': r[5],
                'total': r[6],
                'profit': r[7]
            })
        return jsonify(sales_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

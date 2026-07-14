# pyrefly: ignore [missing-import]
from flask import Blueprint
import os
import sys
import logging
from flask import jsonify, request

# Removed sys.path modification to avoid ModuleNotFoundError on Vercel

from _services.config import SECRET_KEY, CORS_ORIGINS
from _services.validation import validate_sale_input
import _services.database as database
from _services.auth_service import require_auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

sales_bp = Blueprint("sales", __name__)


@sales_bp.route('/api/sales', methods=['GET'])
@sales_bp.route('/sales', methods=['GET'])
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

@sales_bp.route('/api/sales', methods=['POST'])
@sales_bp.route('/sales', methods=['POST'])
@require_auth
def add_sale():
    data = request.get_json() or {}
    date = data.get('date')
    product = data.get('product')
    category = data.get('category')
    quantity = data.get('quantity')
    price = data.get('price')

    valid, result = validate_sale_input(date, product, category, quantity, price)
    if not valid:
        return jsonify({'error': result}), 400

    try:
        qty, prc = result
        total = qty * prc
        profit = total * 0.20

        database.insert_sale(date, product, category, qty, prc, total, profit)
        return jsonify({'success': True, 'message': 'Sale added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/api/sales/<int:sale_id>', methods=['PUT'])
@sales_bp.route('/sales/<int:sale_id>', methods=['PUT'])
@require_auth
def update_sale(sale_id):
    data = request.get_json() or {}
    date = data.get('date')
    product = data.get('product')
    category = data.get('category')
    quantity = data.get('quantity')
    price = data.get('price')

    valid, result = validate_sale_input(date, product, category, quantity, price)
    if not valid:
        return jsonify({'error': result}), 400

    try:
        qty, prc = result
        total = qty * prc
        profit = total * 0.20

        database.update_sale(sale_id, date, product, category, qty, prc, total, profit)
        return jsonify({'success': True, 'message': 'Sale updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/api/sales/<int:sale_id>', methods=['DELETE'])
@sales_bp.route('/sales/<int:sale_id>', methods=['DELETE'])
@require_auth
def delete_sale(sale_id):
    try:
        database.delete_sale(sale_id)
        return jsonify({'success': True, 'message': 'Sale deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/api/sales/search', methods=['GET'])
@sales_bp.route('/sales/search', methods=['GET'])
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



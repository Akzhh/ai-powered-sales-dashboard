from flask import Blueprint, request, jsonify
import services.database as database
from services.auth_service import require_auth

sales_bp = Blueprint('sales', __name__)


@sales_bp.route('/api/sales', methods=['GET'])
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


@sales_bp.route('/api/sales/<int:sale_id>', methods=['PUT'])
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


@sales_bp.route('/api/sales/<int:sale_id>', methods=['DELETE'])
@require_auth
def delete_sale(sale_id):
    try:
        database.delete_sale(sale_id)
        return jsonify({'success': True, 'message': 'Sale deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@sales_bp.route('/api/sales/search', methods=['GET'])
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


@sales_bp.route('/api/stats', methods=['GET'])
@require_auth
def get_stats():
    try:
        rows = database.view_sales()
        total_sales = sum(float(r[6]) for r in rows)
        total_profit = sum(float(r[7]) for r in rows)
        total_orders = len(rows)
        return jsonify({
            'total_sales': round(total_sales, 2),
            'total_profit': round(total_profit, 2),
            'total_orders': total_orders
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

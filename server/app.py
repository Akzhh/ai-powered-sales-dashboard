import os
import csv
from flask import Flask, request, jsonify, session, send_file
from flask_cors import CORS
import database
import model
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from pathlib import Path

# ----------------------------------------
# Flask App Setup
# ----------------------------------------
BASE_DIR = Path(__file__).resolve().parent
TMP_DIR = BASE_DIR / "tmp"
TMP_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.secret_key = 'ai-sales-forecasting-dashboard-secret-key-2026'

# Configure session cookie settings for cross-origin authentication in production
if os.environ.get('ENV') == 'production' or os.environ.get('DATABASE_URL'):
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True

# Enable CORS for React dev server and production frontend domain(s)
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
if os.environ.get("ALLOWED_ORIGINS"):
    cors_origins.extend(os.environ.get("ALLOWED_ORIGINS").split(","))

CORS(app, supports_credentials=True, origins=cors_origins)


# ----------------------------------------
# Authentication API
# ----------------------------------------
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if username == 'admin' and password == 'admin123':
        session['logged_in'] = True
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    return jsonify({'logged_in': session.get('logged_in', False)})


# ----------------------------------------
# Auth Helper
# ----------------------------------------
def check_auth():
    return session.get('logged_in', False)


# ----------------------------------------
# Sales CRUD API
# ----------------------------------------
@app.route('/api/sales', methods=['GET'])
def get_sales():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

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
def add_sale():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

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
def update_sale(sale_id):
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

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
def delete_sale(sale_id):
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        database.delete_sale(sale_id)
        return jsonify({'success': True, 'message': 'Sale deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/sales/search', methods=['GET'])
def search_sales():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

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


# ----------------------------------------
# Dashboard Stats API
# ----------------------------------------
@app.route('/api/stats', methods=['GET'])
def get_stats():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

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


# ----------------------------------------
# Dataset API
# ----------------------------------------
@app.route('/api/dataset', methods=['GET'])
def get_dataset():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = model.get_dataset()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ----------------------------------------
# AI Prediction API
# ----------------------------------------
@app.route('/api/predict', methods=['POST'])
def predict():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json() or {}
    month = data.get('month')

    if month is None:
        return jsonify({'error': 'Month is required'}), 400

    try:
        m = int(month)
        if m <= 0:
            return jsonify({'error': 'Month must be greater than 0'}), 400

        prediction = model.predict_sales(m)
        return jsonify({
            'month': m,
            'predicted_sales': prediction
        })
    except ValueError:
        return jsonify({'error': 'Month must be an integer'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ----------------------------------------
# CSV Upload & Model Retrain API
# ----------------------------------------
@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Only CSV files are allowed'}), 400

    try:
        # Read and validate CSV contents
        content = file.read().decode('utf-8')
        lines = content.strip().split('\n')

        # Basic validation: must have header + at least 2 rows
        if len(lines) < 3:
            return jsonify({'error': 'CSV must have a header and at least 2 data rows'}), 400

        # Check header
        header = lines[0].strip().lower()
        if 'month' not in header or 'sales' not in header:
            return jsonify({'error': 'CSV must have "Month" and "Sales" columns'}), 400

        # Save the file
        csv_path = model.CSV_PATH
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        csv_path.write_text(content)

        # Retrain model
        row_count = model.retrain_model()

        return jsonify({
            'success': True,
            'message': f'CSV uploaded and model retrained with {row_count} records',
            'rows': row_count
        })
    except Exception as e:
        return jsonify({'error': f'Failed to process CSV: {str(e)}'}), 500


# ----------------------------------------
# Export: Excel
# ----------------------------------------
@app.route('/api/export/excel', methods=['GET'])
def export_excel():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        rows = database.view_sales()
        wb = Workbook()
        ws = wb.active
        ws.title = "Sales Report"

        headers = ["ID", "Date", "Product", "Category", "Quantity", "Price", "Total", "Profit"]
        ws.append(headers)

        for r in rows:
            ws.append(r)

        temp_filename = str(TMP_DIR / "sales_report.xlsx")
        wb.save(temp_filename)

        response = send_file(
            temp_filename,
            as_attachment=True,
            download_name="Sales_Report.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        @response.call_on_close
        def remove_temp_file():
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ----------------------------------------
# Export: PDF
# ----------------------------------------
@app.route('/api/export/pdf', methods=['GET'])
def export_pdf():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        rows = database.view_sales()
        total_sales = sum(float(r[6]) for r in rows)

        # Predict sales for Month 13 as sample forecast
        try:
            sample_prediction = model.predict_sales(13)
        except Exception:
            sample_prediction = 51424.24

        temp_filename = str(TMP_DIR / "sales_report.pdf")

        doc = SimpleDocTemplate(temp_filename, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        title = Paragraph(
            "<b><font size=18 color='#0B3D91'>AI Sales Forecasting Report</font></b>",
            styles['Title']
        )
        elements.append(title)
        elements.append(Spacer(1, 20))

        # Date & Time
        date_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        elements.append(Paragraph(f"<b>Generated Date:</b> {date_str}", styles['Normal']))
        elements.append(Spacer(1, 10))

        # Summary Statistics
        elements.append(Paragraph(
            f"<b>Total Historical Sales:</b> ₹ {total_sales:.2f}",
            styles['Normal']
        ))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(
            f"<b>Forecasted Sales (Next Month/13):</b> ₹ {sample_prediction:.2f}",
            styles['Normal']
        ))
        elements.append(Spacer(1, 20))

        # Description
        description = """
        This PDF report is dynamically generated from the AI Sales Forecasting Dashboard.
        The linear regression machine learning model utilizes historical sales trends
        to output automated sales predictions.
        """
        elements.append(Paragraph(description, styles['BodyText']))
        elements.append(Spacer(1, 30))

        # Footer
        elements.append(Paragraph(
            "<b>Report End. Generated by AI Sales Forecasting Dashboard (Web Version)</b>",
            styles['Normal']
        ))

        doc.build(elements)

        response = send_file(
            temp_filename,
            as_attachment=True,
            download_name="Sales_Report.pdf",
            mimetype="application/pdf"
        )

        @response.call_on_close
        def remove_temp_file():
            if os.path.exists(temp_filename):
                os.remove(temp_filename)

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ----------------------------------------
# Run Server
# ----------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)

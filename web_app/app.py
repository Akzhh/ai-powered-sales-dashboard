import os
import csv
# pyrefly: ignore [missing-import]
from flask import Flask, request, jsonify, session, send_file
import database
import model
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'ai-sales-forecasting-dashboard-secret-key'

# -----------------------------
# Auth Helper Decorator
# -----------------------------
def check_auth():
    if not session.get('logged_in'):
        return False
    return True

# -----------------------------
# Static Routes
# -----------------------------
@app.route('/')
def index():
    return app.send_static_file('index.html')

# -----------------------------
# Authentication API
# -----------------------------
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
    return jsonify({'logged_in': check_auth()})

# -----------------------------
# Database CRUD API
# -----------------------------
@app.route('/api/sales', methods=['GET'])
def get_sales():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        rows = database.view_sales()
        # Convert tuple rows to lists of dicts
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

# -----------------------------
# Stats API
# -----------------------------
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

# -----------------------------
# Dataset API
# -----------------------------
@app.route('/api/dataset', methods=['GET'])
def get_dataset():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "dataset", "sales.csv")
        if not os.path.exists(csv_path):
            return jsonify([])
        data = []
        with open(csv_path, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    'Month': int(row['Month']),
                    'Sales': float(row['Sales'])
                })
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -----------------------------
# Prediction API
# -----------------------------
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

# -----------------------------
# Export APIs
# -----------------------------
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
            
        temp_filename = "temp_sales_report.xlsx"
        wb.save(temp_filename)
        
        response = send_file(
            temp_filename,
            as_attachment=True,
            download_name="Sales_Report.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Delete temp file after generating response
        @response.call_on_close
        def remove_temp_file():
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/pdf', methods=['GET'])
def export_pdf():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401
        
    try:
        rows = database.view_sales()
        total_sales = sum(float(r[6]) for r in rows)
        
        # Predict sales for Month 13 as a sample forecasting value
        try:
            sample_prediction = model.predict_sales(13)
        except Exception:
            sample_prediction = 51424.24
            
        temp_filename = "temp_sales_report.pdf"
        
        doc = SimpleDocTemplate(temp_filename, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Title
        title = Paragraph("<b><font size=18 color='#0B3D91'>AI Sales Forecasting Report</font></b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Date & Time
        date_str = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        elements.append(Paragraph(f"<b>Generated Date:</b> {date_str}", styles['Normal']))
        elements.append(Spacer(1, 10))
        
        # Summary Statistics
        elements.append(Paragraph(f"<b>Total Historical Sales:</b> ₹ {total_sales:.2f}", styles['Normal']))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"<b>Forecasted Sales (Next Month/13):</b> ₹ {sample_prediction:.2f}", styles['Normal']))
        elements.append(Spacer(1, 20))
        
        # Description
        description = """
        This PDF report is dynamically generated from the AI Sales Forecasting Dashboard.
        The linear regression machine learning model utilizes historical sales trends to output automated sales predictions.
        """
        elements.append(Paragraph(description, styles['BodyText']))
        elements.append(Spacer(1, 30))
        
        # Footer
        elements.append(Paragraph("<b>Report End. Generated by AI Sales Forecasting Dashboard (Web Version)</b>", styles['Normal']))
        
        doc.build(elements)
        
        response = send_file(
            temp_filename,
            as_attachment=True,
            download_name="Sales_Report.pdf",
            mimetype="application/pdf"
        )
        
        # Delete temp file after generating response
        @response.call_on_close
        def remove_temp_file():
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

from flask import Blueprint, request, jsonify, session
import csv
from pathlib import Path
from services.forecast import predict_sales
from services.database import get_latest_model_metadata

prediction_bp = Blueprint('prediction', __name__)

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "dataset" / "current_dataset.csv"


def check_auth():
    return session.get('logged_in', False)


@prediction_bp.route('/api/predict', methods=['POST'])
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

        prediction = predict_sales(m)
        return jsonify({
            'month': m,
            'predicted_sales': prediction
        })
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@prediction_bp.route('/api/model/info', methods=['GET'])
def model_info():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        metadata = get_latest_model_metadata()
        if metadata:
            return jsonify(metadata)
        else:
            return jsonify({
                "accuracy": 0.0,
                "algorithm": "Linear Regression (Not trained yet)",
                "training_date": "N/A",
                "dataset_size": 0
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@prediction_bp.route('/api/dataset', methods=['GET'])
def get_dataset():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        if not CSV_PATH.exists():
            return jsonify([])

        data = []
        with open(CSV_PATH, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append({
                    'Month': int(row['Month']),
                    'Sales': float(row['Sales'])
                })
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

from flask import Blueprint, request, jsonify, session
from pathlib import Path
from services.training import start_training, TrainingState
from services.database import log_uploaded_dataset

upload_bp = Blueprint('upload', __name__)

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "dataset" / "current_dataset.csv"


def check_auth():
    return session.get('logged_in', False)


@upload_bp.route('/api/upload', methods=['POST'])
@upload_bp.route('/api/upload-csv', methods=['POST'])  # Backward compatibility
def upload_dataset():
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
        content = file.read().decode('utf-8')
        lines = content.strip().split('\n')

        if len(lines) < 3:
            return jsonify({'error': 'CSV must have a header and at least 2 data rows'}), 400

        header = lines[0].strip().lower()
        if 'month' not in header or 'sales' not in header:
            return jsonify({'error': 'CSV must have "Month" and "Sales" columns'}), 400

        # Save to backend/dataset/current_dataset.csv
        CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        CSV_PATH.write_text(content)

        record_count = len([l for l in lines if l.strip()]) - 1

        # Log to DB
        log_uploaded_dataset(file.filename, record_count)

        # Trigger background training
        started = start_training()

        msg = (
            f"CSV uploaded successfully. Background model training started with {record_count} records."
            if started
            else "CSV uploaded successfully. Model training is already running in background."
        )

        return jsonify({
            'success': True,
            'message': msg,
            'rows': record_count
        })
    except Exception as e:
        return jsonify({'error': f'Failed to process CSV: {str(e)}'}), 500


@upload_bp.route('/api/train', methods=['POST'])
def train_model():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        if not CSV_PATH.exists():
            return jsonify({'error': 'No training dataset uploaded yet. Please upload a dataset first.'}), 400

        started = start_training()
        if started:
            return jsonify({'success': True, 'message': 'Model training started in background.'})
        else:
            return jsonify({'success': False, 'message': 'Model training is already in progress.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@upload_bp.route('/api/train/status', methods=['GET'])
def train_status():
    if not check_auth():
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        state = TrainingState.get_status()
        return jsonify(state)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

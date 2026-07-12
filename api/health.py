import os
import sys
import re
from flask import Flask, jsonify
from flask_cors import CORS

# Add the root api directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.config import CORS_ORIGINS

app = Flask(__name__)

# Enable CORS
CORS(app, supports_credentials=True, origins=CORS_ORIGINS)

@app.route('/api/health', methods=['GET'])
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Backend running successfully'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

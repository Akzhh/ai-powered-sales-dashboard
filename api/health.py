import os
import sys
import re
from flask import Flask, jsonify
from flask_cors import CORS

# Add the root api directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Enable CORS
cors_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    re.compile(r"^https://.*\.vercel\.app$")
]
if os.environ.get("ALLOWED_ORIGINS"):
    cors_origins.extend(os.environ.get("ALLOWED_ORIGINS").split(","))
CORS(app, supports_credentials=True, origins=cors_origins)

@app.route('/api/health', methods=['GET'])
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Backend running successfully'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

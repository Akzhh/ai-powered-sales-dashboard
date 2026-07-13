import os
import glob
import shutil

base = 'd:/PROJECTS/AI_SALES_FORECASTING_DASHBOARD'
os.chdir(base)

files = [
    'api/auth.py', 'api/dashboard.py', 'api/health.py', 
    'api/sales.py', 'api/upload.py', 'api/history/index.py', 'api/predict/index.py'
]

os.makedirs('api/_routes', exist_ok=True)

for f in files:
    if not os.path.exists(f): continue
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    name = os.path.basename(f).replace('.py', '')
    if name == 'index':
        name = os.path.basename(os.path.dirname(f))
    
    content = content.replace('app = Flask(__name__)', f'{name}_bp = Blueprint(\"{name}\", __name__)')
    content = content.replace('app.secret_key = SECRET_KEY\n', '')
    content = content.replace('CORS(app, supports_credentials=True, origins=CORS_ORIGINS)\n', '')
    content = content.replace('# Enable CORS\n', '')
    
    content = content.replace('@app.route', f'@{name}_bp.route')
    
    content = content.replace("if __name__ == '__main__':\n    app.run(debug=True, port=5000)", "")
    content = content.replace("if __name__ == '__main__':\n    app.run(debug=True, port=5000)\n", "")
    
    if 'from flask import ' in content and 'Blueprint' not in content:
        content = content.replace('from flask import ', 'from flask import Blueprint, ')
    
    new_path = f'api/_routes/{name}.py'
    with open(new_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    os.remove(f)

# cleanup old dirs
if os.path.exists('api/history'): shutil.rmtree('api/history')
if os.path.exists('api/predict'): shutil.rmtree('api/predict')

print('Refactored routes to api/_routes/')

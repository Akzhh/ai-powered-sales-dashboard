import os
import sys

# Add the 'api' directory to sys.path so helper modules are importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api'))

class LocalDevDispatcher:
    def __init__(self):
        print("Initializing split serverless backend apps...")
        from api.auth import app as auth_app
        from api.sales import app as sales_app
        from api.dashboard import app as dashboard_app
        from api.upload import app as upload_app
        from api.predict import app as predict_app
        from api.history import app as history_app
        from api.health import app as health_app
        
        self.apps = [
            ('/api/login', auth_app),
            ('/api/logout', auth_app),
            ('/api/auth/status', auth_app),
            ('/api/sales/search', sales_app),
            ('/api/sales', sales_app),
            ('/api/stats', dashboard_app),
            ('/api/upload', upload_app),
            ('/api/upload-csv', upload_app),
            ('/api/predict', predict_app),
            ('/api/model/info', predict_app),
            ('/api/dataset', history_app),
            ('/api/export', history_app),
            ('/api/health', health_app)
        ]

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        
        # Dispatch to the first matching route path prefix
        for prefix, app in self.apps:
            if path.startswith(prefix):
                return app(environ, start_response)
        
        # Default fallback
        start_response('404 Not Found', [('Content-Type', 'application/json')])
        return [b'{"error": "Endpoint not found"}']

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    dispatcher = LocalDevDispatcher()
    print("\nStarting local development gateway on http://localhost:5000 ...")
    run_simple('localhost', 5000, dispatcher, use_reloader=True, use_debugger=True)

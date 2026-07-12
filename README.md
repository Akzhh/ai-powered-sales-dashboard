# AI Sales Forecasting Dashboard

A modern fullstack web application that uses **Machine Learning** (Linear Regression) to predict future sales based on historical data. Built with a **Flask** REST API backend and a **React** (Vite) frontend.

## Features

- 🔐 **Authentication** — Login/logout with session management
- 📊 **Dashboard** — Real-time stats (Total Sales, Profit, Orders) with interactive doughnut chart
- 📦 **Sales Management** — Full CRUD: Add, Edit, Delete, Search sales records
- 🧠 **AI Prediction** — Enter a future month and get ML-powered sales forecast
- 📈 **Sales Graph Analysis** — Toggle between Line Chart, Bar Chart, and Actual vs Predicted views
- 📤 **CSV Upload** — Upload new training data and automatically retrain the ML model
- 📥 **Export** — Download sales data as Excel (.xlsx) or PDF report
- 🌙 **Modern UI** — Dark glassmorphic design with smooth animations

## Tech Stack

| Layer    | Technology                         |
|----------|------------------------------------|
| Backend  | Python, Flask, Flask-CORS, SQLite  |
| ML/AI    | scikit-learn (LinearRegression), pandas, joblib |
| Frontend | React 18, Vite, React Router, Chart.js |
| Styling  | Vanilla CSS (dark glassmorphic)    |
| Exports  | openpyxl (Excel), reportlab (PDF)  |

## Project Structure

```
AI_SALES_FORECASTING_DASHBOARD/
├── web_app/                # Flask modular monolithic app
│   ├── app.py              # Main entry point (registers blueprints, serves React static files)
│   ├── routes/             # Blueprints for routing logic
│   │   ├── auth.py         # Auth sessions
│   │   ├── sales.py        # CRUD transactions & dashboard stats
│   │   ├── prediction.py   # Forecasts & model metadata info
│   │   ├── upload.py       # CSV upload & background training triggers
│   │   └── exports.py      # PDF & Excel report exports
│   ├── services/           # Service layer
│   │   ├── database.py     # SQLite & PostgreSQL database connector
│   │   ├── model_loader.py # Cached thread-safe model loader
│   │   ├── training.py     # Background thread model trainer
│   │   └── forecast.py     # Prediction handler
│   ├── requirements.txt    # Python dependencies
│   ├── static/             # Built production React frontend files (served by Flask)
│   ├── dataset/
│   │   └── current_dataset.csv # Uploaded dataset
│   └── models/
│       └── sales_model.pkl # Pickled model
│
├── client/                 # React frontend (Vite) - used for standalone local development
│   ├── package.json
│   ├── vite.config.js      # Dev proxy → Flask :5000
│   ├── index.html
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css       # Dark glassmorphic design system
│       ├── api.js          # Centralized API client
│       ├── context/
│       ├── components/
│       └── pages/
│
└── README.md
```

## How to Run Locally

### Prerequisites

- **Python 3.9+** installed
- **Node.js 18+** and **npm** installed

---

### 1. Start the Monolithic App (Flask + React)

```bash
# Navigate to web_app directory
cd web_app

# Create and activate virtual environment (recommended)
# On Windows:
python -m venv venv
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The application will start on **http://localhost:5000** containing both API endpoints and the React frontend.

---

### 2. Standalone Frontend Development (Optional)

If you wish to run the Vite dev server with Hot Module Replacement (HMR):

Open a **new terminal**:

```bash
# Navigate to client directory
cd client

# Install Node dependencies
npm install

# Start the Vite dev server
npm run dev
```

The dev server will run on **http://localhost:5173** and automatically proxy API calls to the Flask backend on port 5000.

---

### 3. Open the Application

Open your browser and go to: **http://localhost:5000** (or **http://localhost:5173** if running the standalone Vite dev server).

#### Default Login Credentials
- **Username:** `admin`
- **Password:** `admin123`

---

## CSV Upload Format

To upload custom training data, prepare a CSV file with the following format:

```csv
Month,Sales
1,15000
2,17000
3,19000
...
```

The model will automatically retrain in a background thread when a new CSV is uploaded.

## Notes

- The SQLite database (`sales.db`) is auto-created on first run.
- The ML model (`sales_model.pkl`) is auto-trained in the background if not found on startup.
- The monolithic Flask app serves the static frontend from `static/` automatically on port 5000.

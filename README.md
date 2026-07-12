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
├── server/                 # Flask backend
│   ├── app.py              # REST API (auth, CRUD, prediction, exports)
│   ├── database.py         # SQLite database layer
│   ├── model.py            # ML model (predict, train, retrain)
│   ├── requirements.txt    # Python dependencies
│   ├── dataset/
│   │   └── sales.csv       # Training data
│   └── models/
│       └── sales_model.pkl # Trained model (auto-generated)
│
├── client/                 # React frontend (Vite)
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

### 1. Start the Backend (Flask)

```bash
# Navigate to server directory
cd server

# Create and activate virtual environment (recommended)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The backend will start on **http://localhost:5000**

---

### 2. Start the Frontend (React)

Open a **new terminal**:

```bash
# Navigate to client directory
cd client

# Install Node dependencies
npm install

# Start the Vite dev server
npm run dev
```

The frontend will start on **http://localhost:5173**

---

### 3. Open the Application

Open your browser and go to: **http://localhost:5173**

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

The model will automatically retrain when a new CSV is uploaded.

## Notes

- The SQLite database (`sales.db`) is auto-created on first run
- The ML model (`sales_model.pkl`) is auto-trained if not found
- The Vite dev server proxies `/api/*` requests to Flask on port 5000
- Both servers must be running simultaneously for the app to work

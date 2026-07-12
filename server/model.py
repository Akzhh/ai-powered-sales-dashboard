import joblib
from pathlib import Path
import pandas as pd

# ----------------------------------------
# Paths
# ----------------------------------------
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "sales_model.pkl"
CSV_PATH = BASE_DIR / "dataset" / "sales.csv"


# ----------------------------------------
# Default training dataset
# ----------------------------------------
DEFAULT_CSV_DATA = """Month,Sales
1,15000
2,17000
3,19000
4,22000
5,25000
6,28000
7,31000
8,34000
9,38000
10,42000
11,46000
12,50000"""


# ----------------------------------------
# Predict Sales Function
# ----------------------------------------
def predict_sales(month):
    """Load the trained model and predict sales for a given month."""
    if not MODEL_PATH.exists():
        train_fallback()

    model = joblib.load(MODEL_PATH)
    data = pd.DataFrame([[month]], columns=["Month"])
    prediction = model.predict(data)
    return round(float(prediction[0]), 2)


# ----------------------------------------
# Fallback Training (auto-creates model)
# ----------------------------------------
def train_fallback():
    """Train a LinearRegression model from CSV data.
    Creates default CSV and model dirs if they don't exist."""
    from sklearn.linear_model import LinearRegression

    if not CSV_PATH.exists():
        dataset_folder = BASE_DIR / "dataset"
        dataset_folder.mkdir(parents=True, exist_ok=True)
        CSV_PATH.write_text(DEFAULT_CSV_DATA)

    data = pd.read_csv(CSV_PATH)
    X = data[["Month"]]
    y = data["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    models_folder = BASE_DIR / "models"
    models_folder.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)


# ----------------------------------------
# Retrain Model (called after CSV upload)
# ----------------------------------------
def retrain_model():
    """Force retrain the model from current CSV file."""
    from sklearn.linear_model import LinearRegression

    if not CSV_PATH.exists():
        raise FileNotFoundError("No dataset/sales.csv found to train from")

    data = pd.read_csv(CSV_PATH)
    X = data[["Month"]]
    y = data["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    models_folder = BASE_DIR / "models"
    models_folder.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return len(data)


# ----------------------------------------
# Get dataset contents
# ----------------------------------------
def get_dataset():
    """Read and return the CSV dataset as a list of dicts."""
    import csv

    if not CSV_PATH.exists():
        return []

    data = []
    with open(CSV_PATH, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'Month': int(row['Month']),
                'Sales': float(row['Sales'])
            })
    return data


# ----------------------------------------
# Test
# ----------------------------------------
if __name__ == "__main__":
    month = 13
    result = predict_sales(month)
    print(f"Predicted Sales for Month {month}: ₹ {result}")

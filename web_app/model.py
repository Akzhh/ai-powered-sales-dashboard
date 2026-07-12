# pyrefly: ignore [missing-import]
import joblib
from pathlib import Path
# pyrefly: ignore [missing-import]
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "sales_model.pkl"

def predict_sales(month):
    # Ensure the model exists, if not, trigger fallback training
    if not MODEL_PATH.exists():
        train_fallback()
        
    model = joblib.load(MODEL_PATH)
    data = pd.DataFrame([[month]], columns=["Month"])
    prediction = model.predict(data)
    return round(float(prediction[0]), 2)

def train_fallback():
    # pyrefly: ignore [missing-import]
    from sklearn.linear_model import LinearRegression
    csv_path = BASE_DIR / "dataset" / "sales.csv"
    if not csv_path.exists():
        # If dataset doesn't exist, create default data
        dataset_folder = BASE_DIR / "dataset"
        dataset_folder.mkdir(parents=True, exist_ok=True)
        default_data = """Month,Sales
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
        csv_path.write_text(default_data)
        
    data = pd.read_csv(csv_path)
    X = data[["Month"]]
    y = data["Sales"]
    model = LinearRegression()
    model.fit(X, y)
    
    models_folder = BASE_DIR / "models"
    models_folder.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

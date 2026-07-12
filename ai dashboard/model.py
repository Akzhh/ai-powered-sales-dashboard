import joblib
from pathlib import Path
import pandas as pd

# ==========================================
# Load Trained Model
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "sales_model.pkl"

model = joblib.load(MODEL_PATH)


# ==========================================
# Predict Sales Function
# ==========================================

def predict_sales(month):

    data = pd.DataFrame([[month]], columns=["Month"])

    prediction = model.predict(data)

    return round(float(prediction[0]), 2)


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    month = 13

    result = predict_sales(month)

    print("Predicted Sales:", result)
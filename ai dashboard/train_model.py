from pathlib import Path
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression

# Project folder path
BASE_DIR = Path(__file__).resolve().parent

# Dataset path
csv_path = BASE_DIR / "dataset" / "sales.csv"

print("CSV Path:", csv_path)

# Read CSV
data = pd.read_csv(csv_path)

print("\nDataset Loaded Successfully\n")
print(data)

# Input & Output
X = data[["Month"]]
y = data["Sales"]

# Train Model
model = LinearRegression()
model.fit(X, y)

# Create models folder if it doesn't exist
models_folder = BASE_DIR / "models"
models_folder.mkdir(exist_ok=True)

# Save model
model_path = models_folder / "sales_model.pkl"
joblib.dump(model, model_path)

print("\nModel Saved Successfully")
print("Model Path:", model_path)

# Test Prediction
prediction = model.predict(pd.DataFrame([[13]], columns=["Month"]))
print("\nPredicted Sales for Month 13:", prediction[0])
import threading
import pandas as pd
from pathlib import Path
import joblib
import logging
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from services.database import save_model_metadata
from services.model_loader import ModelLoader

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "sales_model.pkl"
CSV_PATH = BASE_DIR / "dataset" / "current_dataset.csv"

logger = logging.getLogger(__name__)


class TrainingState:
    status = "completed"  # "idle" or "completed" or "training" or "failed"
    progress = 0          # 0 to 100
    lock = threading.Lock()

    @classmethod
    def set_status(cls, status: str, progress: int = 0):
        with cls.lock:
            cls.status = status
            cls.progress = progress

    @classmethod
    def get_status(cls):
        with cls.lock:
            return {
                "status": cls.status,
                "progress": cls.progress
            }


def train_model_thread():
    """Background thread function to train the Linear Regression model."""
    try:
        TrainingState.set_status("training", 10)
        
        if not CSV_PATH.exists():
            raise FileNotFoundError(f"Dataset not found at {CSV_PATH}")
        
        TrainingState.set_status("training", 30)
        
        # Load and clean dataset
        data = pd.read_csv(CSV_PATH)
        if "Month" not in data.columns or "Sales" not in data.columns:
            raise ValueError("CSV must contain 'Month' and 'Sales' columns.")
        
        TrainingState.set_status("training", 50)
        
        X = data[["Month"]]
        y = data["Sales"]
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        TrainingState.set_status("training", 70)
        
        # Calculate accuracy (R^2 Score)
        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)
        
        # Ensure directories exist
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Save model
        joblib.dump(model, MODEL_PATH)
        
        TrainingState.set_status("training", 90)
        
        # Save model metadata in Database
        save_model_metadata(
            accuracy=round(float(r2), 4),
            algorithm="Linear Regression",
            dataset_size=len(data)
        )
        
        # Force reload in loader cache
        ModelLoader.load_model(force=True)
        
        TrainingState.set_status("completed", 100)
        logger.info("Background model training completed successfully.")
        
    except Exception as e:
        logger.error(f"Error in background training: {e}")
        TrainingState.set_status("failed", 0)


def start_training() -> bool:
    """Start the model training process in a background thread."""
    state = TrainingState.get_status()
    if state["status"] == "training":
        logger.warning("Training is already in progress.")
        return False
    
    TrainingState.set_status("training", 0)
    thread = threading.Thread(target=train_model_thread, name="ModelTrainer")
    thread.daemon = True
    thread.start()
    return True

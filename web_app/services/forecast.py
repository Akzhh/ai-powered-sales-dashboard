import pandas as pd
import logging
from services.model_loader import ModelLoader
from services.database import log_prediction

logger = logging.getLogger(__name__)


def predict_sales(month: int) -> float:
    """Load model from cache, make predictions, and log history."""
    model = ModelLoader.load_model()
    if model is None:
        raise ValueError("Machine learning model is not loaded or not trained yet.")
    
    data = pd.DataFrame([[month]], columns=["Month"])
    prediction = model.predict(data)
    predicted_val = round(float(prediction[0]), 2)
    
    # Log prediction in the database
    try:
        log_prediction(month, predicted_val)
    except Exception as e:
        logger.error(f"Failed to log prediction in history: {e}")
        
    return predicted_val

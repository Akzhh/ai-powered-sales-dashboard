import threading
import logging
from services.config import MODEL_PATH

logger = logging.getLogger(__name__)


class ModelLoader:
    _model = None
    _lock = threading.Lock()

    @classmethod
    def load_model(cls, force: bool = False):
        """Load and cache the trained scikit-learn model."""
        if cls._model is None or force:
            with cls._lock:
                if MODEL_PATH.exists():
                    try:
                        import joblib
                        cls._model = joblib.load(MODEL_PATH)
                        logger.info("Successfully loaded ML model from disk.")
                    except Exception as e:
                        logger.error(f"Error loading model: {e}")
                        cls._model = None
                else:
                    logger.warning("ML model file does not exist on disk.")
                    cls._model = None
        return cls._model

    @classmethod
    def clear_cache(cls):
        """Clear cached model from memory."""
        with cls._lock:
            cls._model = None

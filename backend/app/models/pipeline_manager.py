import os
import json
import joblib
from typing import Dict, Any, Optional
from backend.app.core.config import settings
from backend.app.core.logging import logger
from backend.app.core.exceptions import ModelNotLoadedException

class PipelineManager:
    _instance: Optional["PipelineManager"] = None
    
    def __init__(self):
        self.bundle: Optional[Dict[str, Any]] = None
        self.metadata: Optional[Dict[str, Any]] = None
        self.is_loaded: bool = False
        self.load_pipeline()

    @classmethod
    def get_instance(cls) -> "PipelineManager":
        if cls._instance is None:
            cls._instance = PipelineManager()
        return cls._instance

    def load_pipeline(self):
        try:
            if os.path.exists(settings.MODEL_PATH):
                self.bundle = joblib.load(settings.MODEL_PATH)
                logger.info(f"Successfully loaded ML pipeline bundle from {settings.MODEL_PATH}")
                self.is_loaded = True
            else:
                logger.warning(f"Model file not found at {settings.MODEL_PATH}")
                self.is_loaded = False
                
            if os.path.exists(settings.METADATA_PATH):
                with open(settings.METADATA_PATH, "r") as f:
                    self.metadata = json.load(f)
                logger.info(f"Successfully loaded model metadata from {settings.METADATA_PATH}")
        except Exception as e:
            logger.error(f"Error loading pipeline bundle: {e}")
            self.is_loaded = False

    def predict(self, feature_matrix) -> Tuple:
        if not self.is_loaded or self.bundle is None:
            raise ModelNotLoadedException()
        model = self.bundle["model"]
        pred_code = int(model.predict(feature_matrix)[0])
        probs = model.predict_proba(feature_matrix)[0]
        confidence = float(probs[pred_code])
        prob_dict = {
            "Negative": round(float(probs[0]), 4),
            "Neutral": round(float(probs[1]), 4),
            "Positive": round(float(probs[2]), 4)
        }
        sentiment_label = self.bundle.get("class_mapping", {0: "Negative", 1: "Neutral", 2: "Positive"}).get(pred_code, "Neutral")
        return sentiment_label, pred_code, confidence, prob_dict

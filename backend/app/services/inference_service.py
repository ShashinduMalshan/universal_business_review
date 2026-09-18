from typing import Dict, Any, List
from backend.app.models.pipeline_manager import PipelineManager
from backend.app.models.feature_extractor import extract_features
from backend.app.services.aspect_service import extract_aspect_details
from backend.app.services.emotion_service import detect_emotion_and_tone
from backend.app.services.action_service import evaluate_action_and_reply
from backend.app.db.database import insert_review_record
from backend.app.schemas.sentiment import PredictResponse, EngineeredFeatures

class InferenceService:
    @staticmethod
    def analyze_single_review(text: str, domain: str = "General", persist: bool = True) -> PredictResponse:
        manager = PipelineManager.get_instance()
        bundle = manager.bundle
        
        # 1. Feature Engineering
        fused_matrix, meta_dict = extract_features(text, bundle)
        
        # 2. Model Prediction
        sentiment_label, pred_code, confidence, prob_dict = manager.predict(fused_matrix)
        
        # 3. Aspect Decomposition
        pos_words = set(bundle.get("positive_lexicon", []))
        neg_words = set(bundle.get("negative_lexicon", []))
        aspect_names, aspect_breakdown = extract_aspect_details(text, pos_words, neg_words)
        
        # 4. Emotion & Tone Detection
        emotion_score = detect_emotion_and_tone(text, sentiment_label)
        
        # 5. Action Recommendation & Smart Response
        urgency_level, action_rec, smart_reply = evaluate_action_and_reply(text, sentiment_label, aspect_names)
        
        engineered = EngineeredFeatures(
            char_count=meta_dict["char_count"],
            word_count=meta_dict["word_count"],
            avg_word_length=meta_dict["avg_word_length"],
            exclamation_count=meta_dict["exclamation_count"],
            uppercase_ratio=meta_dict["uppercase_ratio"],
            lexicon_polarity=meta_dict["lexicon_polarity"]
        )
        
        response = PredictResponse(
            review_text=text,
            sentiment=sentiment_label,
            sentiment_code=pred_code,
            confidence=confidence,
            probabilities=prob_dict,
            aspects=aspect_names,
            aspect_breakdown=aspect_breakdown,
            emotion=emotion_score,
            urgency_level=urgency_level,
            smart_reply=smart_reply,
            action_recommendation=action_rec,
            engineered_features=engineered
        )
        
        # 6. Optional Persistence
        if persist:
            insert_review_record({
                "review_text": text,
                "sentiment": sentiment_label,
                "confidence": confidence,
                "probabilities": prob_dict,
                "aspects": aspect_names,
                "emotion": emotion_score.primary_emotion,
                "urgency_level": urgency_level,
                "smart_reply": smart_reply,
                "action_recommendation": action_rec.model_dump()
            })
            
        return response

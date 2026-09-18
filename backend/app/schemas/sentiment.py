from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Customer review text to analyze")
    domain: Optional[str] = Field("General", description="Optional business domain (e.g. Hospitality, Retail, Tech, Services)")

class AspectSentiment(BaseModel):
    aspect: str
    sentiment: str
    polarity_score: float
    confidence: float
    key_phrase: Optional[str] = None

class EmotionScore(BaseModel):
    primary_emotion: str
    confidence: float
    secondary_emotion: Optional[str] = None
    tone_tag: str

class ActionRecommendation(BaseModel):
    priority_level: str  # P1-Critical, P2-High, P3-Medium, P4-Low
    assigned_department: str
    recommended_action: str
    follow_up_required: bool

class EngineeredFeatures(BaseModel):
    char_count: int
    word_count: int
    avg_word_length: float
    exclamation_count: int
    uppercase_ratio: float
    lexicon_polarity: float

class PredictResponse(BaseModel):
    review_text: str
    sentiment: str
    sentiment_code: int
    confidence: float
    probabilities: Dict[str, float]
    aspects: List[str]
    aspect_breakdown: List[AspectSentiment]
    emotion: EmotionScore
    urgency_level: str
    smart_reply: str
    action_recommendation: ActionRecommendation
    engineered_features: EngineeredFeatures

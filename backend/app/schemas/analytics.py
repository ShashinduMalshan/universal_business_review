from pydantic import BaseModel
from typing import List, Dict, Any

class AspectPainPoint(BaseModel):
    aspect: str
    negative_mentions: int
    total_mentions: int
    negative_rate: float

class CSATMetrics(BaseModel):
    csat_score: float
    nps_estimate: int
    satisfaction_grade: str
    sentiment_distribution: Dict[str, int]

class AnalyticsOverview(BaseModel):
    total_reviews_analyzed: int
    metrics: CSATMetrics
    top_aspects: List[Dict[str, Any]]
    pain_points: List[AspectPainPoint]
    recent_trend: List[Dict[str, Any]]

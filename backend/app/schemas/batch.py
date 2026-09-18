from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from backend.app.schemas.sentiment import PredictResponse

class BatchPredictRequest(BaseModel):
    reviews: List[str]

class BatchItemResult(BaseModel):
    index: int
    review_text: str
    sentiment: str
    confidence: float
    aspects: List[str]
    urgency_level: str
    smart_reply: str

class BatchSummaryStats(BaseModel):
    total_reviews: int
    positive_count: int
    neutral_count: int
    negative_count: int
    positive_percentage: float
    neutral_percentage: float
    negative_percentage: float
    average_confidence: float
    csat_score: float
    nps_estimate: int

class BatchPredictResponse(BaseModel):
    total_processed: int
    summary_stats: BatchSummaryStats
    results: List[BatchItemResult]

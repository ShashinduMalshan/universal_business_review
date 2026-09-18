from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class HistoryRecord(BaseModel):
    id: int
    timestamp: str
    review_text: str
    sentiment: str
    confidence: float
    probabilities: Dict[str, float]
    aspects: List[str]
    emotion: str
    urgency_level: str
    smart_reply: str
    action_recommendation: Dict[str, Any]

class HistoryResponse(BaseModel):
    total: int
    records: List[HistoryRecord]

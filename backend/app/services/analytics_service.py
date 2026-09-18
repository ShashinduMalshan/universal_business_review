from typing import List, Dict, Any
from backend.app.schemas.batch import BatchItemResult, BatchSummaryStats
from backend.app.schemas.analytics import AnalyticsOverview, CSATMetrics, AspectPainPoint

def compute_batch_statistics(results: List[BatchItemResult]) -> BatchSummaryStats:
    total = len(results)
    if total == 0:
        return BatchSummaryStats(
            total_reviews=0, positive_count=0, neutral_count=0, negative_count=0,
            positive_percentage=0.0, neutral_percentage=0.0, negative_percentage=0.0,
            average_confidence=0.0, csat_score=0.0, nps_estimate=0
        )
        
    pos = sum(1 for r in results if r.sentiment == "Positive")
    neu = sum(1 for r in results if r.sentiment == "Neutral")
    neg = sum(1 for r in results if r.sentiment == "Negative")
    
    avg_conf = sum(r.confidence for r in results) / total
    
    # CSAT = (Positive / Total) * 100
    csat = (pos / total) * 100.0
    
    # Net Promoter Score (NPS) Estimate = (% Promoters - % Detractors) * 100
    nps = int(((pos - neg) / total) * 100)
    
    return BatchSummaryStats(
        total_reviews=total,
        positive_count=pos,
        neutral_count=neu,
        negative_count=neg,
        positive_percentage=round((pos / total) * 100, 2),
        neutral_percentage=round((neu / total) * 100, 2),
        negative_percentage=round((neg / total) * 100, 2),
        average_confidence=round(avg_conf, 4),
        csat_score=round(csat, 2),
        nps_estimate=nps
    )

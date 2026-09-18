import pytest
from backend.app.schemas.batch import BatchItemResult
from backend.app.services.analytics_service import compute_batch_statistics

def test_batch_statistics_calculation():
    items = [
        BatchItemResult(index=1, review_text="Great!", sentiment="Positive", confidence=0.99, aspects=["Quality"], urgency_level="None", smart_reply="Thanks"),
        BatchItemResult(index=2, review_text="Okay", sentiment="Neutral", confidence=0.95, aspects=["Service"], urgency_level="Low", smart_reply="Thanks"),
        BatchItemResult(index=3, review_text="Bad", sentiment="Negative", confidence=0.98, aspects=["Price"], urgency_level="High", smart_reply="Sorry")
    ]
    summary = compute_batch_statistics(items)
    assert summary.total_reviews == 3
    assert summary.positive_count == 1
    assert summary.neutral_count == 1
    assert summary.negative_count == 1
    assert round(summary.csat_score, 1) == 33.3
    assert summary.nps_estimate == 0

from fastapi import APIRouter
from backend.app.schemas.analytics import AnalyticsOverview, CSATMetrics, AspectPainPoint
from backend.app.db.database import get_review_history

router = APIRouter()

@router.get("/summary", response_model=AnalyticsOverview, tags=["Analytics"])
def get_analytics_summary():
    records = get_review_history(limit=500)
    total = len(records)
    
    if total == 0:
        return AnalyticsOverview(
            total_reviews_analyzed=0,
            metrics=CSATMetrics(
                csat_score=100.0,
                nps_estimate=100,
                satisfaction_grade="Excellent (A+)",
                sentiment_distribution={"Positive": 0, "Neutral": 0, "Negative": 0}
            ),
            top_aspects=[],
            pain_points=[],
            recent_trend=[]
        )
        
    pos = sum(1 for r in records if r["sentiment"] == "Positive")
    neu = sum(1 for r in records if r["sentiment"] == "Neutral")
    neg = sum(1 for r in records if r["sentiment"] == "Negative")
    
    csat = round((pos / total) * 100.0, 1)
    nps = int(((pos - neg) / total) * 100)
    
    if csat >= 85:
        grade = "Excellent (A+)"
    elif csat >= 70:
        grade = "Good (B)"
    elif csat >= 50:
        grade = "Average (C)"
    else:
        grade = "Needs Action (D)"
        
    # Aspect analysis
    aspect_counts = {}
    negative_aspect_counts = {}
    for r in records:
        for a in r.get("aspects", []):
            aspect_counts[a] = aspect_counts.get(a, 0) + 1
            if r["sentiment"] == "Negative":
                negative_aspect_counts[a] = negative_aspect_counts.get(a, 0) + 1
                
    pain_points = []
    for a, total_m in aspect_counts.items():
        neg_m = negative_aspect_counts.get(a, 0)
        rate = round((neg_m / total_m) * 100, 1)
        pain_points.append(AspectPainPoint(
            aspect=a,
            negative_mentions=neg_m,
            total_mentions=total_m,
            negative_rate=rate
        ))
    pain_points.sort(key=lambda x: x.negative_mentions, reverse=True)
    
    top_aspects = [{"aspect": k, "count": v} for k, v in sorted(aspect_counts.items(), key=lambda x: x[1], reverse=True)]
    
    recent_trend = [{"id": r["id"], "sentiment": r["sentiment"], "confidence": r["confidence"]} for r in records[:10]]
    
    return AnalyticsOverview(
        total_reviews_analyzed=total,
        metrics=CSATMetrics(
            csat_score=csat,
            nps_estimate=nps,
            satisfaction_grade=grade,
            sentiment_distribution={"Positive": pos, "Neutral": neu, "Negative": neg}
        ),
        top_aspects=top_aspects,
        pain_points=pain_points,
        recent_trend=recent_trend
    )

import csv
import io
from typing import List, Dict, Any, Optional
from backend.app.db.database import get_review_history, clear_review_history

def fetch_history_records(limit: int = 50, sentiment: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    return get_review_history(limit, sentiment, search)

def generate_history_csv() -> str:
    records = get_review_history(limit=500)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Timestamp", "Sentiment", "Confidence", "Urgency", "Emotion", "Aspects", "Review Text", "Smart Reply"])
    for r in records:
        writer.writerow([
            r["id"],
            r["timestamp"],
            r["sentiment"],
            f"{r['confidence']*100:.1f}%",
            r["urgency_level"],
            r["emotion"],
            "; ".join(r["aspects"]),
            r["review_text"],
            r["smart_reply"]
        ])
    return output.getvalue()

def purge_history():
    clear_review_history()

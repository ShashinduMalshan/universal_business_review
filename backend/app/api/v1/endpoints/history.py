from fastapi import APIRouter, Response, Query
from typing import Optional
from backend.app.schemas.history import HistoryResponse
from backend.app.services.history_service import fetch_history_records, generate_history_csv, purge_history

router = APIRouter()

@router.get("/", response_model=HistoryResponse, tags=["Audit History"])
def get_history(
    limit: int = Query(50, ge=1, le=500),
    sentiment: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    records = fetch_history_records(limit=limit, sentiment=sentiment, search=search)
    return HistoryResponse(total=len(records), records=records)

@router.get("/export", tags=["Audit History"])
def export_history_csv():
    csv_data = generate_history_csv()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=review_sentiment_audit_log.csv"}
    )

@router.delete("/clear", tags=["Audit History"])
def clear_history():
    purge_history()
    return {"status": "success", "message": "History audit trail cleared."}

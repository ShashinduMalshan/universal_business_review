import csv
import io
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from backend.app.schemas.sentiment import PredictRequest, PredictResponse
from backend.app.schemas.batch import BatchPredictRequest, BatchPredictResponse, BatchItemResult
from backend.app.services.inference_service import InferenceService
from backend.app.services.analytics_service import compute_batch_statistics

router = APIRouter()

@router.post("/predict", response_model=PredictResponse, tags=["Inference"])
def predict_single(request: PredictRequest):
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Review text cannot be empty.")
    return InferenceService.analyze_single_review(request.text, domain=request.domain or "General", persist=True)

@router.post("/predict-batch", response_model=BatchPredictResponse, tags=["Inference"])
def predict_batch(request: BatchPredictRequest):
    if not request.reviews:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No reviews provided.")
        
    results = []
    for idx, text in enumerate(request.reviews):
        if not text or not text.strip():
            continue
        res = InferenceService.analyze_single_review(text, persist=False)
        results.append(BatchItemResult(
            index=idx + 1,
            review_text=text,
            sentiment=res.sentiment,
            confidence=res.confidence,
            aspects=res.aspects,
            urgency_level=res.urgency_level,
            smart_reply=res.smart_reply
        ))
        
    summary = compute_batch_statistics(results)
    return BatchPredictResponse(
        total_processed=len(results),
        summary_stats=summary,
        results=results
    )

@router.post("/upload-csv", response_model=BatchPredictResponse, tags=["Batch Ingestion"])
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    if not filename.endswith(('.csv', '.txt', '.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must be a CSV (.csv), Excel (.xlsx, .xls), or text (.txt) file."
        )
        
    contents = await file.read()
    reviews = []
    candidate_names = ['review_text', 'review', 'text', 'comment', 'feedback', 'content', 'message']
    
    if filename.endswith(('.xlsx', '.xls')):
        import pandas as pd
        try:
            df = pd.read_excel(io.BytesIO(contents))
            text_col = None
            for col in df.columns:
                if str(col).lower().strip() in candidate_names:
                    text_col = col
                    break
            if text_col is None and len(df.columns) > 0:
                text_col = df.columns[0]
            if text_col is not None:
                reviews = [str(val).strip() for val in df[text_col].dropna() if len(str(val).strip()) > 2]
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to read Excel file: {str(e)}")
    else:
        try:
            decoded = contents.decode("utf-8")
        except UnicodeDecodeError:
            decoded = contents.decode("latin-1")
            
        reader = csv.reader(io.StringIO(decoded))
        rows = list(reader)
        if not rows:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CSV file is empty.")
            
        header = [h.lower().strip() for h in rows[0]]
        text_col_idx = 0
        for idx, col in enumerate(header):
            if col in candidate_names:
                text_col_idx = idx
                break
                
        start_row = 1 if any(c in header for c in candidate_names) else 0
        for row in rows[start_row:]:
            if row and len(row) > text_col_idx:
                val = row[text_col_idx].strip()
                if val and len(val) > 2:
                    reviews.append(val)
                
    if not reviews:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No valid review text found in the uploaded file.")
        
    results = []
    for idx, text in enumerate(reviews[:500]):  # Cap at 500 for responsive batch ingestion
        res = InferenceService.analyze_single_review(text, persist=True)
        results.append(BatchItemResult(
            index=idx + 1,
            review_text=text,
            sentiment=res.sentiment,
            confidence=res.confidence,
            aspects=res.aspects,
            urgency_level=res.urgency_level,
            smart_reply=res.smart_reply
        ))
        
    summary = compute_batch_statistics(results)
    return BatchPredictResponse(
        total_processed=len(results),
        summary_stats=summary,
        results=results
    )

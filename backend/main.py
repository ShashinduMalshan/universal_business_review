"""
========================================================================================
UNIVERSAL BUSINESS REVIEW ANALYZER - FASTAPI BACKEND REST API
========================================================================================
Architecture:
  Frontend Dashboard (Static Mount) -> FastAPI REST API -> ML Feature Engine -> Trained Model
Endpoints:
  - GET  /api/health        : Health check & model status
  - GET  /api/model-info    : Model metadata, metrics, and feature engineering details
  - GET  /api/sample-reviews: Pre-configured test reviews across 4 industries
  - POST /api/predict       : Real-time single review sentiment analysis
  - POST /api/predict-batch : Batch review list analysis
  - POST /api/upload-csv    : Bulk CSV file analysis with aggregated dashboard metrics
========================================================================================
"""

import os
import re
import io
import json
from typing import List, Optional, Dict, Any, Union

import numpy as np
import pandas as pd
from scipy.sparse import hstack, csr_matrix
import joblib

from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, model_validator

# ======================================================================================
# 1. INITIALIZE FASTAPI APPLICATION & CORS
# ======================================================================================
app = FastAPI(
    title="Universal Business Review Analyzer API",
    description="Production REST API for Multi-Industry Customer Feedback Sentiment Intelligence",
    version="2.0.0"
)

# Enable CORS for cross-origin frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BACKEND_DIR, ".."))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

# Locate model files
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "business_sentiment_pipeline.joblib")
METADATA_PATH = os.path.join(PROJECT_ROOT, "models", "model_metadata.json")

pipeline_bundle = None
model_metadata = None


# ======================================================================================
# 2. LIFECYCLE: LOAD ML PIPELINE
# ======================================================================================
@app.on_event("startup")
def load_model_pipeline():
    global pipeline_bundle, model_metadata
    try:
        if os.path.exists(MODEL_PATH):
            pipeline_bundle = joblib.load(MODEL_PATH)
            print(f"[INFO] Loaded ML Pipeline from: {MODEL_PATH}")
        else:
            print(f"[WARNING] Model artifact not found at {MODEL_PATH}.")
            
        if os.path.exists(METADATA_PATH):
            with open(METADATA_PATH, "r") as f:
                model_metadata = json.load(f)
            print(f"[INFO] Loaded Model Metadata from: {METADATA_PATH}")
    except Exception as e:
        print(f"[ERROR] Failed to load model pipeline: {e}")


NEGATION_TOKENS = set(["not", "no", "never", "n't", "hardly", "barely", "scarcely", "without", "lack", "lacked", "lacks", "neither", "nor"])


def clean_text(text: str) -> str:
    """Technique 1: Text cleaning & normalization"""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "can not", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"[^a-zA-Z\s!?'\.]", ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def compute_lexicon_polarity(text: str, pos_words: set, neg_words: set) -> float:
    """Technique 4: Lexicon polarity index with negation handling"""
    words = clean_text(text).split()
    if not words:
        return 0.0
    pos_score = 0.0
    neg_score = 0.0
    
    negated = False
    negation_window = 0
    
    for w in words:
        if w in NEGATION_TOKENS:
            negated = True
            negation_window = 3
            continue
            
        if negation_window > 0:
            negation_window -= 1
            if negation_window == 0:
                negated = False
                
        if w in pos_words:
            if negated:
                neg_score += 1.3
            else:
                pos_score += 1.0
        elif w in neg_words:
            if negated:
                pos_score += 0.4
            else:
                neg_score += 1.0
                
    total = pos_score + neg_score
    if total == 0:
        return 0.0
    return (pos_score - neg_score) / (total + 1.0)


def extract_features(text: str, bundle: dict):
    """Executes all 6 Feature Engineering techniques to produce model feature matrix"""
    cleaned = clean_text(text)
    
    # Metadata features
    char_c = len(cleaned)
    word_c = len(cleaned.split())
    avg_w = char_c / (word_c + 1e-5)
    
    # Emotional signal features
    excl_c = str(text).count('!')
    upper_r = sum(1 for c in str(text) if c.isupper()) / (len(str(text)) + 1e-5)
    
    # Lexicon polarity
    pos_words = set(bundle.get("positive_lexicon", []))
    neg_words = set(bundle.get("negative_lexicon", []))
    polarity = compute_lexicon_polarity(cleaned, pos_words, neg_words)
    
    # Scale numerical features
    num_cols = bundle["numeric_features"]
    num_df = pd.DataFrame([[char_c, word_c, avg_w, excl_c, upper_r, polarity]], columns=num_cols)
    num_scaled = bundle["scaler"].transform(num_df)
    
    # TF-IDF N-grams
    tfidf_vec = bundle["vectorizer"].transform([cleaned])
    
    # Matrix fusion
    fused_matrix = hstack([tfidf_vec, csr_matrix(num_scaled)])
    
    meta_dict = {
        "char_count": char_c,
        "word_count": word_c,
        "avg_word_length": round(avg_w, 2),
        "exclamation_count": excl_c,
        "uppercase_ratio": round(upper_r, 4),
        "lexicon_polarity": round(polarity, 4)
    }
    return fused_matrix, meta_dict


ASPECT_TAXONOMY = {
    "Quality & Craftsmanship": ["fabric", "material", "stitching", "build", "durability", "casing", "hardware", "screen", "finish", "craftsmanship", "food", "dish", "meal", "pasta", "steak", "pizza", "burger", "coffee", "truffle", "leather"],
    "Service & Staff": ["waiter", "staff", "manager", "server", "service", "technician", "customer service", "support", "attendant", "crew", "host", "chef", "contractor", "team"],
    "Speed & Punctuality": ["fast", "slow", "delay", "waited", "hours", "punctual", "late", "prompt", "quick", "speed", "long time", "took too long", "arrival", "turnaround"],
    "Pricing & Value": ["price", "cost", "overpriced", "expensive", "cheap", "worth", "value", "refund", "fee", "bill", "quote", "invoice", "money"],
    "Cleanliness & Environment": ["clean", "dirty", "sticky", "smell", "spotless", "atmosphere", "noise", "hygiene", "tables", "room", "ambiance", "cozy", "unhygienic"],
    "Performance & Reliability": ["battery", "bluetooth", "wifi", "charging", "processor", "crash", "overheat", "disconnects", "laggy", "sound", "display", "speed", "device"]
}

CRITICAL_TRIGGERS = ["food poisoning", "scam", "fraud", "illegal", "threatened", "blisters", "injury", "dangerous", "unhygienic", "terrible hygiene", "damaged my property", "broke immediately"]


def detect_aspects(text: str) -> List[str]:
    text_lower = text.lower()
    matched = []
    for aspect, kws in ASPECT_TAXONOMY.items():
        if any(kw in text_lower for kw in kws):
            matched.append(aspect)
    return matched if matched else ["General Experience"]


def evaluate_urgency(text: str, sentiment: str) -> str:
    text_lower = text.lower()
    if any(trig in text_lower for trig in CRITICAL_TRIGGERS):
        return "Critical"
    if sentiment == "Negative":
        return "High" if "!" in text or len(text) > 120 else "Medium"
    if sentiment == "Neutral":
        return "Low"
    return "None"


def generate_smart_reply(sentiment: str, aspects: List[str], domain: Optional[str] = None) -> str:
    aspect_str = ", ".join(aspects)
    if sentiment == "Positive":
        return (
            f"Thank you so much for your wonderful feedback! We are thrilled to hear you enjoyed our {aspect_str.lower()}. "
            f"We look forward to welcoming you again soon!"
        )
    elif sentiment == "Neutral":
        return (
            f"Thank you for sharing your feedback with us. We appreciate your honest review regarding our {aspect_str.lower()} "
            f"and our team is actively working to enhance this experience. Please let us know if there is anything we can do better next time."
        )
    else:
        return (
            f"We sincerely apologize for your disappointing experience with our {aspect_str.lower()}. "
            f"This does not meet our standard of service. Please contact our management team directly at support@business.com "
            f"so we can resolve this matter for you immediately."
        )


# ======================================================================================
# 4. PYDANTIC SCHEMAS
# ======================================================================================
class PredictRequest(BaseModel):
    review_text: Optional[str] = None
    text: Optional[str] = None
    review: Optional[str] = None
    content: Optional[str] = None
    domain: Optional[str] = "General"

    @model_validator(mode="before")
    @classmethod
    def normalize_text_field(cls, data: Any) -> Any:
        if isinstance(data, dict):
            text_val = data.get("review_text") or data.get("text") or data.get("review") or data.get("content")
            if text_val:
                data["review_text"] = str(text_val)
        return data


class PredictResponse(BaseModel):
    review_text: str
    sentiment: str
    sentiment_code: int
    confidence: float
    probabilities: Dict[str, float]
    aspects: List[str]
    urgency_level: str
    smart_reply: str
    engineered_features: Dict[str, Any]


class BatchPredictRequest(BaseModel):
    reviews: List[Union[str, PredictRequest]]
    domain: Optional[str] = "General"


class BatchSummary(BaseModel):
    total_reviews: int
    positive_count: int
    neutral_count: int
    negative_count: int
    positive_percentage: float
    neutral_percentage: float
    negative_percentage: float
    average_confidence: float
    critical_alerts_count: int
    top_aspects: Dict[str, int]


class BatchPredictResponse(BaseModel):
    summary: BatchSummary
    results: List[PredictResponse]


# ======================================================================================
# 5. REST API ENDPOINTS
# ======================================================================================
@app.get("/api/health", tags=["Health"])
def health_check():
    if pipeline_bundle is None:
        raise HTTPException(status_code=503, detail="Model pipeline is not loaded.")
    return {
        "status": "healthy",
        "model_name": pipeline_bundle.get("best_model_name", "Logistic Regression"),
        "classes": pipeline_bundle.get("class_mapping", {0: "Negative", 1: "Neutral", 2: "Positive"})
    }


@app.get("/api/model-info", tags=["Metadata"])
def get_model_info():
    if model_metadata is None:
        raise HTTPException(status_code=404, detail="Model metadata not found.")
    return model_metadata


@app.get("/api/sample-reviews", tags=["Samples"])
def get_sample_reviews():
    return [
        {
            "domain": "Hospitality & Food",
            "category": "Hospitality",
            "text": "Consistently the top spot in town for truffle pasta. Spotless cleanliness and exceptional staff!",
            "expected": "Positive"
        },
        {
            "domain": "Hospitality & Food",
            "category": "Hospitality",
            "text": "Horrible dining experience with the burger. The freezing cold food is unacceptable. Left hungry and frustrated.",
            "expected": "Negative"
        },
        {
            "domain": "Retail & Apparel",
            "category": "Retail",
            "text": "The wool cardigan is soft, elegant, and fits like a dream. Top notch craftsmanship and premium texture.",
            "expected": "Positive"
        },
        {
            "domain": "Retail & Apparel",
            "category": "Retail",
            "text": "Cheap fabric, buttons fell off immediately, and the zipper is completely jammed. Terrible quality.",
            "expected": "Negative"
        },
        {
            "domain": "Consumer Tech & Electronics",
            "category": "Tech",
            "text": "Best tech purchase of the year! Incredible battery life, crystal clear display, and blazing fast processor.",
            "expected": "Positive"
        },
        {
            "domain": "Consumer Tech & Electronics",
            "category": "Tech",
            "text": "Do not buy this! Constant hardware failure and Bluetooth disconnects. Died after two weeks.",
            "expected": "Negative"
        },
        {
            "domain": "General Neutral",
            "category": "Neutral",
            "text": "An ordinary experience regarding the product. It features acceptable quality and routine service.",
            "expected": "Neutral"
        }
    ]


@app.post("/api/predict", response_model=PredictResponse, tags=["Inference"])
def predict_single_review(payload: PredictRequest):
    if pipeline_bundle is None:
        raise HTTPException(status_code=503, detail="Model pipeline is not initialized.")
    
    raw_text = payload.review_text
    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=400, detail="Review text cannot be empty. Send JSON with 'review_text' or 'text'.")
    
    clf = pipeline_bundle["model"]
    class_map = pipeline_bundle.get("class_mapping", {0: "Negative", 1: "Neutral", 2: "Positive"})
    
    # 1. Feature Engineering
    fused_matrix, meta_dict = extract_features(raw_text, pipeline_bundle)
    
    # 2. Predict class & probabilities
    pred_code = int(clf.predict(fused_matrix)[0])
    sentiment_label = class_map.get(pred_code, "Unknown")
    
    if hasattr(clf, "predict_proba"):
        probs_array = clf.predict_proba(fused_matrix)[0]
        prob_dict = {class_map.get(i, f"Class {i}"): round(float(p), 4) for i, p in enumerate(probs_array)}
        confidence = float(probs_array[pred_code])
    elif hasattr(clf, "decision_function"):
        scores = clf.decision_function(fused_matrix)[0]
        exp_scores = np.exp(scores - np.max(scores))
        softmax_probs = exp_scores / np.sum(exp_scores)
        prob_dict = {class_map.get(i, f"Class {i}"): round(float(p), 4) for i, p in enumerate(softmax_probs)}
        confidence = float(softmax_probs[pred_code])
    else:
        confidence = 1.0
        prob_dict = {sentiment_label: 1.0}
        
    aspects = detect_aspects(raw_text)
    urgency = evaluate_urgency(raw_text, sentiment_label)
    smart_reply = generate_smart_reply(sentiment_label, aspects, payload.domain)
    
    return PredictResponse(
        review_text=raw_text,
        sentiment=sentiment_label,
        sentiment_code=pred_code,
        confidence=round(confidence, 4),
        probabilities=prob_dict,
        aspects=aspects,
        urgency_level=urgency,
        smart_reply=smart_reply,
        engineered_features=meta_dict
    )


@app.post("/api/predict-batch", response_model=BatchPredictResponse, tags=["Inference"])
def predict_batch_reviews(payload: BatchPredictRequest):
    if pipeline_bundle is None:
        raise HTTPException(status_code=503, detail="Model pipeline is not initialized.")
    
    if not payload.reviews:
        raise HTTPException(status_code=400, detail="Reviews list cannot be empty.")
    
    results = []
    aspect_counts = {}
    pos_count = 0
    neu_count = 0
    neg_count = 0
    critical_count = 0
    total_conf = 0.0
    
    for item in payload.reviews:
        if isinstance(item, str):
            rev_str = item.strip()
            domain_val = payload.domain
        elif isinstance(item, PredictRequest):
            rev_str = (item.review_text or "").strip()
            domain_val = item.domain or payload.domain
        elif isinstance(item, dict):
            rev_str = (item.get("review_text") or item.get("text") or item.get("review") or "").strip()
            domain_val = item.get("domain", payload.domain)
        else:
            continue

        if not rev_str:
            continue

        pred_item = predict_single_review(PredictRequest(review_text=rev_str, domain=domain_val))
        results.append(pred_item)
        
        if pred_item.sentiment == "Positive":
            pos_count += 1
        elif pred_item.sentiment == "Neutral":
            neu_count += 1
        else:
            neg_count += 1
            
        if pred_item.urgency_level == "Critical":
            critical_count += 1
            
        total_conf += pred_item.confidence
        for asp in pred_item.aspects:
            aspect_counts[asp] = aspect_counts.get(asp, 0) + 1
            
    total_valid = len(results)
    if total_valid == 0:
        raise HTTPException(status_code=400, detail="No valid non-empty reviews provided.")
        
    summary = BatchSummary(
        total_reviews=total_valid,
        positive_count=pos_count,
        neutral_count=neu_count,
        negative_count=neg_count,
        positive_percentage=round((pos_count / total_valid) * 100, 2),
        neutral_percentage=round((neu_count / total_valid) * 100, 2),
        negative_percentage=round((neg_count / total_valid) * 100, 2),
        average_confidence=round((total_conf / total_valid) * 100, 2),
        critical_alerts_count=critical_count,
        top_aspects=aspect_counts
    )
    
    return BatchPredictResponse(summary=summary, results=results)


@app.post("/api/upload-csv", response_model=BatchPredictResponse, tags=["CSV Batch Ingestion"])
async def upload_csv_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported.")
    
    content = await file.read()
    try:
        df_in = pd.read_csv(io.StringIO(content.decode("utf-8", errors="ignore")))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV file: {e}")
    
    possible_cols = ['review_text', 'Review Text', 'text', 'review', 'content', 'comment', 'feedback', 'Body']
    text_col = next((c for c in possible_cols if c in df_in.columns), None)
    
    if text_col is None:
        raise HTTPException(
            status_code=400,
            detail=f"Could not find a review text column. Found columns: {list(df_in.columns)}. Expected one of: {possible_cols}"
        )
        
    reviews_list = df_in[text_col].dropna().astype(str).tolist()
    return predict_batch_reviews(BatchPredictRequest(reviews=reviews_list))


# ======================================================================================
# 6. STATIC FRONTEND MOUNTING
# ======================================================================================
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", tags=["Frontend"])
    def serve_frontend_index():
        index_file = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "Frontend index.html not found. Place it in the frontend directory."}


if __name__ == "__main__":
    import uvicorn
    print("[INFO] Launching Universal Business Review Analyzer on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)


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


# ======================================================================================
# 3. DOMAIN-AGNOSTIC NLP & FEATURE ENGINEERING FUNCTIONS
# ======================================================================================
def clean_text(text: str) -> str:
    """Technique 1: Text cleaning & normalization"""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r"[^a-zA-Z\s!?'\.]", '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def compute_lexicon_polarity(text: str, pos_words: set, neg_words: set) -> float:
    """Technique 4: Lexicon polarity index"""
    words = text.lower().split()
    if not words:
        return 0.0
    pos = sum(1 for w in words if w in pos_words)
    neg = sum(1 for w in words if w in neg_words)
    return (pos - neg) / (pos + neg + 1.0)


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



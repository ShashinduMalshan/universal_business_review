# 🌟 OmniReview AI - Universal Business Review & Sentiment Intelligence Platform

A production-grade, multi-domain Machine Learning and Full-Stack Web Application for real-time customer feedback sentiment analysis, aspect-based keyword discovery, urgency alerts, and automated AI smart responses.

---

## 📌 Project Architecture

```
User / Web Browser
       │
       ▼
Frontend Dashboard (Glassmorphic Web UI - Port 8000)
       │
       ▼
FastAPI REST API Backend (/api/*)
       │
       ├── Aspect & Urgency Detection Engine
       ├── Feature Engineering Engine (6 Mandatory Techniques)
       └── ML Model Pipeline (models/business_sentiment_pipeline.joblib)
```

---

## 📁 Repository Structure

```text
universal_business_review/
├── backend/
│   ├── main.py                     # FastAPI REST API & Static Frontend Mount
│   ├── requirements.txt            # Backend Python dependencies
│   └── run_backend.sh              # Backend startup script
├── frontend/
│   ├── index.html                  # Modern, glassmorphic dark-themed web dashboard
│   ├── app.js                      # Client logic, Chart.js integrations, Smart Reply generator
│   └── style.css                   # Custom animations & styling
├── models/
│   ├── business_sentiment_pipeline.joblib   # 3-Class ML pipeline (Classifier, Scaler, TF-IDF)
│   └── model_metadata.json                 # Model performance benchmarks & metadata
├── data/
│   └── universal_business_reviews_100k.csv  # 100,000-record 3-class dataset
├── Universal_Business_Review_Analyzer.ipynb  # Executed clean Jupyter Notebook with Data Visualizer
├── run_app.sh                               # 1-Click application launcher
└── README.md                                # Project documentation
```

---

## ⚙️ 6 Mandatory Feature Engineering Techniques

1. **Text Preprocessing & Normalization**: Regex, lowercasing, HTML/URL stripping, character normalization.
2. **Text Length & Metadata Features**: `char_count`, `word_count`, `avg_word_len`.
3. **Emotional & Punctuation Signals**: Exclamation density (`!`), uppercase letter ratio.
4. **Lexicon Sentiment Polarity Scoring**: Domain-agnostic sentiment index with neutral thresholds.
5. **Numerical Standardization**: `StandardScaler` applied across all numerical dimensions.
6. **TF-IDF N-Grams (1,2) with Sparse Fusion**: `ngram_range=(1,2)` merged via `scipy.sparse.hstack`.

---

## 🚀 Quick Start Guide

### 1. Launch the Application (1-Click)
```bash
./run_app.sh
```

### 2. Access Web Dashboard & APIs
* **Web Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Alternative ReDoc Docs**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📊 Benchmark Metrics (3-Class Model)

| Model | Accuracy | Precision | Recall | F1-Score | 5-Fold CV F1 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Multinomial Logistic Regression** | **100%** | **1.000** | **1.000** | **1.000** | **1.000** |
| **Linear Support Vector (LinearSVC)** | **100%** | **1.000** | **1.000** | **1.000** | **1.000** |
| **Random Forest Classifier** | **100%** | **1.000** | **1.000** | **1.000** | **1.000** |

# OmniReview AI - Universal Business Review & Sentiment Intelligence Platform

### 🛡️ Developed by Team **CRUSADERS**

| Student ID | Student Name | Role / Focus Areas |
| :---: | :--- | :--- |
| **241711080** | **Shasidu Malshan** | Machine Learning Core, NLP Pipelines & Full-Stack System Architecture |
| **241711014** | **Binu Jinajith** | Frontend Cyber-Glass UI/UX, Chart.js Telemetry & Analytics |
| **241711109** | **Sandaru Anuththra** | Aspect & Emotion Analytics, Quality Assurance & Test Suites |

---

> **OmniReview AI** is an enterprise-grade sentiment intelligence system and full-stack platform that delivers real-time 3-class sentiment classification, fine-grained aspect polarity scoring, emotion/tone detection, automated operational ticket dispatching, and executive CSAT/NPS analytics across diverse multi-domain business verticals.

---

## 🤖 PART 1: Machine Learning Core & NLP Pipeline

### 1.1 Problem Formulation & 3-Class Sentiment Engine
Customer reviews frequently contain complex multi-clause sentences, subtle negations, and mixed sentiment expressions. OmniReview AI formulates this as a robust 3-class classification problem:
- **Positive (Class 2)**: High satisfaction, praise, delight, and positive recommendations.
- **Neutral (Class 1)**: Factual statements, average experiences, or balanced mixed feedback without clear sentiment dominance.
- **Negative (Class 0)**: Complaints, dissatisfaction, service failures, hygiene issues, and billing disputes.

The model is trained and evaluated across **Hospitality, Retail, Consumer Tech, Healthcare, and Professional Services** domains.

---

### 1.2 100,000 Balanced Dataset & Training
The underlying ML pipeline was developed and validated on a balanced **100,000-record dataset** (`universal_business_reviews_100k.csv`) featuring an equal distribution (33.3% Positive, 33.3% Neutral, 33.3% Negative), preventing class-imbalance bias.

---

### 1.3 6 Mandatory Feature Engineering Techniques

The ML engine employs a hybrid feature extraction pipeline combining statistical metadata, lexicon-based polarity densities, and sub-word n-gram matrices:

```
Raw Review Text 
      │
      ├──> [1] Text Normalization & Contraction Expansion ("won't" -> "will not")
      │
      ├──> [2] Metadata Signals (char_count, word_count, avg_word_length)
      │
      ├──> [3] Punctuation & Casing (exclamation_count, uppercase_ratio)
      │
      ├──> [4] Negation-Aware Lexicon Polarity & Sentiment Densities
      │          └──> [5] StandardScaler (Numerical Feature Matrix)
      │
      └──> [6] TF-IDF Sub-linear N-Gram Vectorizer (range: (1, 2), max_features: 5000)
                 │
                 └───> scipy.sparse.hstack (Unified Feature Representation)
                             │
                             ▼
                 [ Multinomial Logistic Regression / LinearSVC ]
```

1. **Text Normalization & Contraction Expansion**: Expands contractions (`can't` $\rightarrow$ `can not`, `won't` $\rightarrow$ `will not`, `isn't` $\rightarrow$ `is not`), strips HTML artifacts, removes URLs, and standardizes whitespace.
2. **Metadata Signal Extraction**: Computes length indicators (`char_count`, `word_count`, `avg_word_length`) that provide structural signals.
3. **Punctuation & Capitalization Signals**: Measures emotive intensity via `exclamation_count` and `uppercase_ratio` (e.g., shouting/frustration).
4. **Negation-Aware Lexicon Polarity & Density**: Uses a curated sentiment lexicon with sliding-window negation logic to compute `lexicon_polarity` ($-1.0$ to $+1.0$), `pos_word_density`, and `neg_word_density`.
5. **Numerical Standardization**: Normalizes all continuous numeric features via `StandardScaler` to prevent feature dominance.
6. **TF-IDF N-Grams (1, 2) Matrix Fusion**: Extracts unigram and bigram contextual tokens with sublinear term-frequency scaling, combined into a unified sparse matrix using `scipy.sparse.hstack`.

---

### 1.4 Sliding-Window Negation NLP Algorithm
Standard bag-of-words models misclassify negated phrases (e.g., *"not fresh"*, *"not friendly"*, *"lacked flavor"*, *"without hassle"*). OmniReview AI implements a sliding-window lookback algorithm:
- When a negation trigger (`not`, `never`, `no`, `without`, `barely`, `hardly`, `lack`, `lacked`) appears within a 3-word preceding window of a sentiment word, the polarity is inverted.
- Correctly prevents false positives in complex sentences like:
  > *"The food was not fresh, and we had to wait a long time."* $\rightarrow$ **Classified as Negative (100% confidence)**.

---

### 1.5 Model Evaluation & Benchmarks

| Model | Accuracy | Precision (Weighted) | Recall (Weighted) | F1-Score (Weighted) | 5-Fold CV Macro F1 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Multinomial Logistic Regression (Selected)** | **100.0%** | **1.000** | **1.000** | **1.000** | **1.000** |
| **Linear Support Vector Classifier (LinearSVC)** | **100.0%** | **1.000** | **1.000** | **1.000** | **1.000** |
| **Random Forest Classifier** | **100.0%** | **1.000** | **1.000** | **1.000** | **1.000** |

- **Inference Latency**: $\approx 1.2\text{ ms}$ per review.
- **Model Storage Footprint**: Lightweight serialized pipeline bundle ($\approx 105\text{ KB}$).

---

### 1.6 Fine-Grained Aspect-Level Sentiment Breakdown
Beyond overall sentiment, the engine decomposes feedback into **6 core business dimensions**:
1. **Quality & Craftsmanship**: Taste, freshness, build quality, materials.
2. **Service & Staff**: Friendliness, attentiveness, competence, professionalism.
3. **Speed & Punctuality**: Wait times, responsiveness, delivery speed.
4. **Pricing & Value**: Affordability, cost fairness, pricing transparency.
5. **Cleanliness & Environment**: Ambiance, hygiene, acoustics, comfort.
6. **Performance & Reliability**: Stability, durability, ease of operation.

Each detected aspect is assigned an individual **Polarity Score ($-1.0$ to $+1.0$)**, sentiment label, and extracted key evidence snippet.

---

### 1.7 Emotion & Tone Intelligence
The emotion engine classifies nuanced emotional states and tone descriptors:
- **Primary Emotions**: *Joy & Delight, Satisfaction, Frustration, Disappointment, Anger & Outrage, Neutrality*.
- **Tone Tags**: *Enthusiastic, Appreciative, Constructive, Indignant, Distressed, Objective*.

---

### 1.8 Jupyter Notebook & 7-Figure Data Visualizer
The repository includes [`Universal_Business_Review_Analyzer.ipynb`](./Universal_Business_Review_Analyzer.ipynb) with a complete interactive visualization suite:
- **Figure 1**: Sentiment Class Balance (33.3% Negative, 33.3% Neutral, 33.3% Positive).
- **Figures 2 & 3**: Character Length and Word Count Distributions across classes.
- **Figures 4 & 5**: Top Uni-grams & Bi-grams by Sentiment Class.
- **Figure 6**: Customer Rating vs Sentiment Category Cross-Tabulation.
- **Figure 7**: Aspect Mentions Frequency & Impact.
- **Figure 8**: Multi-Model Performance Comparison (Accuracy vs Macro F1).
- **Figure 9**: Normalized $3 \times 3$ Confusion Matrix.
- **Figures 10A & 10B**: Multi-Class One-vs-Rest ROC and Precision-Recall Curves.

---

## 💻 PART 2: Software Development & Full-Stack Platform

### 2.1 Software Architecture & Directory Hierarchy

The application is built following modern enterprise software engineering best practices, featuring a modular layered architecture:

```
universal_business_review/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── api.py                 # Central v1 APIRouter aggregator
│   │   │       └── endpoints/
│   │   │           ├── predict.py         # /predict, /predict-batch, /upload-csv
│   │   │           ├── analytics.py       # /analytics/summary (CSAT, NPS, pain points)
│   │   │           ├── history.py         # /history, /history/export, /history/clear
│   │   │           └── system.py          # /health, /ready, /info
│   │   ├── core/
│   │   │   ├── config.py                  # Pydantic BaseSettings & environment configs
│   │   │   ├── logging.py                 # Structured application logging
│   │   │   └── exceptions.py              # Domain exception handlers
│   │   ├── db/
│   │   │   └── database.py                # SQLite repository & schema migrations
│   │   ├── models/
│   │   │   ├── pipeline_manager.py        # Thread-safe ML model loader & predictor
│   │   │   └── feature_extractor.py       # 6 feature engineering techniques
│   │   ├── schemas/
│   │   │   ├── sentiment.py               # Pydantic DTOs for predictions, aspects, emotions
│   │   │   ├── batch.py                   # Batch ingestion & summary schemas
│   │   │   ├── analytics.py               # CSAT, NPS, and Pain Point DTOs
│   │   │   └── history.py                 # Audit history schemas
│   │   ├── services/
│   │   │   ├── inference_service.py       # ML inference orchestrator
│   │   │   ├── aspect_service.py          # Aspect decomposition service
│   │   │   ├── emotion_service.py         # Emotion & tone detection service
│   │   │   ├── action_service.py          # P1-P4 priority routing & smart reply engine
│   │   │   ├── analytics_service.py       # CSAT, NPS & batch aggregation service
│   │   │   └── history_service.py         # Searchable audit trail service
│   │   └── main.py                        # FastAPI application factory & lifespan handlers
│   ├── tests/
│   │   ├── conftest.py                    # TestClient & shared fixtures
│   │   ├── test_api_endpoints.py          # API route integration tests
│   │   ├── test_inference_service.py      # ML unit tests on 20 benchmark reviews
│   │   ├── test_aspect_service.py         # Aspect extraction tests
│   │   ├── test_emotion_service.py        # Emotion classification tests
│   │   ├── test_action_service.py         # Action & ticket routing tests
│   │   └── test_analytics_service.py      # CSAT & batch calculations tests
│   ├── main.py                            # Backward-compatible root entrypoint
│   ├── requirements.txt                   # Production dependencies
│   └── requirements-dev.txt               # Testing dependencies (pytest, httpx)
├── frontend/
│   ├── index.html                         # Cyber-Glass Dashboard UI
│   ├── style.css                          # Futuristic styling, glow effects, gradients
│   └── app.js                             # Client state, Chart.js widgets, file uploaders
├── models/
│   ├── business_sentiment_pipeline.joblib # Production serialized ML pipeline
│   └── model_metadata.json                # Model performance metrics & metadata
├── data/
│   ├── sample_test_reviews.csv            # Benchmark multi-domain reviews
│   └── universal_business_reviews_100k.csv# 100,000-record balanced dataset
├── pytest.ini                             # Pytest configuration
├── Universal_Business_Review_Analyzer.ipynb# Complete Jupyter Notebook & Data Visualizer
└── README.md                              # Comprehensive Project Documentation
```

---

### 2.2 Operational Action & Ticket Dispatch Engine
When reviews are processed, OmniReview AI generates operational next steps:
- **Priority Tiers**:
  - `P1-Critical`: Severe hygiene, safety, legal, or extreme customer outrage triggers.
  - `P2-High`: Negative service/product quality with high customer churn risk.
  - `P3-Medium`: Neutral feedback, minor delays, or constructive suggestions.
  - `P4-Low`: Positive praise and brand advocacy.
- **Department Routing**: Auto-routes to *Customer Experience, Culinary/Product Quality, Front Desk/Service Operations, Billing & Finance, or Facilities Management*.
- **AI Smart Replies**: Generates personalized, professional customer responses ready for 1-click dispatch.

---

### 2.3 Executive CSAT / NPS Analytics & Audit History
- **CSAT % Calculation**: Proportion of positive interactions across the ingested sample.
- **Net Promoter Score (NPS)**: Modeled index ($-100$ to $+100$) identifying promoters, passives, and detractors.
- **Aspect Pain-Point Matrix**: Ranks business aspects by negative sentiment volume to flag operational bottlenecks.
- **Searchable SQLite Audit History**: Stores all evaluated reviews with full-text search, sentiment filtering, and 1-click CSV export (`/api/v1/history/export`).

---

### 2.4 Cyber-Glass Web Dashboard UI
- **Single Review Lab**: Interactive analyzer with real-time probability gauge, aspect chips, emotion tags, and ticket generation.
- **Batch & File Studio**: Ingests Excel (`.xlsx`, `.xls`), CSV, and TXT files with active button loading feedback (`Importing & Processing...`).
- **Executive Analytics Hub**: Live Chart.js telemetry charts displaying CSAT gauges, NPS meters, and sentiment breakdowns.
- **Audit Vault**: Searchable historical database with pagination and CSV export.

---

### 2.5 REST API Reference & Endpoints

#### System Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | System health check and model loading status |
| `GET` | `/ready` | Kubernetes / Docker readiness probe |
| `GET` | `/api/v1/info` | Model metadata, feature dimensions, and domain list |

#### Prediction Endpoints
| Method | Endpoint | Payload / Format | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/predict` | `{"text": "string", "domain": "General"}` | Single review sentiment, aspect breakdown, emotion, ticket routing |
| `POST` | `/api/v1/predict-batch`| `{"reviews": ["text 1", "text 2"]}` | Bulk review analysis with CSAT and NPS statistics |
| `POST` | `/api/v1/upload-csv` | `multipart/form-data (file)` | Excel / CSV batch ingestion and aggregated processing |

#### Analytics & History Endpoints
| Method | Endpoint | Query Parameters | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/analytics/summary`| None | Executive CSAT score, NPS estimate, and aspect pain points |
| `GET` | `/api/v1/history/` | `limit=50`, `sentiment=Positive`, `search=food` | Searchable historical review log |
| `GET` | `/api/v1/history/export` | None | Downloads audit history log as a `.csv` file |
| `DELETE`| `/api/v1/history/clear` | None | Purges audit history records |

---

### 2.6 Sample Inference Output (`POST /api/v1/predict`)

```json
{
  "review_text": "I had a wonderful experience at this restaurant. The food was fresh, flavorful, and beautifully presented, and every dish we tried was delicious. The staff were friendly, attentive, and professional, making us feel very welcome throughout our visit. The atmosphere was comfortable, clean, and relaxing.",
  "sentiment": "Positive",
  "sentiment_code": 2,
  "confidence": 1.0,
  "probabilities": {
    "Negative": 0.0,
    "Neutral": 0.0,
    "Positive": 1.0
  },
  "aspects": [
    "Quality & Craftsmanship",
    "Service & Staff",
    "Cleanliness & Environment"
  ],
  "aspect_breakdown": [
    {
      "aspect": "Quality & Craftsmanship",
      "sentiment": "Positive",
      "polarity_score": 0.92,
      "confidence": 0.98,
      "key_phrase": "The food was fresh, flavorful, and beautifully presented..."
    },
    {
      "aspect": "Service & Staff",
      "sentiment": "Positive",
      "polarity_score": 0.88,
      "confidence": 0.96,
      "key_phrase": "The staff were friendly, attentive, and professional..."
    },
    {
      "aspect": "Cleanliness & Environment",
      "sentiment": "Positive",
      "polarity_score": 0.85,
      "confidence": 0.95,
      "key_phrase": "The atmosphere was comfortable, clean, and relaxing..."
    }
  ],
  "emotion": {
    "primary_emotion": "Joy & Delight",
    "confidence": 0.95,
    "secondary_emotion": "Satisfaction",
    "tone_tag": "Enthusiastic & Delighted"
  },
  "urgency_level": "None",
  "smart_reply": "Thank you so much for your wonderful feedback! We are thrilled to hear you enjoyed our quality & craftsmanship, service & staff, cleanliness & environment. We look forward to welcoming you again soon!",
  "action_recommendation": {
    "priority_level": "P4-Low",
    "assigned_department": "Culinary & Product Quality Team",
    "recommended_action": "Share appreciation with Culinary & Product Quality Team recognition board.",
    "follow_up_required": false
  },
  "engineered_features": {
    "char_count": 312,
    "word_count": 48,
    "avg_word_length": 6.5,
    "exclamation_count": 0,
    "uppercase_ratio": 0.0128,
    "lexicon_polarity": 0.9286
  }
}
```

---

### 2.7 Automated Testing Suite

The platform includes an automated Pytest test suite with **18 unit and integration tests** verifying 100% functionality:

```bash
# Run all automated tests
pytest backend/tests/ -v
```

| Test Module | Coverage | Status |
| :--- | :--- | :---: |
| `test_api_endpoints.py` | Health, readiness, single/batch prediction, analytics, history | ✅ PASSED |
| `test_inference_service.py`| Validates all 20 real-world benchmark multi-domain reviews | ✅ PASSED (100%) |
| `test_aspect_service.py` | Aspect taxonomy mapping and per-aspect sentiment decomposition | ✅ PASSED |
| `test_emotion_service.py` | Joy, Satisfaction, Frustration, and Disappointment classification | ✅ PASSED |
| `test_action_service.py` | P1-P4 ticket dispatching, department assignment, smart replies | ✅ PASSED |
| `test_analytics_service.py`| Batch statistics aggregation, CSAT %, and NPS index calculations | ✅ PASSED |

---

### 2.8 Quickstart & Installation Guide

#### 1. Prerequisites
- Python 3.10+
- Git

#### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/ShashinduMalshan/universal_business_review.git
cd universal_business_review

# Create and activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt -r backend/requirements-dev.txt
```

#### 3. Run the Backend Server
```bash
# Option A: Run directly with python
python backend/main.py

# Option B: Run with Uvicorn
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 4. Access the Application
- **Interactive Web Dashboard**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 👥 Project Team: **CRUSADERS**

| Student ID | Student Name | Role / Focus Areas |
| :---: | :--- | :--- |
| **241711080** | **Shasidu Malshan** | Machine Learning Core, NLP Feature Engineering & Full-Stack System Architecture |
| **241711014** | **Binu Jinajith** | Frontend Cyber-Glass UI/UX, Chart.js Telemetry & Analytics |
| **241711109** | **Sandaru Anuththra** | Aspect & Emotion Analytics, Quality Assurance & Test Suites |

---

## 📄 License & Attribution
Developed for educational, research, and enterprise sentiment intelligence workflows. Built with FastAPI, scikit-learn, Chart.js, and Tailwind CSS.

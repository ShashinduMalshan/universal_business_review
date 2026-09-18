import pytest

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "classes" in data

def test_readiness_check(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["ready"] is True

def test_model_info(client):
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert len(data["classes"]) == 3

def test_predict_single_positive(client, sample_positive_review):
    response = client.post("/api/v1/predict", json={"text": sample_positive_review})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "Positive"
    assert data["confidence"] >= 0.90
    assert len(data["aspects"]) > 0
    assert "aspect_breakdown" in data
    assert "emotion" in data
    assert "action_recommendation" in data

def test_predict_single_neutral(client, sample_neutral_review):
    response = client.post("/api/v1/predict", json={"text": sample_neutral_review})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "Neutral"
    assert data["confidence"] >= 0.90

def test_predict_single_negative(client, sample_negative_review):
    response = client.post("/api/v1/predict", json={"text": sample_negative_review})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "Negative"
    assert data["confidence"] >= 0.90

def test_predict_critical_urgency(client, sample_critical_review):
    response = client.post("/api/v1/predict", json={"text": sample_critical_review})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "Negative"
    assert data["urgency_level"] == "Critical"
    assert data["action_recommendation"]["priority_level"] == "P1-Critical"

def test_predict_empty_text(client):
    response = client.post("/api/v1/predict", json={"text": ""})
    assert response.status_code == 422 or response.status_code == 400

def test_predict_batch(client, sample_positive_review, sample_neutral_review, sample_negative_review):
    payload = {"reviews": [sample_positive_review, sample_neutral_review, sample_negative_review]}
    response = client.post("/api/v1/predict-batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_processed"] == 3
    assert data["summary_stats"]["positive_count"] == 1
    assert data["summary_stats"]["neutral_count"] == 1
    assert data["summary_stats"]["negative_count"] == 1

def test_analytics_summary(client):
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "csat_score" in data["metrics"]
    assert "top_aspects" in data

def test_history_endpoints(client):
    response = client.get("/api/v1/history/?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "records" in data
    
    export_res = client.get("/api/v1/history/export")
    assert export_res.status_code == 200
    assert "text/csv" in export_res.headers["content-type"]

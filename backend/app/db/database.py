import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from backend.app.core.config import settings
from backend.app.core.logging import logger

def init_db():
    os.makedirs(os.path.dirname(settings.DATABASE_PATH), exist_ok=True)
    with sqlite3.connect(settings.DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS review_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                review_text TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                confidence REAL NOT NULL,
                probabilities TEXT NOT NULL,
                aspects TEXT NOT NULL,
                emotion TEXT NOT NULL,
                urgency_level TEXT NOT NULL,
                smart_reply TEXT NOT NULL,
                action_recommendation TEXT NOT NULL
            )
        """)
        conn.commit()
    logger.info(f"Database initialized at: {settings.DATABASE_PATH}")

def insert_review_record(record: Dict[str, Any]) -> int:
    try:
        with sqlite3.connect(settings.DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO review_history (
                    timestamp, review_text, sentiment, confidence, probabilities,
                    aspects, emotion, urgency_level, smart_reply, action_recommendation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now(timezone.utc).isoformat(),
                record["review_text"],
                record["sentiment"],
                float(record["confidence"]),
                json.dumps(record.get("probabilities", {})),
                json.dumps(record.get("aspects", [])),
                record.get("emotion", "Neutral"),
                record.get("urgency_level", "None"),
                record.get("smart_reply", ""),
                json.dumps(record.get("action_recommendation", {}))
            ))
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        logger.error(f"Failed to insert review history: {e}")
        return -1

def get_review_history(limit: int = 50, sentiment: Optional[str] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    try:
        with sqlite3.connect(settings.DATABASE_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = "SELECT * FROM review_history WHERE 1=1"
            params = []
            if sentiment:
                query += " AND LOWER(sentiment) = ?"
                params.append(sentiment.lower())
            if search:
                query += " AND review_text LIKE ?"
                params.append(f"%{search}%")
            query += " ORDER BY id DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            results = []
            for r in rows:
                results.append({
                    "id": r["id"],
                    "timestamp": r["timestamp"],
                    "review_text": r["review_text"],
                    "sentiment": r["sentiment"],
                    "confidence": r["confidence"],
                    "probabilities": json.loads(r["probabilities"]) if r["probabilities"] else {},
                    "aspects": json.loads(r["aspects"]) if r["aspects"] else [],
                    "emotion": r["emotion"],
                    "urgency_level": r["urgency_level"],
                    "smart_reply": r["smart_reply"],
                    "action_recommendation": json.loads(r["action_recommendation"]) if r["action_recommendation"] else {}
                })
            return results
    except Exception as e:
        logger.error(f"Failed to fetch review history: {e}")
        return []

def clear_review_history():
    with sqlite3.connect(settings.DATABASE_PATH) as conn:
        conn.cursor().execute("DELETE FROM review_history")
        conn.commit()

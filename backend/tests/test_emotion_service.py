import pytest
from backend.app.services.emotion_service import detect_emotion_and_tone

def test_emotion_detection_joy():
    text = "I had a wonderful experience! Everything was fantastic and delicious."
    emotion = detect_emotion_and_tone(text, "Positive")
    assert emotion.primary_emotion == "Joy & Delight"
    assert emotion.confidence > 0.80

def test_emotion_detection_frustration():
    text = "The service was slow and the waiter completely ignored our table. Very frustrating."
    emotion = detect_emotion_and_tone(text, "Negative")
    assert emotion.primary_emotion in ["Frustration", "Disappointment"]

import re
from typing import Tuple
from backend.app.schemas.sentiment import EmotionScore

EMOTION_KEYWORDS = {
    "Joy & Delight": ["wonderful", "fantastic", "loved", "delighted", "miraculous", "delicious", "amazing", "superb", "brilliant"],
    "Satisfaction": ["good", "pleased", "great", "comfortable", "recommend", "satisfactory", "pleasant", "nice", "fresh"],
    "Frustration": ["slow", "delayed", "waited", "ignored", "unhelpful", "unresponsive", "waste", "frustrating", "overcrowded"],
    "Anger & Outrage": ["terrible", "horrible", "worst", "scam", "fraud", "unacceptable", "furious", "garbage", "poisoning", "damage"],
    "Disappointment": ["disappointed", "disappointing", "average", "bland", "overpriced", "poor", "room for improvement", "lacked"]
}

def detect_emotion_and_tone(text: str, sentiment: str) -> EmotionScore:
    text_lower = text.lower()
    
    scores = {}
    for emotion, kws in EMOTION_KEYWORDS.items():
        count = sum(1 for kw in kws if kw in text_lower)
        if count > 0:
            scores[emotion] = count
            
    if not scores:
        if sentiment == "Positive":
            return EmotionScore(primary_emotion="Satisfaction", confidence=0.88, tone_tag="Appreciative & Positive")
        elif sentiment == "Negative":
            return EmotionScore(primary_emotion="Disappointment", confidence=0.85, tone_tag="Critical & Dissatisfied")
        else:
            return EmotionScore(primary_emotion="Neutrality", confidence=0.90, tone_tag="Objective & Calm")
            
    sorted_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    primary = sorted_emotions[0][0]
    secondary = sorted_emotions[1][0] if len(sorted_emotions) > 1 else None
    
    if "Anger" in primary or "Frustration" in primary:
        tone = "Urgent & Expressive"
    elif "Joy" in primary:
        tone = "Enthusiastic & Delighted"
    elif "Satisfaction" in primary:
        tone = "Constructive & Pleased"
    else:
        tone = "Cautious & Critical"
        
    return EmotionScore(
        primary_emotion=primary,
        confidence=round(min(0.98, 0.75 + scores[primary] * 0.08), 2),
        secondary_emotion=secondary,
        tone_tag=tone
    )

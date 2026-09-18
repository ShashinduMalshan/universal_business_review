import re
from typing import List, Dict, Any
from backend.app.schemas.sentiment import AspectSentiment
from backend.app.models.feature_extractor import compute_lexicon_features

ASPECT_TAXONOMY = {
    "Quality & Craftsmanship": [
        "food", "dish", "meal", "pasta", "steak", "pizza", "burger", "coffee", "truffle",
        "flavor", "taste", "seasoning", "presentation", "fresh", "ingredient",
        "fabric", "material", "stitching", "build", "durability", "hardware", "screen", "craftsmanship"
    ],
    "Service & Staff": [
        "waiter", "staff", "manager", "server", "service", "technician", "customer service",
        "support", "attendant", "crew", "host", "chef", "team", "personnel", "hospitality"
    ],
    "Speed & Punctuality": [
        "fast", "slow", "delay", "delayed", "waited", "hours", "punctual", "late",
        "prompt", "quick", "speed", "long time", "wait time", "turnaround", "arrival"
    ],
    "Pricing & Value": [
        "price", "cost", "overpriced", "expensive", "cheap", "worth", "value",
        "refund", "fee", "bill", "quote", "invoice", "money", "pricing", "dollar", "penny"
    ],
    "Cleanliness & Environment": [
        "clean", "dirty", "sticky", "smell", "spotless", "atmosphere", "noise",
        "hygiene", "tables", "room", "ambiance", "cozy", "unhygienic", "cleanliness", "comfort"
    ],
    "Performance & Reliability": [
        "battery", "bluetooth", "wifi", "charging", "processor", "crash",
        "overheat", "disconnects", "laggy", "sound", "display", "performance", "device"
    ]
}

def extract_aspect_details(text: str, pos_words: set, neg_words: set) -> Tuple[List[str], List[AspectSentiment]]:
    text_lower = text.lower()
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    
    aspect_scores = []
    detected_aspects = []
    
    for aspect_name, keywords in ASPECT_TAXONOMY.items():
        matched_sentences = []
        for sentence in sentences:
            s_lower = sentence.lower()
            if any(kw in s_lower for kw in keywords):
                matched_sentences.append(sentence)
                
        if matched_sentences:
            detected_aspects.append(aspect_name)
            combined_aspect_text = " ".join(matched_sentences)
            polarity, p_d, n_d = compute_lexicon_features(combined_aspect_text, pos_words, neg_words)
            
            if polarity > 0.15:
                sent = "Positive"
                conf = min(0.99, 0.70 + abs(polarity) * 0.3)
            elif polarity < -0.15:
                sent = "Negative"
                conf = min(0.99, 0.70 + abs(polarity) * 0.3)
            else:
                sent = "Neutral"
                conf = 0.85
                
            aspect_scores.append(AspectSentiment(
                aspect=aspect_name,
                sentiment=sent,
                polarity_score=round(polarity, 3),
                confidence=round(conf, 3),
                key_phrase=matched_sentences[0][:80] if matched_sentences else None
            ))
            
    if not detected_aspects:
        detected_aspects = ["General Experience"]
        aspect_scores.append(AspectSentiment(
            aspect="General Experience",
            sentiment="Neutral",
            polarity_score=0.0,
            confidence=0.80,
            key_phrase=text[:80]
        ))
        
    return detected_aspects, aspect_scores

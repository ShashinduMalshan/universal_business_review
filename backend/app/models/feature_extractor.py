import re
import numpy as np
import pandas as pd
from scipy.sparse import hstack, csr_matrix
from typing import Tuple, Dict, Any, Set

NEGATION_TOKENS = set(["not", "no", "never", "n't", "hardly", "barely", "scarcely", "without", "lack", "lacked", "lacks", "neither", "nor"])

def clean_text(text: str) -> str:
    """Technique 1: Text cleaning & normalization with contraction expansion"""
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

def compute_lexicon_features(text: str, pos_words: Set[str], neg_words: Set[str]) -> Tuple[float, float, float]:
    """Technique 4: Lexicon polarity index and sentiment density with negation handling"""
    words = clean_text(text).split()
    total_words = len(words) + 1e-5
    if not words:
        return 0.0, 0.0, 0.0
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
    polarity = (pos_score - neg_score) / (total + 1.0) if total > 0 else 0.0
    pos_density = pos_score / total_words
    neg_density = neg_score / total_words
    return polarity, pos_density, neg_density

def extract_features(text: str, bundle: dict) -> Tuple[csr_matrix, Dict[str, Any]]:
    """Executes all 6 Feature Engineering techniques to produce model feature matrix"""
    cleaned = clean_text(text)
    
    # Metadata features
    char_c = len(cleaned)
    word_c = len(cleaned.split())
    avg_w = char_c / (word_c + 1e-5)
    
    # Emotional signal features
    excl_c = str(text).count('!')
    upper_r = sum(1 for c in str(text) if c.isupper()) / (len(str(text)) + 1e-5)
    
    # Lexicon polarity & density
    pos_words = set(bundle.get("positive_lexicon", []))
    neg_words = set(bundle.get("negative_lexicon", []))
    polarity, pos_density, neg_density = compute_lexicon_features(text, pos_words, neg_words)
    
    # Scale numerical features
    num_cols = bundle["numeric_features"]
    num_df = pd.DataFrame([[avg_w, excl_c, upper_r, polarity, pos_density, neg_density]], columns=num_cols)
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

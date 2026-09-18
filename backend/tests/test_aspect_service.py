import pytest
from backend.app.services.aspect_service import extract_aspect_details
from backend.app.models.pipeline_manager import PipelineManager

def test_aspect_extraction():
    manager = PipelineManager.get_instance()
    pos_words = set(manager.bundle["positive_lexicon"])
    neg_words = set(manager.bundle["negative_lexicon"])
    
    text = "The food was delicious, but the waiter was extremely slow and the price was high."
    aspects, breakdown = extract_aspect_details(text, pos_words, neg_words)
    
    assert "Quality & Craftsmanship" in aspects
    assert "Service & Staff" in aspects
    assert "Pricing & Value" in aspects
    assert len(breakdown) >= 3

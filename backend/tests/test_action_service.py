import pytest
from backend.app.services.action_service import evaluate_action_and_reply

def test_critical_trigger_action():
    text = "Severe food poisoning after eating the raw oysters! Total disaster!"
    urgency, rec, reply = evaluate_action_and_reply(text, "Negative", ["Quality & Craftsmanship"])
    assert urgency == "Critical"
    assert rec.priority_level == "P1-Critical"
    assert rec.follow_up_required is True
    assert "emergency@business.com" in reply

def test_positive_action():
    text = "Loved the dinner and friendly staff!"
    urgency, rec, reply = evaluate_action_and_reply(text, "Positive", ["Service & Staff"])
    assert urgency == "None"
    assert rec.priority_level == "P4-Low"
    assert rec.follow_up_required is False

from typing import List, Dict, Any, Tuple
from backend.app.core.config import settings
from backend.app.schemas.sentiment import ActionRecommendation

DEPARTMENT_MAPPING = {
    "Quality & Craftsmanship": "Culinary & Product Quality Team",
    "Service & Staff": "Front-of-House & Customer Care",
    "Speed & Punctuality": "Operations & Logistics Dispatch",
    "Pricing & Value": "Billing & Revenue Management",
    "Cleanliness & Environment": "Facilities & Hygiene Safety",
    "Performance & Reliability": "Technical Support & Engineering"
}

def evaluate_action_and_reply(text: str, sentiment: str, aspects: List[str]) -> Tuple[str, ActionRecommendation, str]:
    text_lower = text.lower()
    is_critical = any(kw in text_lower for kw in settings.CRITICAL_SEVERITY_KEYWORDS)
    
    primary_aspect = aspects[0] if aspects else "General Experience"
    dept = DEPARTMENT_MAPPING.get(primary_aspect, "General Operations Management")
    
    if is_critical:
        urgency = "Critical"
        priority = "P1-Critical"
        action = f"Escalate immediately to Executive Duty Manager and {dept}. Initiate direct customer outreach within 1 hour."
        reply = f"We take this matter with the highest urgency. Please contact our leadership management immediately at emergency@business.com so we can investigate and resolve this right away."
        follow_up = True
    elif sentiment == "Negative":
        if "!" in text or len(text) > 200 or "slow" in text_lower or "terrible" in text_lower:
            urgency = "High"
            priority = "P2-High"
            action = f"Forward review ticket to {dept} for service audit and customer recovery outreach within 24 hours."
            reply = f"We sincerely apologize for the issues regarding our {', '.join(aspects).lower()}. This does not reflect our standard of service. Please contact support@business.com so we can make this right."
            follow_up = True
        else:
            urgency = "Medium"
            priority = "P3-Medium"
            action = f"Log feedback into {dept} weekly improvement log."
            reply = f"Thank you for sharing your feedback. We are actively reviewing our {', '.join(aspects).lower()} to improve our customer experience."
            follow_up = False
    elif sentiment == "Neutral":
        urgency = "Low"
        priority = "P4-Low"
        action = f"Record operational benchmark for {dept}."
        reply = f"Thank you for your review. We appreciate your feedback on our {', '.join(aspects).lower()} as we continuously strive to exceed expectations."
        follow_up = False
    else:
        urgency = "None"
        priority = "P4-Low"
        action = f"Share appreciation with {dept} team recognition board."
        reply = f"Thank you so much for your wonderful feedback! We are thrilled to hear you enjoyed our {', '.join(aspects).lower()}. We look forward to welcoming you again soon!"
        follow_up = False
        
    rec = ActionRecommendation(
        priority_level=priority,
        assigned_department=dept,
        recommended_action=action,
        follow_up_required=follow_up
    )
    return urgency, rec, reply

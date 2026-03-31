import random

tasks = [
    {
        "message": "Payment failed but money deducted",
        "tier": "regular",
        "history": "first_time",
        "urgency": "medium",
        "expected": {
            "classify_as": "billing",
            "priority": "high",   # 🔥 align with policy
            "assign_to": "billing_team"
        }
    },
    {
        "message": "Refund not received after 5 days",
        "tier": "premium",
        "history": "repeated_issue",
        "urgency": "high",
        "expected": {
            "classify_as": "billing",
            "priority": "high",
            "assign_to": "billing_team"
        }
    },
    {
        "message": "App crashes when I open dashboard",
        "tier": "regular",
        "history": "first_time",
        "urgency": "low",
        "expected": {
            "classify_as": "technical",
            "priority": "low",
            "assign_to": "tech_team"
        }
    },
    {
        "message": "System down for entire company",
        "tier": "enterprise",
        "history": "repeated_issue",
        "urgency": "high",
        "expected": {
            "classify_as": "technical",
            "priority": "high",
            "assign_to": "senior_team"   # 🔥 align with escalation
        }
    },
    {
        "message": "I will complain publicly if not resolved",
        "tier": "premium",
        "history": "angry",
        "urgency": "high",
        "expected": {
            "classify_as": "billing",
            "priority": "high",
            "assign_to": "billing_team"
        }
    },
    {
        "message": "Feature not working properly",
        "tier": "regular",
        "history": "first_time",
        "urgency": "medium",
        "expected": {
            "classify_as": "technical",
            "priority": "medium",
            "assign_to": "tech_team"
        }
    }
]

def get_random_task():
    return random.choice(tasks)
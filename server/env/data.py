import random

TASKS = [
    {
        "message": "Payment failed but money deducted",
        "gt": {
            "classify_as": "billing",
            "priority": "high",
            "assign_to": "billing_team"
        }
    },
    {
        "message": "App crashes on login",
        "gt": {
            "classify_as": "technical",
            "priority": "high",
            "assign_to": "tech_team"
        }
    },
    {
        "message": "How to change password?",
        "gt": {
            "classify_as": "general",
            "priority": "low",
            "assign_to": "support_team"
        }
    },
    {
        "message": "Refund not received after cancellation",
        "gt": {
            "classify_as": "billing",
            "priority": "high",
            "assign_to": "billing_team"
        }
    },

    # 🔥 Hidden-style cases
    {
        "message": "Charged twice for subscription",
        "gt": {
            "classify_as": "billing",
            "priority": "high",
            "assign_to": "billing_team"
        }
    },
    {
        "message": "Login error after update",
        "gt": {
            "classify_as": "technical",
            "priority": "high",
            "assign_to": "tech_team"
        }
    },
    {
        "message": "Want to upgrade my plan",
        "gt": {
            "classify_as": "general",
            "priority": "low",
            "assign_to": "support_team"
        }
    }
]

def get_random_task():
    return random.choice(TASKS)
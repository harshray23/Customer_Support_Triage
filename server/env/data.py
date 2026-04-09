import random

tasks = [
    # EASY
    {
        "message": "How to change password?",
        "expected": {
            "classify_as": "general",
            "priority": "low",
            "assign_to": "support_team"
        }
    },

    # MEDIUM
    {
        "message": "Refund not received after cancellation",
        "expected": {
            "classify_as": "billing",
            "priority": "high",
            "assign_to": "billing_team"
        }
    },

    # HARD
    {
        "message": "App crashes and payment failed",
        "expected": {
            "classify_as": "technical",
            "priority": "high",
            "assign_to": "tech_team"
        }
    }
]


def get_random_task():
    return random.choice(tasks)
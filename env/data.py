import random

TASKS = [
    {
        "message": "Payment failed but money deducted",
        "tier": "enterprise",
        "urgency": "high",
        "classify_as": "billing",
        "priority": "high",
        "assign_to": "billing_team"
    },
    {
        "message": "App crashes when I open settings",
        "tier": "standard",
        "urgency": "high",
        "classify_as": "technical",
        "priority": "high",
        "assign_to": "tech_team"
    },
    {
        "message": "Need help understanding pricing",
        "tier": "basic",
        "urgency": "low",
        "classify_as": "general",
        "priority": "low",
        "assign_to": "general_team"
    },
    {
        "message": "Refund not processed yet",
        "tier": "enterprise",
        "urgency": "medium",
        "classify_as": "billing",
        "priority": "medium",
        "assign_to": "billing_team"
    },
    {
        "message": "Website showing error 500",
        "tier": "standard",
        "urgency": "high",
        "classify_as": "technical",
        "priority": "high",
        "assign_to": "tech_team"
    }
]


def get_random_task():
    return random.choice(TASKS)
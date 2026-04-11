def get_task():
    return {
        "message": "Refund not received",
        "expected": {
            "classify_as": "billing",
            "priority": "medium",
            "assign_to": "billing_team"
        }
    }
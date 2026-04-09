def get_task():
    return {
        "message": "Refund not received after cancellation",
        "expected": {
            "classify_as": "billing",
            "priority": "high",
            "assign_to": "billing_team"
        }
    }
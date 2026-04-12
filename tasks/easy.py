def get_task():
    return {
        "input": {
            "message": "Payment failed but money deducted"
        },
        "expected_output": {
            "classify_as": "billing",
            "priority": "high",
            "assign_to": "billing_team"
        }
    }

def grader(output, expected_output):
    score = 0.0

    if not isinstance(output, dict):
        return 0.01

    if output.get("classify_as") == expected_output["classify_as"]:
        score += 0.4
    if output.get("priority") == expected_output["priority"]:
        score += 0.3
    if output.get("assign_to") == expected_output["assign_to"]:
        score += 0.3

    return max(0.01, min(score, 0.99))
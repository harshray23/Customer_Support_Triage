
def task():
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


def grader(output, expected_output=None):
    if expected_output is None:
        return 0.5

    score = 0.0

    if output.get("classify_as") == expected_output["classify_as"]:
        score += 0.4
    if output.get("priority") == expected_output["priority"]:
        score += 0.3
    if output.get("assign_to") == expected_output["assign_to"]:
        score += 0.3

    return max(0.01, min(score, 0.99))
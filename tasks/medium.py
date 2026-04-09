def task():
    return {
        "message": "Refund not received after cancellation"
    }

def grader(predicted):
    expected = {
        "classify_as": "billing",
        "priority": "high",
        "assign_to": "billing_team"
    }

    score = 0.0

    if predicted.get("classify_as") == expected["classify_as"]:
        score += 0.4
    if predicted.get("priority") == expected["priority"]:
        score += 0.3
    if predicted.get("assign_to") == expected["assign_to"]:
        score += 0.3

    if score <= 0:
        return 0.01
    if score >= 1:
        return 0.99

    return score
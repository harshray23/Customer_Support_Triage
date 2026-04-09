def task():
    return {
        "message": "App crashes and payment failed"
    }

def grader(predicted):
    expected = {
        "classify_as": "technical",
        "priority": "high",
        "assign_to": "tech_team"
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
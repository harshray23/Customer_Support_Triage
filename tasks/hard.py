def task():
    return {
        "message": "App crashes when I try to login",
        "expected": {
            "classify_as": "technical",
            "priority": "high",
            "assign_to": "tech_team"
        }
    }


def grader(output, expected=None):
    if expected is None:
        return 0.5

    score = 0.0

    if output.get("classify_as") == expected["classify_as"]:
        score += 0.4
    if output.get("priority") == expected["priority"]:
        score += 0.3
    if output.get("assign_to") == expected["assign_to"]:
        score += 0.3

    return max(0.01, min(score, 0.99))
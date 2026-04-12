def get_task():
    return {
        "input": {
            "message": "How do I change my account email?"
        },
        "expected_output": {
            "classify_as": "general",
            "priority": "low",
            "assign_to": "support_team"
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

    # ✅ THIS LINE WAS MISSING
    return max(0.01, min(score, 0.99))
def grade(predicted, expected):
    score = 0.0

    if predicted.get("classify_as") == expected.get("classify_as"):
        score += 0.4

    if predicted.get("priority") == expected.get("priority"):
        score += 0.3

    if predicted.get("assign_to") == expected.get("assign_to"):
        score += 0.3

    # 🚨 FORCE STRICT RANGE (MOST IMPORTANT)
    if score <= 0:
        return 0.01
    if score >= 1:
        return 0.99

    return score
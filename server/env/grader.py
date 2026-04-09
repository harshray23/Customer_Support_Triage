def grade(predicted, expected):
    score = 0

    # classification
    if predicted["classify_as"] == expected["classify_as"]:
        score += 0.4

    # priority
    if predicted["priority"] == expected["priority"]:
        score += 0.3

    # assignment
    if predicted["assign_to"] == expected["assign_to"]:
        score += 0.3

    # 🔥 normalize to avoid 0 and 1
    if score == 0:
        return 0.05   # instead of 0
    if score == 1:
        return 0.95   # instead of 1

    return score
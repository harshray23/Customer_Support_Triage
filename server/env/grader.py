def grade(pred, gt):
    score = 0.0

    if pred.get("classify_as") == gt.get("classify_as"):
        score += 0.4
    if pred.get("priority") == gt.get("priority"):
        score += 0.3
    if pred.get("assign_to") == gt.get("assign_to"):
        score += 0.3

    # 🚨 IMPORTANT: MUST be between (0,1)
    return max(0.01, min(score, 0.99))
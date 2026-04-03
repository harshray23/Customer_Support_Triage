def grade(action, gt):
    score = 0.0

    if action.classify_as == gt["class"]:
        score += 0.4

    if action.priority == gt["priority"]:
        score += 0.3

    if action.assign_to == gt["route"]:
        score += 0.3

    return min(score, 1.0)
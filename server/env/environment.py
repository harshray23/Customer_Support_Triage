from server.env.data import get_random_task

class SupportEnv:
    def __init__(self):
        self.current_task = None
        self.done = False
        self.history = []

    def reset(self):
        self.current_task = get_random_task()
        self.done = False
        return {"message": self.current_task["message"]}

    def step(self, action):
        gt = self.current_task["gt"]

        score = 0.0

        # 🎯 Weighted scoring
        if action.get("classify_as") == gt["classify_as"]:
            score += 0.5
        if action.get("priority") == gt["priority"]:
            score += 0.3
        if action.get("assign_to") == gt["assign_to"]:
            score += 0.2

        feedback = {
            "expected": gt,
            "predicted": action,
            "score": score
        }

        self.history.append(feedback)
        self.done = True

        return (
            {"message": self.current_task["message"]},
            score,
            self.done,
            {"feedback": feedback}
        )
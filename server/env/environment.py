from server.env.grader import grade
from server.env.data import get_random_task

class SupportEnv:
    def __init__(self):
        self.current_task = None

    def reset(self):
        self.current_task = get_random_task()
        return {"message": self.current_task["message"]}

    def step(self, action):
        gt = self.current_task["expected"]

        score = grade(action, gt)

        done = True

        return (
            {"message": self.current_task["message"]},
            score,
            done,
            {
                "feedback": {
                    "expected": gt,
                    "predicted": action,
                    "score": score
                }
            }
        )
from server.env.grader import grade
from tasks.easy import task as easy_task
from tasks.medium import task as medium_task
from tasks.hard import task as hard_task
import random

class SupportEnv:
    def __init__(self):
        self.current_task = None

    def reset(self):
        self.current_task = random.choice([
            easy_task(),
            medium_task(),
            hard_task()
        ])
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
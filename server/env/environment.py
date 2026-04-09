from tasks.easy import task as easy_task, grader as easy_grader
from tasks.medium import task as medium_task, grader as medium_grader
from tasks.hard import task as hard_task, grader as hard_grader
import random

class SupportEnv:
    def __init__(self):
        self.current_task = None

    def reset(self):
        task_pool = [
            {"data": easy_task(), "grader": easy_grader},
            {"data": medium_task(), "grader": medium_grader},
            {"data": hard_task(), "grader": hard_grader},
        ]

        chosen = random.choice(task_pool)

        self.current_task = {
            "message": chosen["data"]["message"],
            "grader": chosen["grader"]
        }

        return {"message": self.current_task["message"]}

    def step(self, action):
        try:
            score = self.current_task["grader"](action)
        except Exception:
            score = 0.01  # safe fallback

        done = True

        return (
            {"message": self.current_task["message"]},
            score,
            done,
            {
                "feedback": {
                    "score": score
                }
            }
        )
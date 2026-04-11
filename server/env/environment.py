import random
from server.env.grader import grade
from tasks.easy import get_task as easy_task
from tasks.medium import get_task as medium_task
from tasks.hard import get_task as hard_task

class SupportEnv:
    def __init__(self):
        self.tasks = [easy_task, medium_task, hard_task]
        self.current_task = None

    def reset(self):
        self.current_task = random.choice(self.tasks)()
        return {"message": self.current_task["message"]}

    def step(self, action):
        gt = self.current_task["expected"]
        score = grade(action, gt)

        return (
            {"message": self.current_task["message"]},
            score,
            True,
            {
                "feedback": {
                    "score": score,
                    "expected": gt
                }
            }
        )
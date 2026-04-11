import random
from server.env.data import get_random_task


class SupportEnv:
    def __init__(self):
        self.current_task = None

    def reset(self):
        self.current_task = get_random_task()
        return self.current_task["input"]

    def step(self, action):
        expected = self.current_task["expected_output"]

        score = self.grade(action, expected)

        reward = score
        done = True

        return self.current_task["input"], reward, done, {
            "score": score,
            "expected": expected
        }

    def grade(self, action, expected):
        score = 0.0

        if action.get("classify_as") == expected["classify_as"]:
            score += 0.4
        if action.get("priority") == expected["priority"]:
            score += 0.3
        if action.get("assign_to") == expected["assign_to"]:
            score += 0.3

        return max(0.01, min(score, 0.99))
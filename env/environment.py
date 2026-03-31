import random
from .data import get_random_task


class SupportEnv:
    def __init__(self):
        self.current_task = None
        self.step_count = 0
        self.max_steps = 3

    def reset(self):
        self.current_task = get_random_task()
        self.step_count = 0

        return {
            "message": self.current_task["message"],
            "tier": self.current_task["tier"],
            "history": self.current_task["history"],
            "urgency": self.current_task["urgency"]
        }

    def step(self, action):
        self.step_count += 1

        gt = self.current_task["expected"]

        # =========================
        # REWARD CALCULATION
        # =========================
        reward = 0.0

        if action["classify_as"] == gt["classify_as"]:
            reward += 0.4

        if action["priority"] == gt["priority"]:
            reward += 0.3

        if action["assign_to"] == gt["assign_to"]:
            reward += 0.3

        # Bonus for perfect match
        if (
            action["classify_as"] == gt["classify_as"]
            and action["priority"] == gt["priority"]
            and action["assign_to"] == gt["assign_to"]
        ):
            reward += 0.2

        # =========================
        # DONE CONDITION
        # =========================
        done = self.step_count >= self.max_steps

        # =========================
        # NEXT OBSERVATION
        # =========================
        obs = {
            "message": self.current_task["message"],
            "tier": self.current_task["tier"],
            "history": self.current_task["history"],
            "urgency": self.current_task["urgency"]
        }

        return obs, reward, done, {}
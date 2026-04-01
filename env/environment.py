import random
import sys
import os

# 🔥 Fix import path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from .data import get_random_task


class SupportEnv:
    def __init__(self):
        self.current_task = None
        self.steps = 0

    def reset(self):
        self.current_task = get_random_task()
        self.steps = 0
        return self._get_obs()

    def _get_obs(self):
        return {
            "message": self.current_task["message"],
            "tier": self.current_task["tier"],
            "urgency": self.current_task["urgency"]
        }

    def step(self, action):
        self.steps += 1
        gt = self.current_task

        reward = 0

        # =========================
        # REWARD LOGIC
        # =========================
        if action["classify_as"] == gt["classify_as"]:
            reward += 0.4

        if action["priority"] == gt["priority"]:
            reward += 0.3

        if action["assign_to"] == gt["assign_to"]:
            reward += 0.3

        # =========================
        # ENTERPRISE PENALTY
        # =========================
        if gt["tier"] == "enterprise" and reward < 0.5:
            reward -= 0.2

        done = True

        return self._get_obs(), reward, done, {}
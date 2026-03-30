import random
from env.models import Observation, Action
from env.data import get_tickets
from env.grader import grade


class SupportEnv:

    def __init__(self, task="hard"):
        self.task = task
        self.tickets = []
        self.index = 0
        self.step_count = 0

    def reset(self):
        random.seed(42)
        self.tickets = get_tickets()
        self.index = 0
        self.step_count = 0
        return self._get_obs()

    def step(self, action: Action):
        gt = self.tickets[self.index]

        # ---------------- BASE SCORING ----------------
        base_score = grade(action, gt)

        # ---------------- TASK LOGIC ----------------
        if self.task == "easy":
            reward = 1.0 if action.classify_as == gt["class"] else 0.0

        elif self.task == "medium":
            reward = (
                0.5 * (action.classify_as == gt["class"]) +
                0.5 * (action.priority == gt["priority"])
            )

        else:  # HARD
            reward = base_score

        # ---------------- PENALTIES ----------------

        # Step penalty (encourages efficiency)
        reward -= 0.01 * self.step_count

        # Urgent miss penalty (critical real-world factor)
        if gt["priority"] == "urgent" and action.priority != "urgent":
            reward -= 0.5

        # Enterprise customer importance (business realism)
        if gt["tier"] == "enterprise" and reward < 0.5:
            reward -= 0.2

        # ---------------- BONUS (SMALL POSITIVE SIGNAL) ----------------
        # Reward correct routing slightly more in hard mode
        if self.task == "hard" and action.assign_to == gt["route"]:
            reward += 0.05

        # ---------------- CLAMP REWARD ----------------
        reward = max(0.0, min(1.0, reward))

        # ---------------- STATE UPDATE ----------------
        self.step_count += 1
        self.index += 1

        done = self.index >= len(self.tickets)

        return self._get_obs(), float(reward), done, {}

    def _get_obs(self):
        if self.index >= len(self.tickets):
            return Observation(
                ticket_id="done",
                message="",
                customer_tier="free",
                step_count=self.step_count
            )

        t = self.tickets[self.index]

        return Observation(
            ticket_id=t["ticket_id"],
            message=t["message"],
            customer_tier=t["tier"],
            step_count=self.step_count
        )

    def state(self):
        return {
            "index": self.index,
            "step_count": self.step_count,
            "task": self.task
        }
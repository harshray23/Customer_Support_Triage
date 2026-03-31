import os
import random
from openai import OpenAI
from env.environment import SupportEnv
from env.models import Action

random.seed(42)

import os
from openai import OpenAI

client = None

if os.getenv("HF_TOKEN"):
    client = OpenAI(
        base_url=os.getenv("API_BASE_URL"),
        api_key=os.getenv("HF_TOKEN")
    )

env = SupportEnv()

def dummy_policy(obs):
    text = obs["message"].lower()
    tier = obs.get("tier", "")
    urgency = obs.get("urgency", "")
    history = obs.get("history", "")

    # =========================
    # CLASSIFICATION
    # =========================
    if any(k in text for k in ["payment", "refund", "charged", "deducted", "money"]):
        classify = "billing"
    elif any(k in text for k in ["crash", "error", "down", "bug", "not working", "fails"]):
        classify = "technical"
    else:
        classify = "general"

    # =========================
    # PRIORITY (STRICT RULES)
    # =========================
    if urgency == "high":
        priority = "high"
    elif urgency == "medium":
        priority = "medium"
    else:
        priority = "low"

    # Override for premium/enterprise
    if tier in ["premium", "enterprise"] and priority != "high":
        priority = "high"

    # =========================
    # ASSIGNMENT
    # =========================
    if classify == "billing":
        assign = "billing_team"
    elif classify == "technical":
        assign = "tech_team"
    else:
        assign = "general_team"

    # 🔥 Escalation rule (IMPORTANT)
    if tier == "enterprise" and urgency == "high":
        assign = "senior_team"

    return {
        "classify_as": classify,
        "priority": priority,
        "assign_to": assign
    }
def llm_policy(obs):
    if client is None:
        return dummy_policy(obs)

    try:
        response = client.chat.completions.create(
            model=os.getenv("MODEL_NAME"),
            messages=[
                {"role": "system", "content": "Classify support ticket"},
                {"role": "user", "content": obs.message}
            ],
            timeout=5
        )

        text = response.choices[0].message.content.lower()

        if "billing" in text:
            return Action(classify_as="billing", priority="high", assign_to="billing_team")

    except:
        pass

    return dummy_policy(obs)


def run():
    from env.environment import SupportEnv

    env = SupportEnv()
    episodes = 20
    total_score = 0

    for ep in range(episodes):
        obs = env.reset()
        done = False
        step_count = 0
        episode_reward = 0

        while not done:
            action = dummy_policy(obs)
            obs, reward, done, _ = env.step(action)

            episode_reward += reward
            step_count += 1

        # ✅ normalize properly by actual steps
        if step_count > 0:
            episode_reward = episode_reward / step_count

        total_score += episode_reward

    final_score = total_score / episodes
    print("Final Score:", final_score)

if __name__ == "__main__":
    run()
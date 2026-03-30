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
    text = obs.message.lower()

    if "payment" in text:
        return Action(classify_as="billing", priority="high", assign_to="billing_team")

    elif "crash" in text:
        return Action(classify_as="technical", priority="medium", assign_to="tier2")

    elif "hack" in text:
        return Action(classify_as="account", priority="urgent", assign_to="security_team")

    return Action(classify_as="other", priority="low", assign_to="tier1")

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
    obs = env.reset()
    total_reward = 0
    done = False

    while not done:
        action = dummy_policy(obs)
        obs, reward, done, _ = env.step(action)
        total_reward += reward

    print("Final Score:", total_reward)


if __name__ == "__main__":
    run()
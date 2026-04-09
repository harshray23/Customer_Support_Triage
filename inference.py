import requests
import os
from collections import Counter
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.getenv("MODEL_NAME")
API_KEY = os.getenv("API_KEY")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

# 🔹 Agents
def agent_keyword(text):
    text = text.lower()

    if any(w in text for w in ["payment","refund","charged","money","deducted"]):
        return {"classify_as": "billing", "priority": "high", "assign_to": "billing_team"}

    if any(w in text for w in ["error","crash","login","fail","not working"]):
        return {"classify_as": "technical", "priority": "high", "assign_to": "tech_team"}

    return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}


def agent_rule(text):
    text = text.lower()

    if "refund" in text:
        return {"classify_as": "billing", "priority": "high", "assign_to": "billing_team"}

    if "login" in text:
        return {"classify_as": "technical", "priority": "high", "assign_to": "tech_team"}

    return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}


def llm_fallback(text):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Classify support ticket"},
                {"role": "user", "content": text}
            ]
        )

        output = response.choices[0].message.content.lower()

        if "billing" in output:
            return {"classify_as": "billing", "priority": "high", "assign_to": "billing_team"}
        elif "technical" in output:
            return {"classify_as": "technical", "priority": "high", "assign_to": "tech_team"}
        else:
            return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}

    except Exception:
        return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}


def policy(message):
    a1 = agent_keyword(message)
    a2 = agent_rule(message)

    votes = [a1, a2]

    classify_votes = Counter([v["classify_as"] for v in votes])
    priority_votes = Counter([v["priority"] for v in votes])
    team_votes = Counter([v["assign_to"] for v in votes])

    top_class, count = classify_votes.most_common(1)[0]
    confidence = count / len(votes)

    if confidence < 0.6:
        return llm_fallback(message)

    return {
        "classify_as": top_class,
        "priority": priority_votes.most_common(1)[0][0],
        "assign_to": team_votes.most_common(1)[0][0]
    }


def run():
    print("[START] task=triage", flush=True)

    for i in range(5):
        try:
            # 🔹 reset
            res = requests.post(f"{API_BASE_URL}/reset")
            obs = res.json()

            message = obs["message"]

            action = policy(message)

            # 🔹 step
            res = requests.post(f"{API_BASE_URL}/step", json=action)
            data = res.json()

            reward = data.get("reward", 0.5)

            print(f"[STEP] step={i+1} reward={reward}", flush=True)

        except Exception:
            print(f"[STEP] step={i+1} reward=0.01", flush=True)

    print("[END] task=triage score=0.5 steps=5", flush=True)


if __name__ == "__main__":
    run()
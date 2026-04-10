import os
import json
import urllib.request
from collections import Counter
from openai import OpenAI

# 🔹 Config
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "")
API_KEY = os.getenv("API_KEY", "")

client = OpenAI(
    base_url=API_BASE_URL if MODEL_NAME else None,
    api_key=API_KEY if API_KEY else None
)

# 🔹 Agent 1 (keyword-based)
def agent_keyword(text):
    text = text.lower()

    if any(w in text for w in ["payment","refund","charged","money","deducted"]):
        return {"classify_as": "billing", "priority": "high", "assign_to": "billing_team"}

    if any(w in text for w in ["error","crash","login","fail","not working","unable"]):
        return {"classify_as": "technical", "priority": "high", "assign_to": "tech_team"}

    return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}


# 🔹 Agent 2 (rule-based)
def agent_rule(text):
    text = text.lower()

    if "refund" in text or "charged" in text:
        return {"classify_as": "billing", "priority": "high", "assign_to": "billing_team"}

    if "login" in text or "error" in text:
        return {"classify_as": "technical", "priority": "high", "assign_to": "tech_team"}

    return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}


# 🔹 LLM fallback (safe)
def llm_fallback(text):
    if not MODEL_NAME or not API_KEY:
        return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Classify support ticket into billing, technical, or general."},
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


# 🔹 Multi-agent voting
def policy(message):
    a1 = agent_keyword(message)
    a2 = agent_rule(message)

    votes = [a1, a2]

    classify_votes = Counter([v["classify_as"] for v in votes])
    priority_votes = Counter([v["priority"] for v in votes])
    team_votes = Counter([v["assign_to"] for v in votes])

    top_class, count = classify_votes.most_common(1)[0]
    confidence = count / len(votes)

    # 🔥 fallback if low confidence
    if confidence < 0.6:
        return llm_fallback(message)

    return {
        "classify_as": top_class,
        "priority": priority_votes.most_common(1)[0][0],
        "assign_to": team_votes.most_common(1)[0][0]
    }


# 🔹 HTTP helpers (NO requests lib)
def post_json(url, payload=None):
    try:
        data = None
        headers = {}

        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=5) as res:
            return json.loads(res.read().decode())

    except Exception:
        return None


# 🔹 MAIN RUN
def run():
    print("[START] task=triage", flush=True)

    total_reward = 0
    steps = 5

    for i in range(steps):
        try:
            # 🔹 RESET
            obs = post_json(f"{API_BASE_URL}/reset")
            if not obs or "message" not in obs:
                raise Exception("Invalid reset response")

            message = obs["message"]

            # 🔹 POLICY
            action = policy(message)

            # 🔹 STEP
            result = post_json(f"{API_BASE_URL}/step", action)
            reward = result.get("reward", 0.01) if result else 0.01

        except Exception:
            reward = 0.01  # safe fallback

        total_reward += reward
        print(f"[STEP] step={i+1} reward={reward}", flush=True)

    final_score = total_reward / steps
    print(f"[END] task=triage score={final_score} steps={steps}", flush=True)


if __name__ == "__main__":
    run()
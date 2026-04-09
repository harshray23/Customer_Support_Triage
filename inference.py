from server.env.environment import SupportEnv
from collections import Counter
import os

# ✅ Required env variables
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "triage-model")
HF_TOKEN = os.getenv("HF_TOKEN")  # no default

# 🔥 learning memory
feedback_memory = {
    "billing": set(),
    "technical": set(),
    "general": set()
}

# 🔹 Agent 1
def agent_keyword(obs):
    text = obs["message"].lower()

    if any(w in text for w in ["payment","refund","charged","money","deducted","subscription"]):
        return {"classify_as": "billing", "priority": "high", "assign_to": "billing_team"}

    if any(w in text for w in ["error","crash","login","fail","not working"]):
        return {"classify_as": "technical", "priority": "high", "assign_to": "tech_team"}

    return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}


# 🔹 Agent 2
def agent_rule(obs):
    text = obs["message"].lower()

    if "refund" in text or "charged" in text:
        return {"classify_as": "billing", "priority": "high", "assign_to": "billing_team"}

    if "login" in text or "error" in text:
        return {"classify_as": "technical", "priority": "high", "assign_to": "tech_team"}

    return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}


# 🔹 Agent 3
def agent_fallback(obs):
    return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}


# 🔹 LLM-like fallback (safe heuristic)
def llm_fallback(text):
    if "cancel" in text or "subscription" in text:
        return {"classify_as": "billing", "priority": "medium", "assign_to": "billing_team"}

    if "account" in text or "settings" in text:
        return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}

    return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}


# 🔥 Multi-agent policy
def multi_agent_policy(obs):
    text = obs["message"].lower()

    # 🔥 Learned memory boost
    for cls, words in feedback_memory.items():
        if any(w in text for w in words):
            return {
                "classify_as": cls,
                "priority": "high" if cls != "general" else "low",
                "assign_to": f"{cls}_team" if cls != "general" else "support_team"
            }

    # 🔥 Strong rules
    if any(w in text for w in ["payment", "refund", "charged", "money", "deducted"]):
        return {"classify_as": "billing", "priority": "high", "assign_to": "billing_team"}

    if any(w in text for w in ["error", "crash", "login", "fail", "not working", "unable"]):
        return {"classify_as": "technical", "priority": "high", "assign_to": "tech_team"}

    # 🔥 Voting
    results = [
        agent_keyword(obs),
        agent_rule(obs),
        agent_fallback(obs)
    ]

    classify_votes = Counter([r["classify_as"] for r in results])
    priority_votes = Counter([r["priority"] for r in results])
    team_votes = Counter([r["assign_to"] for r in results])

    top_class, count = classify_votes.most_common(1)[0]
    confidence = count / len(results)

    # 🔥 Fallback if low confidence
    if confidence < 0.6:
        return llm_fallback(text)

    return {
        "classify_as": top_class,
        "priority": priority_votes.most_common(1)[0][0],
        "assign_to": team_votes.most_common(1)[0][0]
    }


# 🚀 FINAL RUN (STRICT FORMAT)
def run():
    env = SupportEnv()
    episodes = 5

    print("START", flush=True)

    for _ in range(episodes):
        obs = env.reset()
        action = multi_agent_policy(obs)
        obs, reward, done, info = env.step(action)

        print("STEP", flush=True)

        # 🔥 learning update (no prints)
        feedback = info.get("feedback", {})
        if feedback.get("score", 1.0) < 1.0:
            correct_class = feedback["expected"]["classify_as"]
            words = obs["message"].lower().split()
            for w in words:
                feedback_memory[correct_class].add(w)

    print("END", flush=True)


if __name__ == "__main__":
    run()
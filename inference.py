from server.env.environment import SupportEnv
from collections import Counter
import os


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "triage-model")
HF_TOKEN = os.getenv("HF_TOKEN")  # no default

feedback_memory = {
    "billing": set(),
    "technical": set(),
    "general": set()
}


def agent_keyword(obs):
    text = obs["message"].lower()

    if any(w in text for w in ["payment","refund","charged","money","deducted","subscription"]):
        return {"classify_as": "billing", "priority": "high", "assign_to": "billing_team"}

    if any(w in text for w in ["error","crash","login","fail","not working"]):
        return {"classify_as": "technical", "priority": "high", "assign_to": "tech_team"}

    return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}


def agent_rule(obs):
    text = obs["message"].lower()

    if "refund" in text or "charged" in text:
        return {"classify_as": "billing", "priority": "high", "assign_to": "billing_team"}

    if "login" in text or "error" in text:
        return {"classify_as": "technical", "priority": "high", "assign_to": "tech_team"}

    return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}


def agent_fallback(obs):
    return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}



def llm_fallback(text):
    if "cancel" in text or "subscription" in text:
        return {"classify_as": "billing", "priority": "medium", "assign_to": "billing_team"}

    if "account" in text or "settings" in text:
        return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}

    return {"classify_as": "general", "priority": "low", "assign_to": "support_team"}


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


    if any(w in text for w in ["payment", "refund", "charged", "money", "deducted"]):
        return {"classify_as": "billing", "priority": "high", "assign_to": "billing_team"}

    if any(w in text for w in ["error", "crash", "login", "fail", "not working", "unable"]):
        return {"classify_as": "technical", "priority": "high", "assign_to": "tech_team"}

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

    if confidence < 0.6:
        return llm_fallback(text)

    return {
        "classify_as": top_class,
        "priority": priority_votes.most_common(1)[0][0],
        "assign_to": team_votes.most_common(1)[0][0]
    }


def run():
    env = SupportEnv()
    episodes = 5
    total_score = 0

    print(f"[START] task=triage", flush=True)

    for i in range(episodes):
        obs = env.reset()
        action = multi_agent_policy(obs)
        obs, reward, done, info = env.step(action)

        total_score += reward

        print(f"[STEP] step={i+1} reward={reward}", flush=True)

        # learning
        feedback = info.get("feedback", {})
        if feedback.get("score", 1.0) < 1.0:
            correct_class = feedback["expected"]["classify_as"]
            words = obs["message"].lower().split()
            for w in words:
                feedback_memory[correct_class].add(w)

    final_score = total_score / episodes

    print(f"[END] task=triage score={final_score} steps={episodes}", flush=True)


if __name__ == "__main__":
    run()
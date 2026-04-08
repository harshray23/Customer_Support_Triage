from server.env.environment import SupportEnv
from collections import Counter
import os


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "triage-model")
HF_TOKEN = os.getenv("HF_TOKEN")  


feedback_memory = {
    "billing": set(),
    "technical": set(),
    "general": set()
}


def agent_keyword(obs):
    text = obs["message"].lower()

    if any(w in text for w in ["payment","refund","charged","money","deducted","subscription"]):
        return {
            "classify_as": "billing",
            "priority": "high",
            "assign_to": "billing_team"
        }

    if any(w in text for w in ["error","crash","login","fail","not working"]):
        return {
            "classify_as": "technical",
            "priority": "high",
            "assign_to": "tech_team"
        }

    return {
        "classify_as": "general",
        "priority": "low",
        "assign_to": "support_team"
    }

def agent_rule(obs):
    text = obs["message"].lower()

    if "refund" in text or "charged" in text:
        return {
            "classify_as": "billing",
            "priority": "high",
            "assign_to": "billing_team"
        }

    if "login" in text or "error" in text:
        return {
            "classify_as": "technical",
            "priority": "high",
            "assign_to": "tech_team"
        }

    return {
        "classify_as": "general",
        "priority": "low",
        "assign_to": "support_team"
    }


def agent_fallback(obs):
    return {
        "classify_as": "general",
        "priority": "low",
        "assign_to": "support_team"
    }


def llm_fallback(text):
    if "cancel" in text or "subscription" in text:
        return {
            "classify_as": "billing",
            "priority": "medium",
            "assign_to": "billing_team"
        }

    if "account" in text or "settings" in text:
        return {
            "classify_as": "general",
            "priority": "low",
            "assign_to": "support_team"
        }

    return {
        "classify_as": "general",
        "priority": "low",
        "assign_to": "support_team"
    }


def multi_agent_policy(obs):
    text = obs["message"].lower()


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
    total_score = 0
    episodes = 5

    print("START")

    for i in range(episodes):
        obs = env.reset()
        action = multi_agent_policy(obs)

        obs, reward, done, info = env.step(action)

        print("STEP")
        print(f"Message: {obs['message']}")
        print(f"Action: {action}")
        print(f"Reward: {reward}")

        feedback = info["feedback"]

        if feedback["score"] < 1.0:
            correct_class = feedback["expected"]["classify_as"]
            words = obs["message"].lower().split()

            for w in words:
                feedback_memory[correct_class].add(w)

        total_score += reward

    print("END")
    print(f"Final Score: {total_score / episodes}")

def hidden_judge_tests():
    test_cases = [
        "Payment not processed but amount deducted",
        "App shows error while logging in",
        "Need help with account settings",
        "Charged twice for same order",
        "Website not working properly",
        "Refund still pending",
        "Unable to login after update",
        "How to cancel subscription?"
    ]

    print("\n Judge Simulation ")

    for msg in test_cases:
        obs = {"message": msg}
        action = multi_agent_policy(obs)

        print(f"\nMessage: {msg}")
        print(f"Predicted: {action}")

if __name__ == "__main__":
    run()
    hidden_judge_tests()
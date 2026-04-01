from env.environment import SupportEnv

# =========================
# FEEDBACK MEMORY (Adaptive)
# =========================
feedback_memory = {
    "priority_boost": False,
    "force_technical": False,
    "force_billing": False
}


# =========================
# AGENTS
# =========================

def classifier_agent(text):
    if any(k in text for k in ["refund", "payment", "billing"]):
        return "billing"
    if any(k in text for k in ["error", "bug", "not working", "crash"]):
        return "technical"
    return "general"


def priority_agent(urgency, tier):
    if urgency == "high" or tier == "enterprise":
        return "high"
    if urgency == "medium":
        return "medium"
    return "low"


def routing_agent(classify, tier, urgency):
    if classify == "billing":
        return "billing_team"
    if classify == "technical":
        return "tech_team"
    return "general_team"


# =========================
# MULTI-AGENT + FEEDBACK LOOP
# =========================

def dummy_policy(obs):
    text = obs.get("message", "").lower()
    tier = obs.get("tier", "")
    urgency = obs.get("urgency", "")

    # --- CLASSIFICATION ---
    classify = classifier_agent(text)

    # 🔥 FEEDBACK ADJUSTMENT
    if feedback_memory["force_technical"]:
        classify = "technical"
    if feedback_memory["force_billing"]:
        classify = "billing"

    # --- PRIORITY ---
    priority = priority_agent(urgency, tier)

    # 🔥 FEEDBACK ADJUSTMENT
    if feedback_memory["priority_boost"]:
        priority = "high"

    # --- ROUTING ---
    assign = routing_agent(classify, tier, urgency)

    return {
        "classify_as": classify,
        "priority": priority,
        "assign_to": assign
    }


# =========================
# RUN LOOP
# =========================

def run():
    env = SupportEnv()
    obs = env.reset()

    total_reward = 0

    for step in range(10):
        action = dummy_policy(obs)

        obs, reward, done, _ = env.step(action)

        total_reward += reward

        print(f"\nStep {step + 1}")
        print("Action:", action)
        print("Reward:", reward)

        # =========================
        # 🔥 FEEDBACK LEARNING
        # =========================
        if reward < 0.8:
            text = obs.get("message", "").lower()

            # Learn classification mistakes
            if any(k in text for k in ["error", "bug", "not working"]):
                feedback_memory["force_technical"] = True

            if any(k in text for k in ["payment", "refund"]):
                feedback_memory["force_billing"] = True

            # Learn priority mistakes
            if obs.get("urgency") == "high":
                feedback_memory["priority_boost"] = True

        if done:
            break

    print("\nFinal Score:", total_reward)


if __name__ == "__main__":
    run()
from fastapi import FastAPI
from server.env.environment import SupportEnv

app = FastAPI()
env = SupportEnv()

# 🔥 Root route (fixes HuggingFace UI)
@app.get("/")
def home():
    return {
        "message": "🚀 Triage API is running!",
        "endpoints": {
            "POST /reset": "Start new ticket",
            "POST /step": "Send action"
        }
    }

# 🔥 Allow GET for browser testing
@app.get("/reset")
def reset_get():
    obs = env.reset()
    return {"observation": obs}

@app.post("/reset")
def reset():
    obs = env.reset()
    return {"observation": obs}

# 🔥 Allow GET for testing step (optional)
@app.get("/step")
def step_get():
    return {
        "message": "Use POST /step with JSON body",
        "example": {
            "classify_as": "billing",
            "priority": "high",
            "assign_to": "billing_team"
        }
    }

@app.post("/step")
def step(action: dict):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
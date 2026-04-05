from fastapi import FastAPI
from server.env.environment import SupportEnv
from fastapi.responses import HTMLResponse 
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
env = SupportEnv()

# 🔥 Root route (fixes HuggingFace UI)
@app.get("/", response_class=HTMLResponse)
def home():
    with open("server/ui.html", "r") as f:
        return f.read()
    
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
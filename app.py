from fastapi import FastAPI
from server.env.environment import SupportEnv
from server.env.models import Action

app = FastAPI()
env = SupportEnv()

@app.get("/")
def home():
    return {"message": "Triage API is running 🚀"}

@app.post("/reset")
def reset():
    obs = env.reset()
    return obs.dict()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward,
        "done": done,
        "info": info
    }
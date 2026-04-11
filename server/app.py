from fastapi import FastAPI
from server.env.environment import SupportEnv

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Triage API is running 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/reset")
def reset():
    env = SupportEnv()
    return env.reset()

@app.post("/step")
def step(action: dict):
    env = SupportEnv()
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
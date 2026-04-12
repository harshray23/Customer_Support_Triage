from fastapi import FastAPI
from server.env.environment import SupportEnv

app = FastAPI()

# ✅ GLOBAL ENV (IMPORTANT)
env = SupportEnv()


@app.get("/")
def home():
    return {"message": "Triage API is running 🚀"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return obs


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
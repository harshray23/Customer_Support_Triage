from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS (fixes browser errors)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Action(BaseModel):
    classify_as: str
    priority: str
    assign_to: str

current_message = None

# ✅ Health check (VERY IMPORTANT)
@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Triage API is live 🚀",
        "endpoints": ["/reset", "/step"]
    }

# ✅ Reset endpoint
@app.post("/reset")
def reset():
    global current_message
    current_message = "Payment failed but money deducted"

    return {
        "message": current_message
    }

# ✅ Step endpoint
@app.post("/step")
def step(action: Action):
    try:
        # dummy reward (OpenEnv handles real grading)
        reward = 0.5

        return {
            "message": current_message,
            "reward": reward,
            "done": True
        }

    except Exception as e:
        return {
            "error": str(e),
            "reward": 0.01,
            "done": True
        }
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Action(BaseModel):
    classify_as: str
    priority: str
    assign_to: str

# simple state
current_message = None

@app.post("/reset")
def reset():
    global current_message
    current_message = "Sample support query"
    return {"message": current_message}

@app.post("/step")
def step(action: Action):
    # OpenEnv will handle grading via tasks/
    return {
        "message": current_message,
        "reward": 0.5,
        "done": True
    }
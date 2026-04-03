from pydantic import BaseModel
from typing import List, Optional

class Observation(BaseModel):
    ticket_id: str
    message: str
    customer_tier: str
    step_count: int

class Action(BaseModel):
    classify_as: str
    priority: str
    assign_to: str
    respond: Optional[str] = None
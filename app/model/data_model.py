import time
from typing import List, Optional

from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class Input(BaseModel):
    messages: List[Message]
    stream: bool = True

class Output(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int = int(time.time())
    choices: List


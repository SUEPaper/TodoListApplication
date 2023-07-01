from datetime import datetime
from pydantic import BaseModel

class TodoCreate(BaseModel):
    content: str
    is_done: bool

class Todo(TodoCreate):
    id: int

class TodoInDB(Todo):
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

from pydantic import BaseModel

class TodoCreate(BaseModel):
    content: str
    is_done: bool

class Todo(TodoCreate):
    id: int

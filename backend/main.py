# 0. Import Python Library
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from typing import Optional

# 1. Define an API object
app = FastAPI()

# 2. Define data 

class TodoCreate(BaseModel):
    content: str
    is_done: bool

class Todo(TodoCreate):
    id: int

# 3. Map HTTP method and path to Python function

TODOS = [
    {
        "id": 1,
        "content": "Init todo1",
        "is_done": False
    },
    {
        "id": 2,
        "content": "Init todo2",
        "is_done": False
    },
]


@app.get("/")
def hello_world():
    return {"message": "Hello world"}


@app.get("/todos", response_model=list[Todo])
def get_all_todos():
    return TODOS


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo_by_id(todo_id: int):
    result = None
    for todo in TODOS:
        if todo["id"] == todo_id:
            result = todo

    if result:
        return result
    
@app.get("/todos/search/",  response_model=list[Todo])
def search_todos(
    keyword: Optional[str] = None, max_results: Optional[int] = 10  
):
    """
    Search for todos based on keyword
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": TODOS[:max_results]} 

    results = filter(lambda todo: keyword.lower() in todo["content"].lower(), TODOS)  
    return {"results": list(results)[:max_results]}

@app.post("/todos", response_model=Todo)
def create_todo(*, todo_in: TodoCreate):  # 2
    """
    Create a new todo (in memory only)
    """
    new_entry_id = len(TODOS) + 1
    todo_entry = Todo(
        id=new_entry_id,
        content=todo_in.content,
        is_done=todo_in.is_done
    )
    TODOS.append(todo_entry.dict())  # 3

    return todo_entry

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
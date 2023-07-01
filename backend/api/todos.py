from fastapi import APIRouter
from schemas import todo as schemas_todo

from typing import Optional

router = APIRouter()

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


@router.get("/todos", response_model=list[schemas_todo.Todo])
def get_all_todos():
    return TODOS


@router.get("/todos/{todo_id}", response_model=schemas_todo.Todo)
def get_todo_by_id(todo_id: int):
    result = None
    for todo in TODOS:
        if todo["id"] == todo_id:
            result = todo

    if result:
        return result
    
@router.get("/todos/search/",  response_model=list[schemas_todo.Todo])
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

@router.post("/todos", response_model=schemas_todo.Todo)
def create_todo(*, todo_in: schemas_todo.TodoCreate):  # 2
    """
    Create a new todo (in memory only)
    """
    new_entry_id = len(TODOS) + 1
    todo_entry = schemas_todo.Todo(
        id=new_entry_id,
        content=todo_in.content,
        is_done=todo_in.is_done
    )
    TODOS.append(todo_entry.dict())  # 3

    return todo_entry

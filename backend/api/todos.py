from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api import deps
from crud import crud_todo
from schemas import todo as schemas_todo

router = APIRouter()

@router.get("/todos", response_model=list[schemas_todo.Todo])
def get_all_todos(
    db: Session = Depends(deps.get_db)
):
    todos = crud_todo.get_all(db=db)
    return todos

@router.get("/todos/{todo_id}", response_model=schemas_todo.Todo)
def get_todo_by_id( 
    todo_id: int,
    db: Session = Depends(deps.get_db)
):
    todo = crud_todo.get_by_id(db=db, id=todo_id)
    return todo
    
@router.post("/todos", response_model=schemas_todo.Todo)
def create_todo(
    todo_parmas: schemas_todo.TodoCreate,
    db: Session = Depends(deps.get_db)
): 
    todo = crud_todo.create(db=db, todo_params=todo_parmas)
    return todo

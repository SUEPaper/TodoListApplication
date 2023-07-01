from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from crud import crud_todo
from schemas import todo as schemas_todo

router = APIRouter()

@router.get("/todos", response_model=list[schemas_todo.TodoInDB])
def get_all_todos(
    db: Session = Depends(deps.get_db)
):
    todos = crud_todo.get_all(db=db)
    return todos

@router.get("/todos/{todo_id}", response_model=schemas_todo.TodoInDB)
def get_todo_by_id( 
    todo_id: int,
    db: Session = Depends(deps.get_db)
):
    todo = crud_todo.get_by_id(db=db, id=todo_id)
    return todo
    
@router.post("/todos", response_model=schemas_todo.TodoInDB)
def create_todo(
    todo_parmas: schemas_todo.TodoCreate,
    db: Session = Depends(deps.get_db)
): 
    todo = crud_todo.create(db=db, todo_params=todo_parmas)
    return todo

@router.put("/todos/{todo_id}", response_model=schemas_todo.TodoInDB)
def update_todo(
    todo_id: int,
    todo_params: schemas_todo.TodoCreate,
    db: Session = Depends(deps.get_db)
):
    todo = crud_todo.get_by_id(db=db, id=todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo = crud_todo.update(db=db, id=todo_id, todo_params=todo_params)
    return todo


@router.delete("/todos/{todo_id}", response_model=schemas_todo.TodoInDB)
def delete_todo(
    todo_id: int,
    db: Session = Depends(deps.get_db)
):

    todo = crud_todo.get_by_id(db=db, id=todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo = crud_todo.remove(db=db, id=todo_id)

    return todo

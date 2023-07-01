from fastapi import APIRouter
from api.todos import router as todos_router

api_router = APIRouter()
api_router.include_router(todos_router, tags=["todos"])

@api_router.get("/")
def hello_world():
    return {"message": "Hello world"}

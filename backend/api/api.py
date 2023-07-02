from fastapi import APIRouter
from api.todos import router as todos_router
from api.users import router as users_router
from api.auth import router as auth_router

api_router = APIRouter()
api_router.include_router(todos_router, tags=["todos"])
api_router.include_router(users_router, tags=["users"])
api_router.include_router(auth_router, tags=["auth"])

@api_router.get("/")
def hello_world():
    return {"message": "Hello world"}

from fastapi import FastAPI

from src.routers import user_router, profile_router

app = FastAPI()

app.include_router(user_router)
app.include_router(profile_router)
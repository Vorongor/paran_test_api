from fastapi import FastAPI

from src.routers import api_v1_router

app = FastAPI()

app.include_router(api_v1_router)

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.exceptions import UserBaseException
from src.routers import api_v1_router

app = FastAPI()

app.include_router(api_v1_router)


@app.exception_handler(UserBaseException)
async def user_base_exception_handler(request: Request, exc: UserBaseException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=str(exc),
    )

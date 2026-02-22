from fastapi import FastAPI

from pdf_service.router import pdf_router

app = FastAPI(title="PDF Generation Service")

app.include_router(pdf_router)
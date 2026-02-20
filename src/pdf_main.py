from fastapi import FastAPI

from src.crud import prepare_profile_pdf_response
from src.schemas import UserReadSchema

app = FastAPI(title="PDF Generation Service")

@app.post("/generate")
async def generate_pdf(user: UserReadSchema):
    pdf_buffer = prepare_profile_pdf_response(user)
    return pdf_buffer

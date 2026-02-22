from fastapi import APIRouter

from pdf_service.crud import prepare_profile_pdf_response
from pdf_service.schemas import UserReadSchema

pdf_router = APIRouter()


@pdf_router.post("/pdf/generate")
async def generate_pdf(
        user: UserReadSchema,
):
    pdf_buffer = prepare_profile_pdf_response(user)
    return pdf_buffer

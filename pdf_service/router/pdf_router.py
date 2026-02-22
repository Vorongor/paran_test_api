import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from pdf_service.config.dependencies import get_sqs_manager
from pdf_service.crud import (
    prepare_profile_pdf_response,
    generate_profile_pdf_in_storage
)
from pdf_service.schemas import UserReadSchema
from pdf_service.storage.sqs import SQSClient

pdf_router = APIRouter()


@pdf_router.post("/pdf/generate")
async def generate_pdf(
        user: UserReadSchema,
):
    pdf_buffer = prepare_profile_pdf_response(user)
    return pdf_buffer


@pdf_router.post("/pdf/generate-in-storage")
async def start_pdf_generation(
        user_data: UserReadSchema,
        sqs_manager: Annotated[SQSClient, Depends(get_sqs_manager)]
):
    return await generate_profile_pdf_in_storage(
        user_data=user_data,
        sqs_manager=sqs_manager,

    )
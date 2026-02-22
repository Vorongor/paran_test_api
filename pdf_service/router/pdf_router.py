from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from pdf_service.config import PDFSettings
from pdf_service.config.dependencies import (
    get_sqs_manager,
    get_s3_manager,
    get_settings
)
from pdf_service.crud import (
    prepare_profile_pdf_response,
    generate_profile_pdf_in_storage,
    retrieve_profile_pdf
)
from pdf_service.schemas import UserReadSchema
from pdf_service.security.utils import get_current_user
from pdf_service.storage.s3 import S3StorageClient
from pdf_service.storage.sqs import SQSClient

pdf_router = APIRouter()


@pdf_router.post("/pdf/generate")
async def generate_pdf(
        user: UserReadSchema,
        auth_user: Annotated[None, Depends(get_current_user)]  # noqa
):
    try:
        pdf_buffer = prepare_profile_pdf_response(user)
        return pdf_buffer
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@pdf_router.post("/pdf/generate-in-storage")
async def start_pdf_generation(
        user_data: UserReadSchema,
        sqs_manager: Annotated[SQSClient, Depends(get_sqs_manager)],
        auth_user: Annotated[None, Depends(get_current_user)]  # noqa
):
    try:
        return await generate_profile_pdf_in_storage(
            user_data=user_data,
            sqs_manager=sqs_manager,
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@pdf_router.get("/pdf/{file_name}")
async def get_profile_pdf(
        file_name: str,
        settings: Annotated[PDFSettings, Depends(get_settings)],
        s3_manager: Annotated[S3StorageClient, Depends(get_s3_manager)],
        auth_user: Annotated[None, Depends(get_current_user)]  # noqa
):
    try:
        return await retrieve_profile_pdf(
            file_id=file_name,
            settings=settings,
            s3_manager=s3_manager,
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

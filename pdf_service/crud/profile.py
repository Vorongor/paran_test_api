from typing import Annotated

from fastapi import Response, Depends, status
from fastapi.responses import JSONResponse

from pdf_service.config import PDFSettings
from pdf_service.config.dependencies import get_sqs_manager, get_s3_manager, \
    get_settings
from pdf_service.schemas import UserReadSchema
from pdf_service.services import generate_user_pdf
from pdf_service.storage.s3 import S3StorageClient
from pdf_service.storage.sqs import SQSClient


def prepare_profile_pdf_response(user: UserReadSchema) -> Response:
    """
    Core logic to generate a PDF file from user data and wrap it in a Response.
    Args:
        :param user: (UserReadSchema): The authenticated user data.
    Returns:
        Response: FastAPI response object with PDF binary content and headers.
    """
    pdf_buffer = generate_user_pdf(user)

    filename = f"profile_{user.id}.pdf"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}

    return Response(
        content=pdf_buffer.getvalue(),
        media_type="application/pdf",
        headers=headers,
    )


async def generate_profile_pdf_in_storage(
        user_data: UserReadSchema,
        sqs_manager: Annotated[SQSClient, Depends(get_sqs_manager)],
) -> Response:
    """
    Function to generate a PDF file from user data and throw it into
    SQS queue to save pdf in storage in background.
    Args:
        :param user_data: The authenticated user data.
        :param sqs_manager: SQS manager object.
        :param s3_manager: S3 storage manager object.
    Returns:
        Response: FastAPI response object with PDF link in storage.
    """
    full_name = f"{user_data.name}_{user_data.surname}_{user_data.id}"
    file_name = f"profile_{full_name}"

    payload = {
        "job_id": file_name,
        "user_data": user_data.model_dump()
    }
    await sqs_manager.send_message(payload)
    file_url = f"http://127.0.0.1:8001/pdf/{file_name}.pdf"

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={
            "message": "PDF generation started for "
                       f"{user_data.name} {user_data.surname}",
            "job_id": file_name,
            "link": file_url
        }
    )


async def retrieve_profile_pdf(
        file_id: str,
        settings: Annotated[PDFSettings, Depends(get_settings)],
        s3_manager: Annotated[S3StorageClient, Depends(get_s3_manager)]
):
    async with s3_manager.session.client(
            "s3", endpoint_url=settings.AWS_ENDPOINT_URL,
    ) as client:
        response = await client.get_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=file_id
        )
        content = await response['Body'].read()
        return Response(
            content=content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={file_id}"
            }
        )

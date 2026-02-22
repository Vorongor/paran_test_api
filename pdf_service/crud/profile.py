import uuid
from typing import Annotated

from fastapi import Response, Depends

from pdf_service.config.dependencies import get_sqs_manager
from pdf_service.schemas import UserReadSchema
from pdf_service.services import generate_user_pdf
from pdf_service.storage.sqs import SQSClient


def prepare_profile_pdf_response(user: UserReadSchema) -> Response:
    """
    Core logic to generate a PDF file from user data and wrap it in a Response.

    Args:
        user (UserReadSchema): The authenticated user data.

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
        sqs_manager: Annotated[SQSClient, Depends(get_sqs_manager)]
) -> dict:
    job_id = f"job_{uuid.uuid4()}"
    payload = {
        "job_id": job_id,
        "user_data": user_data.model_dump()
    }

    await sqs_manager.send_message(payload)

    return {"status": "accepted", "job_id": job_id}
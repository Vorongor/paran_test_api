from fastapi import Response

from pdf_service.schemas import UserReadSchema
from pdf_service.services import generate_user_pdf


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

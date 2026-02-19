from typing import Annotated

from fastapi import Depends

from src.schemas import UserReadSchema
from src.security.utils import get_current_user
from src.services import generate_user_pdf


async def retrieve_user(
        auth_user: Annotated[UserReadSchema, Depends(get_current_user)]
) -> UserReadSchema:
    pdf_file = generate_user_pdf(auth_user)

    # 2. Повертаємо файл як відповідь
    headers = {
        'Content-Disposition': f'attachment; filename="profile_{auth_user.id}.pdf"'
    }

    return Response(
        content=pdf_file.getvalue(),
        media_type="application/pdf",
        headers=headers
    )
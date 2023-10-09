from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject

UNPROCESSABLE_ENTITY_MESSAGE = 'Проект с именем {} уже существует!'


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        room_name,
        session
    )
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=UNPROCESSABLE_ENTITY_MESSAGE.format(room_name)
        )

from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models import CharityProject
from app.schemas.charityproject import CharityProjectUpdate

UNPROCESSABLE_ENTITY_MESSAGE = 'Проект с именем {} уже существует!'
PROJECT_NOT_FOUND_MESSAGE = 'Проект с таким именем уже существует!'
PROJECT_CANT_BE_MODIFIED = ('Проект закрыт, поэтому не может быть изменен или'
                            ' удален!')
FULL_AMOUNT_UPDATE_ERROR = ('Новая требуемая сумма не должна быть меньше'
                            ' предыдущей.')


async def check_name_duplicate(
        room_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        room_name,
        session,
    )
    if project_id:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=UNPROCESSABLE_ENTITY_MESSAGE.format(room_name),
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND_MESSAGE,
        )
    return project


async def check_can_project_be_modified(
        *,
        project: CharityProject,
        object_in: CharityProjectUpdate = None,
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=PROJECT_CANT_BE_MODIFIED
        )
    if object_in:
        update_full_amount = object_in.dict().get('full_amount')
        if update_full_amount and project.full_amount >= update_full_amount:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail=FULL_AMOUNT_UPDATE_ERROR
            )

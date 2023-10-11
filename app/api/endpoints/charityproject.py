from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_can_project_be_modified, check_name_duplicate, check_project_exists
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.schemas.charityproject import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services import investing

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров. \n Создает благотворительный проект."""
    await check_name_duplicate(charity_project.name, session)
    try:
        new_charity_project = await charity_project_crud.create(
            charity_project,
            session
        )
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=str(error)
        )
    return await investing(new_charity_project, session)


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)

@router.patch(
    '/project_id',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        object_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    print('Начинаем обновлять проект')
    project = await check_project_exists(project_id, session)
    print('Полуили проект по id')
    if object_in:
        await check_can_project_be_modified(
            project=project,
            object_in=object_in
        )
        await check_name_duplicate(object_in.dict().get('name'), session) # TODO Проверить ситуацию, если имени не будет
    print('Сделали валидацию данных')
    project = await charity_project_crud.update(project, object_in, session)
    return project


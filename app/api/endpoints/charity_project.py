from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_can_project_be_modified, check_name_duplicate, check_project_exists,
    check_project_investing
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectDB, CharityProjectUpdate
)
from app.services import investing

CHARITY_PROJECT_PATH = '/'
CHARITY_PROJECT_MODIFY_PATH = CHARITY_PROJECT_PATH + '{project_id}'

router = APIRouter()


@router.post(
    CHARITY_PROJECT_PATH,
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Создаёт благотворительный проект."""
    await check_name_duplicate(charity_project.name, session)
    project = await charity_project_crud.create(
        charity_project,
        session,
        False,
    )
    session.add_all(
        investing(
            project,
            await donation_crud.get_open_objects(session)
        )
    )
    await session.commit()
    await session.refresh(project)
    return project


@router.get(
    CHARITY_PROJECT_PATH,
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.patch(
    CHARITY_PROJECT_MODIFY_PATH,
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        object_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров.
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной."""
    project = await check_project_exists(project_id, session)
    if object_in.name is not None:
        await check_name_duplicate(object_in.name, session)
    check_can_project_be_modified(
        project=project,
        object_in=object_in
    )
    project = await charity_project_crud.update(project, object_in, session)
    return project


@router.delete(
    CHARITY_PROJECT_MODIFY_PATH,
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    check_project_investing(project)
    return await charity_project_crud.remove(project, session)

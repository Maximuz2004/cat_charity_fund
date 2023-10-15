from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User

from app.schemas.donation import DonationCreate, DonationDB, DonationGet
from app.services import investing

DONATION_PATH = '/'
DONATION_MY_PATH = DONATION_PATH + 'my'

router = APIRouter()


@router.post(
    DONATION_PATH,
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Сделать пожертвование"""
    donation = await donation_crud.create(donation, session, user)
    session.add_all(
        investing(
            donation,
            await charity_project_crud.get_open_objects(session)
        )
    )
    await session.commit()
    await session.refresh(donation)
    return donation


@router.get(
    DONATION_PATH,
    response_model=list[DonationGet],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.get(
    DONATION_MY_PATH,
    response_model=list[DonationDB],
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Получить список моих пожертвований."""
    return await donation_crud.get_donation_by_user(session, user)

from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_can_project_be_modified, check_name_duplicate, check_project_exists,
    check_project_investing
)
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User

from app.schemas.donation import DonationCreate, DonationDB
from app.services import investing

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Сделать пожертвование"""
    try:
        new_donation = await donation_crud.create(donation, session, user)
    except ValueError as error:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=str(error)
        )
    return await investing(new_donation, session)

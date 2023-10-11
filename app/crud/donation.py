from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    pass


donation_crud = CRUDDonation(Donation)

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.constants import FULL_AMOUNT_MIN_VALUE
from app.core.db import Base


class CharityProjectDonationAbstractBase(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(
        Integer, nullable=False,
        default=FULL_AMOUNT_MIN_VALUE
    )
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

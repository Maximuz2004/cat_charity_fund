from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.constants import FULL_AMOUNT_MIN_VALUE
from app.core.db import Base


class CharityProjectDonationAbstractBase(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint(
            f'full_amount >= invested_amount >= {FULL_AMOUNT_MIN_VALUE}'
        ),
    )
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(
        Integer, nullable=False,
        default=FULL_AMOUNT_MIN_VALUE
    )
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return f'{self.invested_amount=} {self.full_amount=}'

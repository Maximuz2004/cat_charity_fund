from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]
    create_date: datetime


class DonationCreate(DonationBase):
    id: int

    class Config:
        orm_mode = True


class DonationDB(DonationCreate):
    id: int
    user_id: int
    invested_amount: int = Field(0)
    fully_invested: bool
    close_date: Optional[datetime]

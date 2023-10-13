from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationCreate):
    id: int = Field(...)
    user_id: int = Field(...)
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime = Field(...)
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
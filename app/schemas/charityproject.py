from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

NAME_ERROR_MESSAGE = 'Поле с именем не может быть пустым!'
DESCRIPTION_ERROR_MESSAGE = 'Поле с описанием не может быть пустым!'
FULL_AMOUNT_ERROR = 'Поле с требуемой суммой не может быть пустым!'
FULL_AMOUNT_LESS_INVESTED_AMOUNT_ERROR = ('Сумма не может быть меньше уже '
                                          'вложенной!')
CLOSED_PROJECT_ERROR = 'Закрытый проект нельзя обновить!'


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: str                # =  Field(..., )
    full_amount: PositiveInt

    class Config:
        min_anystr_length = 1
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, )
    full_amount: Optional[PositiveInt]

    @validator('name')
    def name_cant_be_empty(cls, value):
        if value is None:
            raise ValueError(NAME_ERROR_MESSAGE)
        return value

    @validator('description')
    def description_cant_be_empty(cls, value):
        if value is None:
            raise ValueError(DESCRIPTION_ERROR_MESSAGE)
        return value

    @validator('full_amount')
    def validate_full_amount(cls, value, values):
        if value is None:
            raise ValueError(FULL_AMOUNT_ERROR)
        if (
            'invested_amount' in values
            and values['invested_amount'] is not None
            and value < values['invested_amount']
        ):
            raise ValueError(FULL_AMOUNT_LESS_INVESTED_AMOUNT_ERROR)
        return value

    @validator('close_date', check_fields=False)
    def validate_open_project(cls, value):
        if value is not None:
            raise ValueError(CLOSED_PROJECT_ERROR)
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int                # = Field(0)
    fully_invested: bool                # = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True

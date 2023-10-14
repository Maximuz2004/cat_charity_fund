from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.core.constants import (
    CLOSE_DATE_FIELD_NAME, DESCRIPTION_FIELD_NAME, FIELD_MAX_LENGTH,
    FIELD_MIN_LENGTH, FULL_AMOUNT_FIELD_NAME, INVESTED_AMOUNT_FIELD_NAME,
    NAME_FIELD_NAME
)

NAME_ERROR_MESSAGE = 'Поле с именем не может быть пустым!'
DESCRIPTION_ERROR_MESSAGE = 'Поле с описанием не может быть пустым!'
FULL_AMOUNT_ERROR = 'Поле с требуемой суммой не может быть пустым!'
FULL_AMOUNT_LESS_INVESTED_AMOUNT_ERROR = ('Сумма не может быть меньше уже '
                                          'вложенной!')
CLOSED_PROJECT_ERROR = 'Закрытый проект нельзя обновить!'


class CharityProjectBase(BaseModel):
    name: str = Field(..., max_length=FIELD_MAX_LENGTH)
    description: str
    full_amount: PositiveInt

    class Config:
        min_anystr_length = FIELD_MIN_LENGTH
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, max_length=FIELD_MAX_LENGTH)
    description: Optional[str] = Field(None, )
    full_amount: Optional[PositiveInt]

    @validator(NAME_FIELD_NAME)
    def name_cant_be_empty(cls, value):
        if value is None:
            raise ValueError(NAME_ERROR_MESSAGE)
        return value

    @validator(DESCRIPTION_FIELD_NAME)
    def description_cant_be_empty(cls, value):
        if value is None:
            raise ValueError(DESCRIPTION_ERROR_MESSAGE)
        return value

    @validator(FULL_AMOUNT_FIELD_NAME)
    def validate_full_amount(cls, value, values):
        if value is None:
            raise ValueError(FULL_AMOUNT_ERROR)
        if (
            INVESTED_AMOUNT_FIELD_NAME in values
            and values[INVESTED_AMOUNT_FIELD_NAME] is not None
            and value < values[INVESTED_AMOUNT_FIELD_NAME]
        ):
            raise ValueError(FULL_AMOUNT_LESS_INVESTED_AMOUNT_ERROR)
        return value

    @validator(CLOSE_DATE_FIELD_NAME, check_fields=False)
    def validate_open_project(cls, value):
        if value is not None:
            raise ValueError(CLOSED_PROJECT_ERROR)
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True

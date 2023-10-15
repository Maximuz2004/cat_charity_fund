from sqlalchemy import Column, String, Text
from sqlalchemy.orm import validates

from .abstract import CharityProjectDonationAbstractBase
from app.core.constants import (
    DESCRIPTION_FIELD_NAME, FIELD_MAX_LENGTH, FIELD_MIN_LENGTH,
    NAME_FIELD_NAME
)

VALUE_ERROR_MESSAGE = 'Поле {} не может быть пустым'
FULL_AMOUNT_ERROR_MESSAGE = 'Поле {} не может быть меньше нуля'


class CharityProject(CharityProjectDonationAbstractBase):
    name = Column(String(FIELD_MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    @validates(NAME_FIELD_NAME, DESCRIPTION_FIELD_NAME)
    def value_cant_be_empty(self, key, value):
        if len(value.strip()) < FIELD_MIN_LENGTH:
            raise ValueError(VALUE_ERROR_MESSAGE.format(key))
        return value

    def __repr__(self):
        return f'Проект: "{self.name}", {super().__repr__()})'

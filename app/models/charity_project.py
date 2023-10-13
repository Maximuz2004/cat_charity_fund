from sqlalchemy import Column, String, Text
from sqlalchemy.orm import validates

from .abstract import CharityProjectDonationAbstractBase

VALUE_ERROR_MESSAGE = 'Поле {} не может быть пустым'
FULL_AMOUNT_ERROR_MESSAGE = 'Поле {} не может быть меньше нуля'


class CharityProject(CharityProjectDonationAbstractBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    @validates('name', 'description')
    def value_cant_be_empty(self, key, value):
        if len(value.strip()) == 0:
            raise ValueError(VALUE_ERROR_MESSAGE.format(key))
        return value

    @validates('full_amount')
    def validate_full_amount(self, key, value):
        if value <= 0:
            raise ValueError(FULL_AMOUNT_ERROR_MESSAGE.format(key))
        return value

    def __repr__(self):
        return f'Проект: "{self.name}", на сумму: {self.full_amount}'

from sqlalchemy import Column, ForeignKey, Integer, Text

from .abstract import CharityProjectDonationAbstractBase


class Donation(CharityProjectDonationAbstractBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return f'Пожертвование. {super().__repr__()}'

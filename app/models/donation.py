from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import CharityProjectDonationAbstractBase


class Donation(CharityProjectDonationAbstractBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return f'Пожертвование на сумму {self.full_amount}'
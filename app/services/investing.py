from datetime import datetime
from typing import Optional

from app.models.abstract import CharityProjectDonationAbstractBase


def investing(
        target: CharityProjectDonationAbstractBase,
        sources: list[CharityProjectDonationAbstractBase]
) -> list[Optional[CharityProjectDonationAbstractBase]]:
    def update_object(
            obj: CharityProjectDonationAbstractBase,
            value: int
    ) -> None:
        obj.invested_amount = (obj.invested_amount or 0) + value
        if obj.full_amount == obj.invested_amount:
            obj.fully_invested = True
            obj.close_date = datetime.now()

    updated_objects = []
    for source in sources:
        value_to_invest = min(
            source.full_amount - (source.invested_amount or 0),
            target.full_amount - (target.invested_amount or 0)
        )
        update_object(target, value_to_invest)
        update_object(source, value_to_invest)
        updated_objects.append(source)
        if target.fully_invested:
            break
    return updated_objects

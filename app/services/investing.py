from datetime import datetime

from app.models.abstract import CharityProjectDonationAbstractBase


def investing(
        target: CharityProjectDonationAbstractBase,
        sources: list[CharityProjectDonationAbstractBase]
) -> list[CharityProjectDonationAbstractBase]:
    updated = []
    for source in sources:
        value_to_invest = min(
            source.full_amount - (source.invested_amount or 0),
            target.full_amount - (target.invested_amount or 0)
        )
        for obj in (target, source):
            obj.invested_amount = (obj.invested_amount or 0) + value_to_invest
            if obj.full_amount == obj.invested_amount:
                obj.fully_invested = True
                obj.close_date = datetime.now()
        updated.append(source)
        if target.fully_invested:
            break
    return updated

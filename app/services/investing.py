from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject


async def investing(
        investment_object: CharityProject,
        # TODO Потом добавить модель Donation через Union
        session: AsyncSession,
) -> CharityProject:  # TODO Потом добавить модель Donation через Union
    print('Пытаюсь инвестировать ...')

    # await session.commit()        # TODO раскоментировать как все будет готово
    # await session.refresh(investment_object) # TODO раскоментировать как все будет готово
    return object

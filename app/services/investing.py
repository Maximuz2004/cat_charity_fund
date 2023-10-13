from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def close_object(obj: Union[CharityProject, Donation]) -> None:
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()


async def investing(session: AsyncSession) -> None:
    query = await session.execute(
        select(
            CharityProject
        ).where(
            ~CharityProject.fully_invested
        ).order_by(
            CharityProject.create_date
        )
    )
    projects = query.scalars().all()
    if not projects:
        return
    query = await session.execute(
        select(Donation).where(~Donation.fully_invested)
    )
    donations = query.scalars().all()
    if not donations:
        return
    for project in projects:
        for donation in donations:
            need_to_invest = project.full_amount - project.invested_amount
            can_invest = donation.full_amount - donation.invested_amount
            if need_to_invest > can_invest:
                project.invested_amount += can_invest
                await close_object(donation)
            elif need_to_invest < can_invest:
                donation.invested_amount += need_to_invest
                await close_object(project)
            elif need_to_invest == can_invest:
                await close_object(project)
                await close_object(donation)
            session.add(project)
            session.add(donation)
    await session.commit()

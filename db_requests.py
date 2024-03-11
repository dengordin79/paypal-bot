""" Формируем запросы к базе данных получая переменные для запросов от бота
"""
from models import User, async_session
from sqlalchemy import insert, select
from datetime import datetime


async def create_user(telegram_id : int):
    async with async_session() as session:
        users = await session.scalars(select(User).where(User.telegram_id == telegram_id))
        if len(users.all()) > 0:
            return False
        await session.execute(insert(User).values(telegram_id = telegram_id))
        await session.commit()
        return True
    
    
async def check_subscribe(telegram_id : int):
    async with async_session() as session:
        data = await session.scalars(select(User).where(User.telegram_id == telegram_id))
        user = data.one_or_none()
        if user:
            today = datetime.today()
            if user.ending_date:
                if user.ending_date >= today:
                    return True
        return False
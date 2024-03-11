""" Описание данных и формирование базы - Модели
    """
    
    

import asyncio, sys, logging
from datetime import datetime


from sqlalchemy import BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.sql.schema import ForeignKey

engine=create_async_engine('sqlite+aiosqlite:///db.sqlite', echo=True)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    telegram_id: Mapped[str] = mapped_column(primary_key=True)
    payer_id : Mapped[str] = mapped_column(default=None, nullable=True)
    payment_date : Mapped[datetime] = mapped_column(default=None, nullable=True)
    ending_date : Mapped[datetime] = mapped_column(default=None, nullable=True)
    
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        print('Exit')
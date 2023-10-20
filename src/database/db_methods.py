import time

from misc import logger
from .models import User, async_session_maker, engine, Base, ExchangeHistory
from sqlalchemy import update, insert, select


@logger.catch
async def create_tables():
    """
    Создаёт таблицы при старте бота
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@logger.catch
async def add_user(tg_user_id: int, tg_name: str) -> None:
    """
    Добавляет пользователя в базу данных
    """
    async with async_session_maker() as session:
        if not (await session.get(User, tg_user_id)):
            session.add(User(
                tg_user_id=tg_user_id,
                tg_name=tg_name
            ))
            await session.commit()


@logger.catch
async def add_subscription(tg_user_id: int, time: int):
    """
    Добавляет информацию, о том, что пользователь подписался на уведомления
    """
    async with async_session_maker() as session:
        await session.execute(
            update(User).where(User.tg_user_id == tg_user_id).values(subscribe=time)  # NOQA
        )
        await session.commit()


@logger.catch
async def get_subscription_time(tg_user_id: int):
    """
    Получает с каким промежутком, отправлять ему уведомления о курсе доллара 0 - отказ от подписки
    """
    async with async_session_maker() as session:
        user = await session.get(User, tg_user_id)
        return user.subscribe


@logger.catch
async def remove_subscription(tg_user_id: int):
    """
    Удаляет подписку на курс доллара
    """
    async with async_session_maker() as session:
        await session.execute(
            update(User).where(User.tg_user_id == tg_user_id).values(subscribe=0)  # NOQA
        )
        await session.commit()


@logger.catch
async def add_exchange_request(tg_user_id: int, exchange: float) -> None:
    """
    Добавляет информацию о запросе курса
    """
    logger.info('Курс добавлен в базу')
    async with async_session_maker() as session:
        stmt = insert(ExchangeHistory).values(
            tg_user_id=tg_user_id,
            exchange=exchange,
            request_time=time.time()
        )
        await session.execute(stmt)
        await session.commit()
    await session.commit()


@logger.catch
async def get_user_ids():
    async with async_session_maker() as session:
        query = select(User.tg_user_id).where(User.subscribe > 0)
        result = await session.execute(query)
        return result.fetchall()

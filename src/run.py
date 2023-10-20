import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import database

from handlers import start, users, other
from misc import bot, logger


# Запуск бота
async def main():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router,
        users.router
    )
    await other.run_exchange_tasks()
    await database.get_exchange_history(351162658)
    await database.create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info('Бот запущен')
    asyncio.run(main())

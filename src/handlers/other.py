import datetime
import asyncio
import database
from misc import logger
import misc
from misc import bot
from pathlib import Path
from aiogram.types import FSInputFile


@logger.catch
async def send_exchange(tg_user_id: int):
    """
    Отправляет курс доллара в телеграм-бот юзеру.
    """
    exchange = await misc.get_dollar_exchange()
    await bot.send_message(
        chat_id=tg_user_id,
        text=f'Курс доллара на данный момент: {exchange} рублей'
    )
    await database.add_exchange_request(tg_user_id=tg_user_id, exchange=exchange)


async def run_exchange_tasks():
    """
    Запускает задачи по отправке курса доллара юзерам, нужно при ребуте сервера.
    """
    tg_ids = (await database.get_user_ids())
    if tg_ids is None:
        logger.info('Задачи по получению курса доллара запущены')
        return
    for tg_id in tg_ids:
        asyncio.create_task(infinite_send_exchange(tg_id[0]))
    logger.info('Задачи по получению курса доллара запущены')


@logger.catch
async def infinite_send_exchange(tg_user_id: int):
    """
    Запускает задачу по отправке курса раз в какое-то время
    """
    while True:
        time = await database.get_subscription_time(tg_user_id=tg_user_id)
        if time == 0:
            break
        await send_exchange(tg_user_id=tg_user_id)
        await asyncio.sleep(time)


# @logger.catch
async def send_exchange_history(tg_user_id: int):
    """
    Отправляет историю запросов курса доллара пользователю
    """
    history = await database.get_exchange_history(tg_user_id=tg_user_id)
    history_text = 'Время запроса курса доллара\tКурс доллара\n'
    for r in history:
        history_text += f'{datetime.datetime.fromtimestamp(r[0]).strftime("%Y-%m-%d %H:%M:%S")}\t{r[1]}\n'
    with open(f'exchange_history_files/{tg_user_id}_history.txt', 'w') as f:
        f.write(history_text)
    logger.info(Path(f'exchange_history_files/{tg_user_id}_history.txt'))
    document = FSInputFile(f'exchange_history_files/{tg_user_id}_history.txt', filename='history.txt')
    await bot.send_document(
        chat_id=tg_user_id,
        document=document,
        caption='История запросов курса доллара'
    )

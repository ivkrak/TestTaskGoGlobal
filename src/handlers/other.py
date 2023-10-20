import database
from misc import logger
import misc
from misc import bot

import asyncio


@logger.catch
async def send_exchange(tg_user_id: int):
    exchange = await misc.get_dollar_exchange()
    await bot.send_message(
        chat_id=tg_user_id,
        text=f'Курс доллара на данный момент: {exchange} рублей'
    )
    await database.add_exchange_request(tg_user_id=tg_user_id, exchange=exchange)


async def run_exchange_tasks():
    # logger.info(f'{(await database.get_user_ids())=}')
    for tg_id in (await database.get_user_ids()):
        asyncio.create_task(infinite_send_exchange(tg_id[0]))


@logger.catch
async def infinite_send_exchange(tg_user_id: int):
    while True:
        time = await database.get_subscription_time(tg_user_id=tg_user_id)
        if time == 0:
            break
        await send_exchange(tg_user_id=tg_user_id)
        await asyncio.sleep(time)

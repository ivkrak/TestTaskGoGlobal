import database
from misc import logger
import misc
from misc import bot


@logger.catch
async def send_exchange(tg_user_id: int):
    exchange = await misc.get_dollar_exchange()
    await bot.send_message(
        chat_id=tg_user_id,
        text=f'Курс доллара на данный момент: {exchange} рублей'
    )
    await database.add_exchange_request(tg_user_id=tg_user_id,  exchange=exchange)

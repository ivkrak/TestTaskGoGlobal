from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import database
import keyboards

from misc import logger

router = Router()


@router.message(Command('start'), F.text)
@logger.catch
async def start(message: Message):
    await message.answer(
        text='Привет, я бот, который поможет тебе узнать курс рубль/доллар',
        reply_markup=keyboards.menu_kb
    )
    await database.add_user(
        tg_user_id=message.from_user.id,
        tg_name=message.from_user.full_name
    )
    
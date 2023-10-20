from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database
import keyboards
from misc import logger
import misc
from . import other
from .other import send_exchange

router = Router()


@router.message(F.text == 'Получить курс 💵', F.chat.type == 'private')
@logger.catch
async def get_exchange(message: Message):
    logger.info(f'Пользователь {message.from_user.full_name} узнал курс доллара')
    await send_exchange(message.from_user.id)


class FsmGetExchange(StatesGroup):
    get_exchange = State()


@router.message(F.text == 'Подписаться на курс 💵', F.chat.type == 'private')
@logger.catch
async def sud_to_exchange(message: Message, state: FSMContext):
    logger.info(f'Пользователь {message.from_user.full_name} начал процесс подписки на курс доллара')
    await message.answer(
        text='Нужно выбрать, с какой периодичностью вы будете получать информацию о курсе доллара',
        reply_markup=keyboards.time_buttons
    )
    await state.set_state(FsmGetExchange.get_exchange)


@router.callback_query()
@logger.catch
async def get_sub_time(q_query: CallbackQuery, state: FSMContext):
    """
    Получает время между сообщениями на курс доллара
    """
    logger.info(f'Пользователь выбрал раз в {q_query.data}')
    await q_query.message.answer(
        text='Отлично, подписка на курс доллара оформлена'
    )

    await database.add_subscription(
        tg_user_id=q_query.from_user.id,
        pause_between_sending=misc.time_dict.get(q_query.data))
    await state.clear()
    await other.infinite_send_exchange(q_query.from_user.id)


@router.message(F.text == 'Отменить подписку 💵', F.chat.type == 'private')
@logger.catch
async def sud_to_exchange(message: Message):
    logger.info(f'Пользователь {message.from_user.full_name} отменил подписку на курс доллара')
    await message.answer(
        text='Подписка на курс доллара отменена'
    )
    await database.remove_subscription(tg_user_id=message.from_user.id)


@router.message(F.text == 'Получить историю запросов курса 💵', F.chat.type == 'private')
@logger.catch
async def get_exchange_history(message: Message):
    logger.info(f'Пользователь {message.from_user.full_name} узнал историю запросов курса доллара')
    await other.send_exchange_history(message.from_user.id)

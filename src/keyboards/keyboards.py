from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.types import KeyboardButton

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Получить курс 💵')],
        [KeyboardButton(text='Подписаться на курс 💵')],
        [KeyboardButton(text='Отменить подписку 💵')]
    ],
    resize_keyboard=True
)

time_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Раз в минуту', callback_data='1_min')],
        [InlineKeyboardButton(text='Раз в час', callback_data='1_hour')],
        [InlineKeyboardButton(text='Раз в 6 часов', callback_data='6_hours')],
        [InlineKeyboardButton(text='Раз в день', callback_data='1_day')]
    ],
)

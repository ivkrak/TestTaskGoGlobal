from loguru import logger
from aiogram import Bot
import os

logger.add(
    'logs/log.log',
    format='{time:HH:mm:ss} {level} {message}',
    level='DEBUG',
    rotation='50 MB'
)

bot = Bot(token=os.getenv('BOT_TOKEN'))

time_dict = {'1_min': 60,
             '1_hour': 3600,
             '6_hours': 21600,
             '1_day': 86400}

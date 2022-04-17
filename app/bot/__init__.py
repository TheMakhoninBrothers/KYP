import logging

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from bot.logger import logger
import configs
from bot import middlewares

bot = Bot(
    token=configs.TOKEN,
    parse_mode=ParseMode.HTML,
)

dp = Dispatcher(
    bot,
    storage=MemoryStorage(),
)

dp.middleware.setup(middlewares.UserAutoRegistration())
dp.middleware.setup(middlewares.MongoLoggingMiddleware(logger=logger))

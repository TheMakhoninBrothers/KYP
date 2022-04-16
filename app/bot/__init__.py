from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

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

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import configs
from bot import middlewares

bot = Bot(
    token=configs.TOKEN,
)

dp = Dispatcher(
    bot,
    storage=MemoryStorage(),
)

dp.middleware.setup(middlewares.UserAutoRegistration())

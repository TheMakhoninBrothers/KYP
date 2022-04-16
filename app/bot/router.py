from aiogram import Dispatcher

from bot.main_menu import add_handlers as main_handlers
from bot.record.handlers import add_handlers as record_handlers
from bot.records.handlers import add_handlers as records_handlers


def add_handlers(dp: Dispatcher):
    main_handlers(dp)
    record_handlers(dp)
    records_handlers(dp)

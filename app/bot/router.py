from aiogram import Dispatcher

from bot.record.handlers import add_handlers as record_handlers


def add_handlers(dp: Dispatcher):
    record_handlers(dp)

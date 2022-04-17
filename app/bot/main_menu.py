from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text, CommandStart, CommandHelp

from bot import messages


def add_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(cancel, Text('cancel'))
    dp.register_message_handler(start, CommandStart())
    dp.register_message_handler(help, CommandHelp())


async def cancel(callback: types.CallbackQuery):
    await callback.message.delete()


async def start(message: types.Message):
    await message.answer(
        text=messages.START,
    )


async def help(message: types.Message):
    await message.answer(
        text=messages.HELP,
    )

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


def add_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(cancel, Text('cancel'))


async def cancel(callback: types.CallbackQuery):
    await callback.message.delete()

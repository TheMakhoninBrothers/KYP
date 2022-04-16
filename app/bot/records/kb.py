import typing

from aiogram import types

from entities.record import Record


def choose_record(records: typing.List[Record]) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=5)
    for i, record in enumerate(records):
        kb.insert(types.InlineKeyboardButton(text=f'{i + 1}', callback_data=f'verify_delete_record:{record.id}'))
    return kb


def verify_delete_record(record_id: int) -> types.InlineKeyboardMarkup:
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.row(
        types.InlineKeyboardButton(text='Удалить 👍', callback_data=f'delete_record:{record_id}'),
        types.InlineKeyboardButton(text='Отменить ❌', callback_data=f'cancel'),
    )
    return kb

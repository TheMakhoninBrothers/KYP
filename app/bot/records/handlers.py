from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command, Text

import db.postgres as db
from resources.record_deleter.simple import RecordDeleter
from resources.record_repo.postgres import PostgresRecordRepo
from resources.tag_parser.ignore_sign import TagParserWithIgnoreSign
from resources.tag_repo.postgres import PostgresTagRepo
from resources.user_repo.postgres import PostgresTelegramUserRepo
from use_cases.delete_record.simple import DeleteRecord
from use_cases.find_record.simple import FindRecord
from use_cases.records_list_by_search_text_from_telegram.by_tags import RecordsListByTagsInSearchTextFromTelegram
from . import kb


def add_handlers(dp: Dispatcher):
    dp.register_message_handler(
        record_list, Command('list', ignore_caption=False), content_types=[types.ContentType.TEXT],
    )
    dp.register_message_handler(
        search_by_message
    )
    dp.register_callback_query_handler(
        verify_delete_record, Text(startswith='verify_delete_record'),
    )

    dp.register_callback_query_handler(
        delete_record, Text(startswith='delete_record'),
    )


async def record_list(message: types.Message):
    """Add new record"""
    async with db.session_factory() as session:
        user_repo = PostgresTelegramUserRepo(session=session)
        record_repo = PostgresRecordRepo(session=session)
        tag_repo = PostgresTagRepo(session=session)
        tag_parser = TagParserWithIgnoreSign()
        use_case = RecordsListByTagsInSearchTextFromTelegram(
            record_repo=record_repo,
            user_repo=user_repo,
            tag_repo=tag_repo,
            tag_parser=tag_parser,
        )
        records = await use_case.list(message.chat.id, message.text[4:], 0)
    if records:
        record_rows = '\n\n'.join(
            [
                f'{i + 1}. {" ".join([f"#{tag.name}" for tag in record.tags])}\n'
                f'{record.text}'
                for i, record in enumerate(records)
            ]
        )
        await message.answer(
            text=(
                '<b>🔎 Search</b>\n'
                f'{record_rows}'
            ),
            reply_markup=kb.choose_record(records),
        )
    else:
        await message.answer(
            text=(
                '<b>🔎 Search</b>\n'
                '<i>Упс, записи не найдены</i>'
            )
        )


async def search_by_message(message: types.Message):
    async with db.session_factory() as session:
        user_repo = PostgresTelegramUserRepo(session=session)
        record_repo = PostgresRecordRepo(session=session)
        tag_repo = PostgresTagRepo(session=session)
        tag_parser = TagParserWithIgnoreSign()
        use_case = RecordsListByTagsInSearchTextFromTelegram(
            record_repo=record_repo,
            user_repo=user_repo,
            tag_repo=tag_repo,
            tag_parser=tag_parser,
        )
        records = await use_case.list(message.chat.id, message.text, 0)
    if records:
        record_rows = '\n\n'.join(
            [
                f'{i + 1}. {" ".join([f"#{tag.name}" for tag in record.tags])}\n'
                f'{record.text}'
                for i, record in enumerate(records)
            ]
        )
        await message.answer(
            text=(
                '<b>🔎 Search</b>\n'
                f'{record_rows}'
            ),
            reply_markup=kb.choose_record(records)
        )
    else:
        await message.answer(
            text=(
                '<b>🔎 Search</b>\n'
                '<i>Упс, записи не найдены</i>'
            )
        )


async def verify_delete_record(callback: types.CallbackQuery):
    record_id = int(callback.data.split(':')[-1])
    async with db.session_factory() as session:
        record_repo = PostgresRecordRepo(session=session)
        use_case = FindRecord(record_repo=record_repo)
        record = await use_case.find(record_id)
    tags_row = ' '.join([f'#{tag.name}' for tag in record.tags])
    await callback.message.edit_text(
        text='<b>🗑️ Remover</b>\n'
             f'{tags_row}\n'
             f'{record.text}\n'
             '\n'
             '<i>Вы точно хотите удалить?</i>',
        reply_markup=kb.verify_delete_record(record_id),
    )


async def delete_record(callback: types.CallbackQuery):
    record_id = int(callback.data.split(':')[-1])
    async with db.session_factory() as session:
        record_deleter = RecordDeleter(session)
        use_case = DeleteRecord(record_deleter=record_deleter)
        await use_case.delete(record_id)

    await callback.message.edit_text(
        text='<b>🗑️ Remover</b>\n'
             '<i>Запись удалена</i>',
    )

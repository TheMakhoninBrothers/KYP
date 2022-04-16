from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

import db.postgres as db
from resources.record_repo.postgres import PostgresRecordRepo
from resources.tag_parser.from_telegram import TagParserFromTelegram
from resources.tag_repo.postgres import PostgresTagRepo
from resources.user_repo.postgres import PostgresTelegramUserRepo
from use_cases.add_record_in_user_storage_from_telegram.with_tags import AddRecordInUserStorageFromTelegramWithTags


def add_handlers(dp: Dispatcher):
    dp.register_message_handler(
        add_new_record, Command('add', ignore_caption=False), content_types=[types.ContentType.TEXT],
    )


async def add_new_record(message: types.Message):
    """Add new record"""
    async with db.session_factory() as session:
        # async with session.begin():
        user_repo = PostgresTelegramUserRepo(session=session)
        record_repo = PostgresRecordRepo(session=session)
        tag_repo = PostgresTagRepo(session=session)
        tag_parser = TagParserFromTelegram()
        use_case = AddRecordInUserStorageFromTelegramWithTags(
            record_repo=record_repo,
            user_repo=user_repo,
            tag_repo=tag_repo,
            tag_parser=tag_parser,
        )
        new_record = await use_case.add(message.chat.id, message.text[4:])  # TODO: посмотреть можно ли отразеть команду
    tags_row = ' '.join(f'#{tag.name}' for tag in new_record.tags)
    await message.answer(
        text=(
            '<b>📜 Storage</b>\n'
            'Вы успешно добавили запись\n'
            '\n'
            '<b>Теги</b>\n'
            f'{tags_row}\n'
            f'\n'
            '<b>Запись</b>\n'
            f'{new_record.text}'
        ),
    )

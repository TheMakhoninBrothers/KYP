from aiogram import Dispatcher, types

import configs
import interfaces.exc.entity as entity_exc
from bot.logger import logger


def add_handlers(dp: Dispatcher):
    dp.register_errors_handler(entity_not_exist, exception=entity_exc.EntityNotExist)
    dp.register_errors_handler(entity_already_exist, exception=entity_exc.EntityAlreadyExist)
    # dp.register_errors_handler(unexpected_error, exception=Exception)


async def entity_already_exist(update: types.Update, exc: entity_exc.EntityAlreadyExist):
    message = update.message or update.callback_query.message
    chat_id = message.chat.id
    await update.bot.send_message(
        chat_id=chat_id,
        text='<i>😿 Упс, сущность уже существует.</i>',
    )
    return True


async def entity_not_exist(update: types.Update, exc: entity_exc.EntityNotExist):
    message = update.message or update.callback_query.message
    chat_id = message.chat.id
    await update.bot.send_message(
        chat_id=chat_id,
        text='<i>😿 Упс, сущность не существует.</i>',
    )
    return True


async def unexpected_error(update: types.Update, exc: Exception):  # TODO: разобратсья с обработкой Exception
    message = update.message or update.callback_query.message
    chat_id = message.chat.id
    user = message.from_user.username or message.chat.id
    logger().error(f'User {user} . UNEXPECTED ERROR: {exc}')
    await update.bot.send_message(
        chat_id=chat_id,
        text='<i>😿 Упс, произошла непредвиденная ошибка в работе бота.</i>\n'
             f'Вы можете сообщить об ошибке в техническую поддержку (@{configs.SUPPORT_USERNAME}).'
    )

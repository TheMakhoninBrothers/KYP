from bot.logger import logger
from aiogram import types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
import logging
import db.postgres as db
from resources.auth_service.postgres import PostgresTelegramAuthService
from resources.user_repo.postgres import PostgresTelegramUserRepo
from use_cases.registrate_user_in_telegram.auto import AutoRegistrateUserInTelegram


class UserAutoRegistration(BaseMiddleware):

    async def on_pre_process_update(self, update: types.Update, _):
        if update.message:
            data_from_user = update.message.from_user
        elif update.callback_query:
            data_from_user = update.callback_query.from_user
        else:
            return

        async with db.session_factory() as session:
            async with session.begin():
                auth_service = PostgresTelegramAuthService(session)
                user_repo = PostgresTelegramUserRepo(session)
                use_case = AutoRegistrateUserInTelegram(auth_service=auth_service, user_repo=user_repo)
                await use_case.registrate(telegram_id=data_from_user.id, username=data_from_user.username)


class MongoLoggingMiddleware(LoggingMiddleware):

    def __init__(self, logger: logging.Logger):
        super(MongoLoggingMiddleware, self).__init__(logger)

    async def on_post_process_update(self, update: types.Update, result, data: dict):
        pass

    async def on_pre_process_message(self, message: types.Message, data: dict):
        if len(message.text) > 100:
            text = message.text[:100]
        else:
            text = message.text
        user = message.from_user.username or message.from_user.id
        self.logger.info(f'User {user} send message: {text}')

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        user = callback_query.from_user.username or callback_query.from_user.id
        self.logger.info(f'User {user} click callback {callback_query.data}.')

    async def on_post_process_callback_query(self, callback_query, results, data: dict):
        user = callback_query.from_user.username or callback_query.from_user.id
        self.logger.info(f'User {user} get success callback {callback_query.data}')

    async def on_pre_process_error(self, update, error, data: dict):
        timeout = self.check_timeout(update)
        if timeout > 0:
            if update.message:
                user = update.message.from_user.username or update.message.from_user.id
                self.logger.error(f'User {user} send message ERROR "{update.message.text}". ERROR: {error}')
            elif update.callback_query:
                user = update.callback_query.from_user.username or update.callback_query.from_user.id
                self.logger.error(f'User {user} callback {update.callback_query.data}. ERROR: {error}')

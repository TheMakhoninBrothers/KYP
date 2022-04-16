from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

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

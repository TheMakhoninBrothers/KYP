import typing

from entities.user import TelegramUser
from interfaces.resources.telegram_auth_service import TelegramAuthService
from interfaces.resources.telegram_user_repo import TelegramUserRepo
from interfaces.use_case.registrate_user_in_telegram import RegistrateUserInTelegram


class AutoRegistrateUserInTelegram(RegistrateUserInTelegram):
    """Use case for auto registration in telegram"""

    def __init__(self, auth_service: TelegramAuthService, user_repo: TelegramUserRepo):
        self.auth_service = auth_service
        self.user_repo = user_repo

    async def registrate(self, telegram_id: int, username: typing.Optional[str]) -> TelegramUser:
        auth_user = self.auth_service.auth(telegram_id)
        if auth_user:
            return auth_user
        return await self.user_repo.add(telegram_id, username)

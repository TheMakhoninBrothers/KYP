import typing

from entities.record import Record
from interfaces.resources.record_repo import RecordRepo
from interfaces.resources.tag_parser import TagParser
from interfaces.resources.tag_repo import TagRepo
from interfaces.resources.telegram_user_repo import TelegramUserRepo
from interfaces.use_case.list_records_by_search_text_from_telegram import RecordsListBySearchTextFromTelegram


class RecordsListByTagsInSearchTextFromTelegram(RecordsListBySearchTextFromTelegram):

    def __init__(
            self,
            record_repo: RecordRepo,
            tag_parser: TagParser,
            tag_repo: TagRepo,
            user_repo: TelegramUserRepo,
    ):
        self.record_repo = record_repo
        self.tag_parser = tag_parser
        self.tag_repo = tag_repo
        self.user_repo = user_repo

    async def list(self, telegram_id: int, search_text: str, page: int) -> typing.List[Record]:
        user = await self.user_repo.find(telegram_id)
        search_tags = self.tag_parser.parse(search_text)
        user_tags = await self.tag_repo.list(user.id)
        search_user_tags = [user_tag.id for user_tag in user_tags if user_tag.name in search_tags]
        return await self.record_repo.list(user.id, search_user_tags)

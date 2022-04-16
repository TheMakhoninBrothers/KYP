from entities.record import Record
from interfaces.resources.record_repo import RecordRepo
from interfaces.resources.tag_parser import TagParser
from interfaces.resources.tag_repo import TagRepo
from interfaces.resources.telegram_user_repo import TelegramUserRepo
from interfaces.use_case.add_record_in_user_storage_from_telegram import AddRecordInUserStorageFromTelegram


class AddRecordInUserStorageFromTelegramWithTags(AddRecordInUserStorageFromTelegram):

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

    async def add(self, telegram_id: int, text: str) -> Record:
        user = await self.user_repo.find(telegram_id)
        new_tags = self.tag_parser.parse(text)
        user_tags = await self.tag_repo.list(user.id)
        tag_names = [user_tag.name for user_tag in user_tags]
        tag_ids = []
        for new_tag in new_tags:
            if new_tag not in tag_names:
                new_tag = await self.tag_repo.add(user.id, new_tag)
                tag_ids.append(new_tag.id)
            else:
                tag_ids.append(user_tags[tag_names.index(new_tag)].id)
        return await self.record_repo.add(user.id, text, tag_ids)

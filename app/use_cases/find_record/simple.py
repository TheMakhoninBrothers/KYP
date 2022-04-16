from entities.record import Record
from interfaces.resources.record_repo import RecordRepo
from interfaces.use_case.find_record import FindRecord as Interface


class FindRecord(Interface):  # TODO: Продумать лучше класс

    def __init__(self, record_repo: RecordRepo):
        self.record_repo = record_repo

    async def find(self, record_id: int) -> Record:
        return await self.record_repo.find(record_id)

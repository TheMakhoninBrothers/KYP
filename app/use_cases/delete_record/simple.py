from interfaces.resources.record_deleter import RecordDeleter
from interfaces.use_case.delete_record import DeleteRecord as Interface


class DeleteRecord(Interface):

    def __init__(self, record_deleter: RecordDeleter):
        self.record_delete = record_deleter

    async def delete(self, record_id: int):
        await self.record_delete.delete(record_id)

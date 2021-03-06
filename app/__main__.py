from aiogram import executor

import db.postgres as db
from bot import dp, router


async def on_startup(_):
    async with db.async_engine.begin() as conn:
        await conn.run_sync(db.Base.metadata.create_all)


if __name__ == '__main__':
    router.add_handlers(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

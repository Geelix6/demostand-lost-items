import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import start, lost_item
from models.db import engine, Base
from models.item import Item 
from services.embeddings import get_embedding
from utils.config import settings


async def main():
    async with engine.begin() as conn:
      await conn.run_sync(Base.metadata.create_all)

    bot = Bot(token=settings.TG_BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.message.register(start.start_handler, Command(commands=["start"]))
    dp.message.register(start.help_handler, Command(commands=["help"]))
    dp.message.register(lost_item.cancel_handler, Command(commands=["cancel"]))

    dp.callback_query.register(start.find_callback, F.data == "find_item")
    dp.callback_query.register(start.find_callback, F.data == "retry_find")

    dp.message.register(lost_item.date_handler, lost_item.LostState.date)
    dp.message.register(lost_item.station_handler, lost_item.LostState.station)
    dp.message.register(lost_item.description_handler, lost_item.LostState.description)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

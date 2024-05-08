
from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram_dialog import setup_dialogs

from .dialogs.dialogs import dlg_router
from .settings.config import settings
from app.core.init_db import startup_db, shutdown_db
from app.handlers.router import main_router

storage = MemoryStorage()
dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())


async def init_bot() -> None:
    bot = Bot(settings.TOKEN, parse_mode=ParseMode.HTML)

    dp.startup.register(startup_db)
    dp.shutdown.register(shutdown_db)
    dp.include_routers(dlg_router)
    setup_dialogs(dp)

    await dp.start_polling(bot)

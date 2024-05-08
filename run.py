import asyncio
import logging
import sys

from app.main import init_bot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logging.getLogger("aiogram_dialog").setLevel(logging.DEBUG)
    asyncio.run(init_bot())

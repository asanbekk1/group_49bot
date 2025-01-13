from bot_config import bot,dp
from handlers import (myinfo,
                      random,
                      start)
import logging


async def main():
    dp.include_router(myinfo.myinfo_router)
    dp.include_router(random.random_router)
    dp.include_router(start.start_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

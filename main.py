import asyncio
from bot_config import bot,dp
from handlers import (myinfo,
                      random,
                      start,
                      review_dialog)
import logging


async def main():
    dp.include_router(myinfo.myinfo_router)
    dp.include_router(random.random_router)
    dp.include_router(start.start_router)
    dp.include_router(review_dialog.review_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
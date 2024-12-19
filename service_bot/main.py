import asyncio

from aiogram import Bot, Dispatcher
from logging import getLogger, basicConfig
from core.message_handler import scheduler

from tools import token_conf
from core.message_handler import router

basicConfig(level="INFO")
log = getLogger(__name__)

dp = Dispatcher()
bot = Bot(token=token_conf.token)


async def main():
    try:
        dp.include_router(router)
        await dp.start_polling(bot)
        scheduler.start()
        log.info("Бот работает без ошибок")
    except Exception as e:
        log.error(e)
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

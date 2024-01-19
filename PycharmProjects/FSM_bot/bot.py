import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers
from handlers import FSM_handler


async def main():
    config: Config = load_config()
    BOT_TOKEN: str = config.tg_bot.token

    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(FSM_handler.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.configs import settings

logger = logging.getLogger(__name__)

bot = Bot(
    token=settings.tg_bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
tg_dispatcher = Dispatcher(name="main_dispatcher")


async def start_bot():
    try:
        await bot.send_message(settings.tg_admin_id, "Бот запущен.")
    except Exception as e:
        logger.exception(e)


async def stop_bot():
    try:
        await bot.send_message(settings.tg_admin_id, "Бот остановлен.")
    except Exception as e:
        logger.exception(e)

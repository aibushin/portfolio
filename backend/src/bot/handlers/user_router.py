from datetime import datetime
import io
import logging
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import (
    as_section,
    Bold,
    as_list,
    as_key_value,
    HashTag,
    as_numbered_section,
    Text,
)
import orjson

from src.bot.keyboards.kbs import app_keyboard
from src.bot.utils.utils import get_about_us_text, greet_user
from aiogram.types import ContentType

from src.utils.tg_qr_handlers import handle_images, handle_pdf
from src.utils.utils import TaskStatus, handle_tasks
from aiogram_media_group import media_group_handler

logger = logging.getLogger(__name__)

tg_user_router = Router(name="user_router")


@tg_user_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Обрабатывает команду /start."""
    logger.debug("cmd_start")


@tg_user_router.message(F.text == "🔙 Назад")
async def cmd_back_home(message: Message) -> None:
    """Обрабатывает нажатие кнопки "Назад"."""
    await greet_user(message, is_new_user=False)


@tg_user_router.message(F.text == "ℹ️ О нас")
async def about_us(message: Message):
    kb = app_keyboard(user_id=message.from_user.id, first_name=message.from_user.first_name)
    await message.answer(get_about_us_text(), reply_markup=kb)


@tg_user_router.message(F.text == "test")
async def test_handler(message: Message):
    await message.answer("Ответ обработчика test_handler")
    return {"handler": "test_handler"}


@tg_user_router.message(F.content_type == ContentType.DOCUMENT)
async def doc_handler(message: Message):
    file_in_io = io.BytesIO()
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    await message.bot.download_file(file_path=file_path, destination=file_in_io)

    check = await handle_pdf(file_in_io)
    data = check[0]["data"]
    json = data["json"]
    user = json["user"]
    items_raw = json["items"]
    total_sum = f"{(int(json['totalSum']) / 100):,}"
    receive_date = json["metadata"]["receiveDate"]
    receive_date = datetime.strptime(receive_date, "%Y-%m-%dT%H:%M:%SZ")
    receive_date = receive_date.strftime("%d.%m.%Y %H:%M")

    items = [
        as_key_value(
            i["name"],
            f"{(int(i['price']) / 100):,}",
        )
        for i in items_raw
    ]

    reply = as_list(
        as_section(Bold(user), Bold(receive_date)),
        as_numbered_section(
            Bold(f"Сумма: {total_sum}"),
            *items,
        ),
        HashTag("#Чек"),
        sep="\n\n",
    )
    await message.reply(**reply.as_kwargs())

    # await message.reply(text=html, parse_mode=ParseMode.HTML)


def check_prepare_reply(check: list[dict]) -> Text:
    try:
        data = check["data"]
        data_json = orjson.dumps(data).decode("utf-8")  # noqa: F841
        json = data["json"]
        user = json["user"]
        items_raw = json["items"]
        total_sum = f"{(int(json['totalSum']) / 100):,}"
        receive_date = json["metadata"]["receiveDate"]
        receive_date = datetime.strptime(receive_date, "%Y-%m-%dT%H:%M:%SZ")
        receive_date = receive_date.strftime("%d.%m.%Y %H:%M")

        items = [
            as_key_value(
                i["name"],
                f"{(int(i['price']) / 100):,}",
            )
            for i in items_raw
        ]

        reply = as_list(
            as_section(Bold(user), Bold(receive_date)),
            as_numbered_section(
                Bold(f"Сумма: {total_sum}"),
                *items,
            ),
            HashTag("#Чек"),
            sep="\n\n",
        )
        return reply
    except (KeyError, IndexError) as e:
        logger.debug(f"check_prepare_reply exception: {e}")
        return as_list(as_section(Bold("Не удалось получить валидные данные из чека")))


@tg_user_router.message(F.media_group_id, F.content_type.in_({"photo"}))
@media_group_handler
async def album_handler(messages: list[Message]):
    message = messages[-1]

    await message.answer(message.content_type)
    file_in_io = await message.bot.download(file=message.photo[-1].file_id)

    tasks = await handle_images(file_in_io)

    results = handle_tasks(tasks)
    success_checks = results[TaskStatus.SUCCESS]
    for check in success_checks:
        reply = check_prepare_reply(success_checks[check])
        await message.reply(**reply.as_kwargs())


@tg_user_router.message(F.photo)
async def photo_handler(message: Message):
    await message.answer(message.content_type)
    file_in_io = await message.bot.download(file=message.photo[-1].file_id)

    tasks = await handle_images(file_in_io)

    results = handle_tasks(tasks)
    success_checks = results[TaskStatus.SUCCESS]
    for check in success_checks:
        reply = check_prepare_reply(success_checks[check])
        await message.reply(**reply.as_kwargs())

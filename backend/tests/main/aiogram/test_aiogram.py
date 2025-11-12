import logging
import pytest
from src.bot.handlers.user_router import cmd_start, photo_handler
from src.utils.utils import TaskStatus
from tests.mocks.ofd_responses import ASHAN

from unittest.mock import AsyncMock, patch, Mock, call
from aiogram.methods import GetFile
from aiogram.types import ContentType, PhotoSize, File

from tests.main.aiogram.mocked_bot import MockedBot
from aresponses import ResponsesMockServer
from aiogram.utils.formatting import Text
from aiogram.types import User

USER_ROUTER = "src.bot.handlers.user_router"


@pytest.fixture
def tg_user():
    return User(id=1, first_name="Name", username="username", is_bot=False)


class TestAiogram:
    @patch(f"{USER_ROUTER}.handle_images", new_callable=AsyncMock)
    @patch(f"{USER_ROUTER}.handle_tasks", new_callable=Mock)
    @patch(f"{USER_ROUTER}.check_prepare_reply", new_callable=Mock)
    async def test_photo_handler(
        self,
        mock_check_prepare_reply: Mock,
        mock_handle_tasks: Mock,
        mock_handle_images: AsyncMock,
        mocked_bot: MockedBot,
        faker,
        aresponses: ResponsesMockServer,
    ):
        mock_handle_tasks.return_value = {
            TaskStatus.SUCCESS: {ASHAN["request"]["qrraw"]: ASHAN},
            TaskStatus.FAIL: {},
            TaskStatus.CANSEL: [],
        }
        reply = Text("Ответ пользователю")
        mock_check_prepare_reply.return_value = reply

        file_id = "file id"
        file_unique_id = "file id"

        aresponses.add(
            method_pattern="get",
            response=aresponses.Response(status=200, body=faker.ofd_qr_image()),
        )

        mocked_bot.add_result_for(
            GetFile,
            ok=True,
            result=File(file_id=file_id, file_unique_id=file_unique_id),
        )

        content_type = ContentType.PHOTO
        photo = PhotoSize(
            file_id=file_id,
            file_unique_id=file_unique_id,
            width=123,
            height=123,
        )
        message_mock = AsyncMock(bot=mocked_bot, content_type=content_type, photo=[photo])

        await photo_handler(message=message_mock)

        mock_handle_images.assert_awaited_once()
        mock_handle_tasks.assert_called_once()
        mock_check_prepare_reply.assert_called_once()

        message_mock.answer.assert_called_with(content_type)
        message_mock.reply.assert_called_with(**reply.as_kwargs())

    @pytest.mark.skip("Переписать")
    @pytest.mark.parametrize(
        "find_one_or_none__return_value",
        (None, "existing user"),
        ids=("user exists", "user does not exist"),
    )
    @patch(f"{USER_ROUTER}.UserDAO.find_one_or_none", new_callable=AsyncMock)
    @patch(f"{USER_ROUTER}.UserDAO.add", new_callable=AsyncMock)
    @patch(f"{USER_ROUTER}.greet_user", new_callable=AsyncMock)
    async def test_cmd_start(
        self,
        mock_greet_user: AsyncMock,
        mock_add: AsyncMock,
        mock_find_one_or_none: AsyncMock,
        find_one_or_none__return_value,
        tg_user,
        caplog,
    ):
        caplog.set_level(logging.DEBUG)
        mock_find_one_or_none.return_value = find_one_or_none__return_value
        mock_message = AsyncMock(from_user=tg_user)

        await cmd_start(message=mock_message)

        if find_one_or_none__return_value:
            mock_add.assert_not_awaited()
        else:
            mock_add.assert_has_awaits(
                [
                    call(
                        telegram_id=tg_user.id,
                        first_name=tg_user.first_name,
                        username=tg_user.username,
                    )
                ],
                any_order=False,
            )
        # mock_add.assert_awaited_once_with(
        #     telegram_id=mock_message.from_user.id,
        #     first_name=mock_message.from_user.first_name,
        #     username=mock_message.from_user.username,
        # )
        mock_find_one_or_none.assert_awaited_once()
        mock_greet_user.assert_awaited_once()

        assert caplog.messages == ["cmd_start", f"user: {find_one_or_none__return_value}"]

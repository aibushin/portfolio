import datetime
import time
from typing import Any, Dict, Union
from unittest.mock import AsyncMock, patch

from aiogram import Dispatcher, Router
from aiogram.dispatcher.event.handler import CallableObject
from aiogram.types import Chat, Message, Update, User
from aiogram.dispatcher.middlewares.manager import MiddlewareManager
from aiogram.filters import Filter

from pydantic import BaseModel
import pytest


from tests.main.aiogram.mocked_bot import MockedBot

from aiogram.methods import SendMessage
from src.bot.handlers.user_router import tg_user_router


USER_ROUTER = "src.bot.handlers.user_router"


async def my_handler(event: Any, index: int = 0) -> Any:
    return event


class MyFilter1(Filter, BaseModel):
    test: str

    async def __call__(self, *args: Any, **kwargs: Any) -> Union[bool, Dict[str, Any]]:
        return True


# @pytest.mark.skip
class TestFastApi:
    def test__root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}

    def test__favicon(self, client):
        response = client.get("/favicon.ico")
        assert response.status_code == 200
        pass
        # assert response.json() == {"msg": "Hello World"}

    def test__sync__test_handler_sync(
        self,
        client,
        mocked_bot: MockedBot,
    ):
        request_data = {
            "update_id": 0,
            "message": {
                "message_id": 0,
                "from": {"id": 42, "first_name": "Test", "is_bot": False},
                "chat": {"id": 42, "is_bot": False, "type": "private"},
                "date": int(time.time()),
                "text": "test",
            },
        }

        mocked_bot.add_result_for(method=SendMessage, ok=True)

        with patch.multiple("src.app", bot=mocked_bot):
            response = client.post("/webhook", json=request_data)
        assert response.status_code == 200
        assert response.json() == {"handler": "test_handler"}

    async def test__async__test_handler(
        self,
        async_f_client,
        mocked_bot: MockedBot,
    ):
        request_data = {
            "update_id": 0,
            "message": {
                "message_id": 0,
                "from": {"id": 42, "first_name": "Test", "is_bot": False},
                "chat": {"id": 42, "is_bot": False, "type": "private"},
                "date": int(time.time()),
                "text": "test",
            },
        }

        mocked_bot.add_result_for(method=SendMessage, ok=True)

        with patch.multiple("src.app", bot=mocked_bot):
            response = await async_f_client.post("/webhook", json=request_data)
        assert response.status_code == 200
        assert response.json() == {"handler": "test_handler"}

    # @pytest.mark.skip
    @patch(f"{USER_ROUTER}.test_handler", new_callable=AsyncMock)
    async def test__async__test_handler_qwe(
        self,
        mock_test_handler: AsyncMock,
        async_f_client,
        mocked_bot: MockedBot,
        # dispatcher: Dispatcher,
    ):
        request_data = {
            "update_id": 0,
            "message": {
                "message_id": 0,
                "from": {"id": 42, "first_name": "Test", "is_bot": False},
                "chat": {"id": 42, "is_bot": False, "type": "private"},
                "date": int(time.time()),
                "text": "test",
            },
        }

        mocked_bot.add_result_for(method=SendMessage, ok=True)

        # with patch.multiple("src.app", bot=mocked_bot, dispatcher=dispatcher):
        with patch.multiple("src.app", bot=mocked_bot):
            response = await async_f_client.post("/webhook", json=request_data)
        assert response.status_code == 200
        assert response.json() == {"handler": "test_handler"}

        # user_router.obsevers.message.handlers
        mock_test_handler.assert_awaited_once()

    async def test__async__test_handler_asd(
        self,
        mocker,
        async_f_client,
        mocked_bot: MockedBot,
        # dispatcher: Dispatcher,
    ):
        # mock_test_handler = mocker.patch.object(CallableObject, "call", autospec=True)
        # mocker.patch.dict("src.app.tg_user_router.observers", 3.0)

        request_data = {
            "update_id": 0,
            "message": {
                "message_id": 0,
                "from": {"id": 42, "first_name": "Test", "is_bot": False},
                "chat": {"id": 42, "is_bot": False, "type": "private"},
                "date": int(time.time()),
                "text": "test",
            },
        }

        mocked_bot.add_result_for(method=SendMessage, ok=True)

        # with patch.multiple("src.app", bot=mocked_bot, dispatcher=dispatcher):
        with patch.multiple("src.app", bot=mocked_bot):
            response = await async_f_client.post("/webhook", json=request_data)
        assert response.status_code == 200
        assert response.json() == {"handler": "test_handler"}

        # user_router.obsevers.message.handlers
        # mock_test_handler.assert_awaited_once()

    @patch(f"{USER_ROUTER}.test_handler", new_callable=AsyncMock)
    async def test__observer(
        self,
        mock_test_handler: AsyncMock,
        mocker,
        mocked_bot: MockedBot,
    ):
        observer = tg_user_router.message
        # event = Message(
        event = Update(
            update_id=42,
            message=Message(
                text="test",
                message_id=42,
                chat=Chat(id=42, type="private"),
                date=datetime.datetime.now(),
            ),
        )
        # mocked_bot.add_result_for(method=SendMessage, ok=True)

        spy = mocker.spy(MiddlewareManager, "wrap_middlewares")
        await observer.trigger(event=event, bot=mocked_bot)
        # spy.assert_called_once_with("This is a test log.")
        spy.assert_awaited_with("test")
        mock_test_handler.assert_awaited_once()

    async def test_trigger(self):
        # observer = tg_user_router.message
        observer = Router().message
        observer.register(my_handler, MyFilter1(test="ok"))

        message = Message(
            message_id=42,
            date=datetime.datetime.now(),
            text="test",
            chat=Chat(id=42, type="private"),
            from_user=User(id=42, is_bot=False, first_name="Test"),
        )

        results = await observer.trigger(message)
        assert results is message

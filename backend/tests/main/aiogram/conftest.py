from aiogram import Dispatcher
import pytest

from aiogram.fsm.storage.memory import (
    DisabledEventIsolation,
    MemoryStorage,
    SimpleEventIsolation,
)
from tests.main.aiogram.mocked_bot import MockedBot


@pytest.fixture()
async def memory_storage():
    storage = MemoryStorage()
    try:
        yield storage
    finally:
        await storage.close()


@pytest.fixture()
async def lock_isolation():
    isolation = SimpleEventIsolation()
    try:
        yield isolation
    finally:
        await isolation.close()


@pytest.fixture()
async def disabled_isolation():
    isolation = DisabledEventIsolation()
    try:
        yield isolation
    finally:
        await isolation.close()


@pytest.fixture()
def mocked_bot():
    return MockedBot()


@pytest.fixture()
async def dispatcher():
    dp = Dispatcher(name="test_dispatcher")
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()

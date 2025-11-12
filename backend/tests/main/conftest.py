from contextlib import asynccontextmanager

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
import pytest
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
import pytest_asyncio

from src.configs import settings
from src.database import Base, sessionmanager

from src.app import app as actual_app, lifespan_shutdown, lifespan_startup
from asyncpg import Connection
from fastapi.testclient import TestClient
from sqlalchemy import text

from tests.main.factories import OFDItemFactory, OFDReceiptFactory
from asgi_lifespan import LifespanManager


@pytest_asyncio.fixture(scope="session")
async def async_f_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await lifespan_startup()
        yield
        await lifespan_shutdown()

    actual_app.router.lifespan_context = lifespan

    async with LifespanManager(actual_app) as manager:
        yield manager.app


@pytest_asyncio.fixture
async def async_f_client(async_f_app):
    async with AsyncClient(
        transport=ASGITransport(app=async_f_app), base_url="http://testserver"
    ) as client:
        yield client


@pytest.fixture
def client(async_f_app):
    return TestClient(app=async_f_app, base_url="http://testserver")


# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


def run_migrations(connection: Connection):
    config = Config("alembic.ini")
    config.set_main_option("script_location", "migrations")
    config.set_main_option("sqlalchemy.url", settings.postgres_url)
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs("head", rev)

    context = MigrationContext.configure(
        connection, opts={"target_metadata": Base.metadata, "fn": upgrade}
    )

    with context.begin_transaction():
        with Operations.context(context):
            context.run_migrations()


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    # Run alembic migrations on test DB
    async with sessionmanager.connect() as connection:
        await connection.run_sync(run_migrations)

    await sessionmanager._engine.dispose()
    yield

    # Teardown
    await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def transactional_session():
    async with sessionmanager.session() as session:
        try:
            await session.begin()
            yield session
        finally:
            await session.rollback()  # Rolls back the outer transaction

        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f"TRUNCATE {table.name} CASCADE;"))
            await session.commit()


@pytest.fixture(scope="function")
async def db_session(transactional_session):
    yield transactional_session


@pytest.fixture(autouse=True)
def set_factories_session(db_session):
    for my_factory in [OFDReceiptFactory, OFDItemFactory]:
        my_factory._meta.sqlalchemy_session = db_session

from typing import AsyncGenerator
import pytest
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    create_async_engine,
    AsyncTransaction,
)

from src.configs import settings

import pytest_asyncio
from src.database import Base


# def create_test_database():
#     admin_engine = create_engine(settings.postgres_test_url, isolation_level="AUTOCOMMIT")
#     db_name = settings.postgres_test_url.split("/")[-1]
#     with admin_engine.connect() as connection:
#         try:
#             connection.execute(text(f"CREATE DATABASE {db_name}"))
#         except ProgrammingError:
#             print("Database already exists, continuing...")


# @pytest.fixture(scope="session", autouse=True)
# def setup_test_database():
#     # Create an engine and sessionmaker bound to the test database
#     engine = create_engine(settings.postgres_test_url)
#     create_test_database()  # Ensure the test database is created
#     Base.metadata.create_all(bind=engine)  # Create tables
#     yield
#     Base.metadata.drop_all(bind=engine)  # Drop tables after tests


engine = create_async_engine(url=settings.postgres_test_url, echo=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# @pytest.fixture(scope="session", autouse=True)
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_db() -> AsyncGenerator[AsyncConnection, None]:
    # db_name = settings.postgres_test_url.split("/")[-1]
    # async with engine.begin() as conn:
    #     try:
    #         await conn.execute(text(f"CREATE DATABASE {db_name};"))
    #     except ProgrammingError:
    #         print("Database already exists, continuing...")  # noqa: T201
    await create_tables()
    yield
    await drop_tables()


@pytest_asyncio.fixture(scope="session")
async def connection() -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as connection:
        yield connection


@pytest.fixture()
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncTransaction, None]:
    async with connection.begin() as transaction:
        yield transaction


@pytest.fixture()
async def session(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncSession, None]:
    async_session = AsyncSession(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    yield async_session

    await transaction.rollback()

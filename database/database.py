"""Тест."""

from datetime import datetime

from sqlalchemy import NullPool, func, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncConnection,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from sqlalchemy.exc import DBAPIError
from src.configs import EnvEnum, settings

import contextlib
from typing import Annotated, Any, AsyncIterator

# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


class DatabaseSessionManager:
    def __init__(self, **kwargs: dict[str, Any]):
        self._engine: AsyncEngine = create_async_engine(
            url=settings.postgres_url,
            echo=settings.debug,
            poolclass=NullPool,
            **kwargs,
        )
        self._sessionmaker: async_sessionmaker = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def create_db(self):
        async with create_async_engine(
            url=settings.postgres_main_url,
            isolation_level="AUTOCOMMIT",
        ).begin() as connection:
            database = self._engine.url.database
            if settings.enviroment == EnvEnum.test:
                try:
                    await connection.execute(text(f"DROP DATABASE {database} WITH (FORCE)"))
                except DBAPIError:
                    await connection.execute(text("ROLLBACK"))

            await connection.execute(text(f"CREATE DATABASE {database}"))

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        await self.create_db()

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager()


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session


def connection(method):
    async def wrapper(*args, **kwargs):
        async with sessionmanager.session() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше
            finally:
                await session.close()  # Закрываем сессию

    return wrapper

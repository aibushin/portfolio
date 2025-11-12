from sqlalchemy import delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy import func

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert

from src.database import sessionmanager


class BaseDAO:
    model = None  # Устанавливается в дочернем классе

    @classmethod
    async def find_one_or_none_by_pk(cls, val: int):
        """Найти запись по pk."""
        # async with async_session_maker() as session:
        # async with get_db_session() as session:
        pk = cls.model.__mapper__.primary_key[0].name
        async with sessionmanager.session() as session:
            query = select(cls.model).filter_by(**{pk: val})
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """Найти одну запись по фильтрам."""
        async with sessionmanager.session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        """Найти все записи по фильтрам."""
        async with sessionmanager.session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def upsert(cls, **values):
        pk = cls.model.__mapper__.primary_key[0].name
        async with sessionmanager.session() as session:
            async with session.begin():
                stmt = insert(cls.model).values(**values)
                stmt = stmt.on_conflict_do_update(
                    index_elements=[pk],
                    # index_where=cls.model.c.user_email.like('%@gmail.com'),
                    set_={"data": stmt.excluded.data},
                )
                result = await session.execute(stmt)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result

    @classmethod
    async def add(cls, **values):
        """Добавить одну запись."""
        async with sessionmanager.session() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def add_many(cls, instances: list[dict]):
        """Добавить несколько записей."""
        async with sessionmanager.session() as session:
            async with session.begin():
                new_instances = [cls.model(**values) for values in instances]
                session.add_all(new_instances)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instances

    @classmethod
    async def update(cls, filter_by, **values):
        """Обновить записи по фильтру."""
        async with sessionmanager.session() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        """Удалить записи по фильтру."""
        if not delete_all and not filter_by:
            raise ValueError("Нужен хотя бы один фильтр для удаления.")

        async with sessionmanager.session() as session:
            async with session.begin():
                query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount

    @classmethod
    async def count(cls, **filter_by):
        """Подсчитать количество записей."""
        pk = cls.model.__mapper__.primary_key[0].name
        async with sessionmanager.session() as session:
            # query = select(func.count(cls.model.id)).filter_by(**filter_by)
            query = select(func.count(getattr(cls.model, pk))).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def exists(cls, **filter_by):
        """Проверить существование записи."""
        async with sessionmanager.session() as session:
            query = select(cls.model).filter_by(**filter_by).exists()
            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def paginate(cls, page: int = 1, page_size: int = 10, **filter_by):
        """Пагинация записей."""
        async with sessionmanager.session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query.offset((page - 1) * page_size).limit(page_size))
            return result.scalars().all()


# # ---

#     def upsert(model, insert_data, update_data=None, index_elements=None):
#         """Insert (on_conflict_do_update)."""
#         default_index = "id"
#         if not update_data:
#             update_data = copy(insert_data)
#             update_data.pop(default_index, None)

#         insert_stmt = postgresql.insert(model).values(insert_data)
#         do_update_stmt = insert_stmt.on_conflict_do_update(
#             index_elements=index_elements or [default_index],
#             set_=update_data,
#         )
#         return do_update_stmt

# # ---

# @my_router.message(CommandStart())
# async def command_start(message: Message, bot: Bot, base_url: str):
#     await bot.set_chat_menu_button(
#         chat_id=message.chat.id,
#         menu_button=MenuButtonWebApp(text="Open Menu", web_app=WebAppInfo(url=f"{base_url}/demo")),
#     )
#     await message.answer("""Hi!\nSend me any type of message to start.\nOr just send /webview""")

# # ---

# await bot.answer_web_app_query(
#     web_app_query_id=web_app_init_data.query_id,
#     result=InlineQueryResultArticle(
#         id=web_app_init_data.query_id,
#         title="Demo",
#         input_message_content=InputTextMessageContent(
#             message_text="Hello, World!",
#             parse_mode=None,
#         ),
#         reply_markup=reply_markup,
#     ),
# )

import logging

from src.api.models import OFDItem, OFDReceipt
from src.dao.base import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class OFDReceiptDAO(BaseDAO):
    model = OFDReceipt

    @classmethod
    async def add_receipt_with_items(cls, session: AsyncSession, data: dict) -> OFDReceipt:
        """
        Добавляет рецепт и привязанные к нему продукты.

        Аргументы:
        - session: AsyncSession - асинхронная сессия базы данных
        - data: dict - словарь с данными пользователя и профиля

        Возвращает:
        - OFDReceipt - объект рецепта
        """
        items_data = data.pop("items")
        items = [OFDItem(**item) for item in items_data]
        receipt = await OFDReceiptDAO.add(**data, items=items)

        return receipt


class OFDItemDAO(BaseDAO):
    model = OFDItem

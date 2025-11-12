from datetime import datetime

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.api.dao import OFDItemDAO, OFDReceiptDAO
from src.api.models import OFDItem, OFDReceipt
from src.bot.utils.utils import save_receipt
from tests.main.factories import OFDItemFactory, OFDReceiptFactory
from tests.mocks.ofd_responses import (
    VKUSWILL,
    ASHAN,
    YANDEX,
    OZON,
    SDEK,
    MEDSI,
    ROSTELEKOM,
)


class TestClass:
    async def test_create_profile(self, db_session: AsyncSession):
        assert (
            await db_session.execute(select(func.count(OFDReceipt.qrraw)))
        ).scalar() == 0
        assert (
            await db_session.execute(select(func.count(OFDItem.id)))
        ).scalar() == 0

        receipt = OFDReceipt(
            qrraw="qrraw",
            user="user",
            user_inn="userInn",
            seller_address="sellerAddress",
            retail_place="retailPlace",
            retail_place_address="retailPlaceAddress",
            region="region",
            date_time=datetime.now(),
            credit_sum=123,
            code=123,
            operation_type=123,
            total_sum=123,
            buyer_phone_or_address="buyerPhoneOrAddress",
        )
        db_session.add(receipt)
        await db_session.commit()

        assert (
            await db_session.execute(select(func.count(OFDReceipt.qrraw)))
        ).scalar() == 1

        pass

        existing_ofditems = (
            (await db_session.execute(select(OFDItem))).scalars().all()
        )
        assert len(existing_ofditems) == 0

        new_instance = OFDItem(
            name="name",
            price=123,
            quantity=123,
            items_quantity_measure=123,
            receipt_id=receipt.qrraw,
        )
        db_session.add(new_instance)
        await db_session.commit()

        existing_ofditems = (
            (await db_session.execute(select(OFDItem))).scalars().all()
        )
        assert len(existing_ofditems) == 1

    @pytest.mark.parametrize(
        "factory",
        (
            OFDReceiptFactory,
            OFDItemFactory,
        ),
        ids=("OFDReceiptFactory", "OFDItemFactory"),
    )
    async def test_factories(
        self,
        db_session: AsyncSession,
        factory: OFDReceiptFactory | OFDItemFactory,
    ):
        await factory.create()
        assert (
            len(
                (await db_session.execute(select(factory._meta.model)))
                .scalars()
                .all()
            )
            == 1
        )

    @pytest.mark.parametrize(
        ("response", "exp_items_cnt"),
        [
            (VKUSWILL, 5),
            (ASHAN, 7),
            (YANDEX, 1),
            (OZON, 3),
            (SDEK, 3),
            (MEDSI, 1),
            (ROSTELEKOM, 1),
        ],
        ids=(
            "VKUSWILL",
            "ASHAN",
            "YANDEX",
            "OZON",
            "SDEK",
            "MEDSI",
            "ROSTELEKOM",
        ),
    )
    async def test_save_receipt(self, response, exp_items_cnt):
        assert (await OFDReceiptDAO.count()) == 0
        assert await save_receipt(response) == response["request"]["qrraw"]
        assert (await OFDReceiptDAO.count()) == 1
        assert (await OFDItemDAO.count()) == exp_items_cnt

    async def test_items_delete_orphan(self):
        """Удаление позиций чека при удалении чека."""

        qrraw = VKUSWILL["request"]["qrraw"]
        items_cnt = len(VKUSWILL["data"]["json"]["items"])

        await save_receipt(VKUSWILL)
        assert len(await OFDReceiptDAO.find_all(qrraw=qrraw)) == 1
        assert len(await OFDItemDAO.find_all(receipt_id=qrraw)) == items_cnt

        await OFDReceiptDAO.delete(qrraw=qrraw)
        assert len(await OFDReceiptDAO.find_all(qrraw=qrraw)) == 0
        assert len(await OFDItemDAO.find_all(receipt_id=qrraw)) == 0

    @pytest.mark.parametrize(
        ("factory", "pk_kwargs"),
        [
            (OFDReceiptFactory, {"qrraw": "qwe"}),
            (OFDItemFactory, {"id": 1}),
        ],
        ids=("OFDReceiptFactory", "OFDItemFactory"),
    )
    async def test_receipt_pk_constraint(
        self, db_session: AsyncSession, factory, pk_kwargs
    ):
        """qwe"""
        await factory.create(**pk_kwargs)
        with pytest.raises(
            IntegrityError,
            match="duplicate key value violates unique constraint",
        ):
            await factory.create(**pk_kwargs)

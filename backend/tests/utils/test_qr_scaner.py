from aiohttp import ClientConnectionError
from aioresponses import aioresponses
from pydantic import ValidationError
import pytest
from pytest_lazy_fixtures import lfc
from pytest_unordered import unordered

from PIL import Image

from src.api.schemas import QrSchema
from src.utils.cv_scaner import pyzbar_scan_qr
from src.utils.image_merger import stitch

from src.utils.proverka_checka import check_the_receipt_by_qrs
from src.utils.utils import TaskStatus, handle_tasks
from tests.mocks.ofd_responses import ASHAN
from src.configs import settings


class TestQrScaner:
    @pytest.mark.parametrize(
        "data",
        [
            lfc("faker.ofd_qr"),
            pytest.param(
                "invalid format",
                marks=pytest.mark.xfail(raises=ValidationError),
            ),
        ],
        ids=("valid format", "invalid format"),
    )
    def test__qr_schema(self, data):
        assert QrSchema(data=data)

    def test__qr_schema_alt(self):
        with pytest.raises(
            ValidationError,
            match=(
                f"1 validation error for {QrSchema.__name__}\n"
                "data\n  String should match pattern"
            ),
        ):
            QrSchema(data="Невалидный формат данных QR-кода")

    @pytest.mark.parametrize(
        "content",
        (
            [lfc("faker.ofd_qr")] * 2,
            [lfc("faker.word")] * 2,
            [lfc("faker.ofd_qr"), lfc("faker.word")],
        ),
        ids=("2 valid", "2 invalid", "1 valid & 1 invalid"),
    )
    def test__cs2_scan_qr(self, content, faker):
        """Тест распознавания данных QR-кодов с картинки."""
        qr_images = [Image.open(faker.ofd_qr_image(c)) for c in content]
        merged_image = stitch(qr_images)
        result = pyzbar_scan_qr(merged_image)
        assert result == unordered(c for c in content)

    async def test__check_the_receipt_by_qrs__client_connection_error(
        self, faker, mock_aioresponse: aioresponses
    ):
        mock_aioresponse.post(
            url=settings.constants.proverka_checka_url,
            exception=ClientConnectionError("Ошибка сервера"),
        )
        mock_aioresponse.post(
            url=settings.constants.proverka_checka_url,
            exception=ClientConnectionError("Еще одна ошибка сервера"),
        )
        mock_aioresponse.post(
            url=settings.constants.proverka_checka_url,
            status=200,
            payload=ASHAN,
            repeat=True,
        )

        qrs = [faker.ofd_qr() for _ in range(3)]
        tasks = await check_the_receipt_by_qrs(qrs=qrs)
        results = handle_tasks(tasks)

        assert len(results) == 3
        assert sum(len(i) for i in results.values()) == 3

        assert len(results[TaskStatus.SUCCESS]) == 0
        assert len(results[TaskStatus.FAIL]) == 2
        assert len(results[TaskStatus.CANSEL]) == 1

    async def test__check_the_receipt_by_qrs__ok(self, faker, mock_aioresponse):
        mock_aioresponse.post(
            url=settings.constants.proverka_checka_url,
            status=200,
            payload=ASHAN,
            repeat=True,
        )

        qrs = [faker.ofd_qr() for _ in range(3)]
        tasks = await check_the_receipt_by_qrs(qrs=qrs)
        results = handle_tasks(tasks)

        assert len(results) == 3
        assert sum(len(i) for i in results.values()) == 3

        assert len(results[TaskStatus.SUCCESS]) == 3
        assert len(results[TaskStatus.FAIL]) == 0
        assert len(results[TaskStatus.CANSEL]) == 0

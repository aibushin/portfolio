from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest
from src.api.schemas import QrSchema
from src.configs import EnvEnum, Settings, settings
from src.utils.tg_qr_handlers import handle_images
from src.utils.utils import create_secure_file_path
import os

from pytest_lazy_fixtures import lfc


@pytest.fixture
def set_enviroment(request):
    os.environ["ENVIROMENT"] = request.param
    return request.param


@pytest.mark.parametrize("set_enviroment", [e.value for e in EnvEnum], indirect=True)
async def test_settings(set_enviroment):
    settings = Settings()
    assert settings.enviroment == set_enviroment
    if settings.enviroment != EnvEnum.prod:
        assert settings.test is not None
    else:
        assert settings.test is None


@pytest.mark.parametrize(
    ("static_name", "filename", "expected"),
    [
        (
            "static_name",
            "filename",
            settings.test.mock_path / "static_name/filename",
        ),
        (
            "static_name",
            None,
            settings.test.mock_path / "static_name/20250314-224533",
        ),
        (
            settings.test.ofd_responses_dir,
            "filename",
            settings.test.mock_path / f"{settings.test.ofd_responses_dir}/filename.json",
        ),
    ],
)
def test__create_secure_file_path(static_name, filename, expected, freezer):
    freezer.move_to("2025-03-14 22:45:33")
    result = create_secure_file_path(static_name, filename)
    assert result == expected
    assert isinstance(result, Path)


TG_QR_HANDLERS = "src.utils.tg_qr_handlers"


@pytest.mark.parametrize(
    "qr_images",
    (
        lfc("faker.ofd_qr_image"),
        [lfc("faker.ofd_qr_image")] * 2,
        pytest.param("not a qr code", marks=pytest.mark.xfail(raises=FileNotFoundError)),
    ),
    ids=("1 qr code", "list of qr codes", "not a qr code"),
)
@patch(f"{TG_QR_HANDLERS}.check_the_receipt_by_qrs", new_callable=AsyncMock)
@patch(f"{TG_QR_HANDLERS}.validate_ofd_qr_data", new_callable=Mock)
@patch(f"{TG_QR_HANDLERS}.pyzbar_scan_qr", new_callable=Mock)
@patch(f"{TG_QR_HANDLERS}.improve_image_quality", new_callable=Mock)
async def test__handle_images(
    improve_image_quality: Mock,
    pyzbar_scan_qr: Mock,
    validate_ofd_qr_data: Mock,
    check_the_receipt_by_qrs: AsyncMock,
    qr_images,
    faker,
):
    """Тест обработки картинки/ок."""

    validate_ofd_qr_data.return_value = [QrSchema(data=faker.ofd_qr())]

    await handle_images(qr_images)
    improve_image_quality.assert_called_once()
    pyzbar_scan_qr.assert_called_once()
    validate_ofd_qr_data.assert_called_once()
    check_the_receipt_by_qrs.assert_awaited_once()

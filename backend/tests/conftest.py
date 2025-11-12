# from io import BytesIO
# import pyqrcode
import pytest
from aioresponses import aioresponses

from faker import Faker

from src.api.schemas import QrSchema
from tests.mocks.faker_providers.ofd import OfdProvider


@pytest.fixture(autouse=True)
def customize_faker(faker: Faker):
    faker.add_provider(OfdProvider)


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as m:
        yield m


@pytest.fixture
def qr_model():
    def _qr_model(data):
        return QrSchema(data=data)

    yield _qr_model


# @pytest.fixture
# def qrcode():
#     def _qrcode(content, mode="binary"):
#         qr = pyqrcode.create(content=content, mode=mode)
#         io = BytesIO()
#         qr.png(io, scale=2)
#         return io

#     yield _qrcode

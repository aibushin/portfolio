from contextlib import suppress
import logging
from typing import Optional
import cv2
from PIL import Image
from pydantic import ValidationError
from pyzbar import pyzbar

from src.api.schemas import QrSchema
from src.utils import pil2cv

logger = logging.getLogger(__name__)


def cs2_scan_qr(pill_image: Image.Image) -> list[str]:
    """Распознавание данных QR-кодов с картинки."""
    cv_image = pil2cv(pill_image)
    result = cv2.QRCodeDetector().detectAndDecodeMulti(cv_image)
    return result[1]


def validate_ofd_qr_data(qr_data_list: list[str]) -> list[Optional[QrSchema]]:
    """Валидация данных из QR-кодов по формату ОФД."""
    result = []
    for data in qr_data_list:
        with suppress(ValidationError):
            result.append(QrSchema(data=data))
    return result


def pyzbar_scan_qr(image: Image.Image) -> list[str]:
    """Распознавание данных QR-кодов с картинки."""
    decoded_data = pyzbar.decode(image, symbols=[pyzbar.ZBarSymbol.QRCODE])
    result = [r.data.decode("utf-8") for r in decoded_data]
    return result

import asyncio
import logging
from typing import BinaryIO
from PIL import Image

from src.utils.decorators import duration
from src.utils.cv_scaner import pyzbar_scan_qr, validate_ofd_qr_data
from src.utils.image_merger import stitch
from src.utils.proverka_checka import check_the_receipt_by_qrs
from src.utils.pdf_to_img import convert_pdf_to_images
from src.utils.utils import improve_image_quality

logger = logging.getLogger(__name__)


async def handle_pdf(bytes):
    images = convert_pdf_to_images(bytes)
    image = stitch(images)
    data = pyzbar_scan_qr(image)

    result = await check_the_receipt_by_qrs(data)
    return result


@duration
async def handle_images(qr_images: BinaryIO | list[BinaryIO]) -> list[asyncio.Task]:
    if isinstance(qr_images, list):
        pil_images = [Image.open(qr_image) for qr_image in qr_images]
        pil_image = stitch(images=pil_images)
    else:
        pil_image = Image.open(qr_images)

    improved_image = improve_image_quality(pil_image)

    qrs = pyzbar_scan_qr(improved_image)
    validated_qrs = validate_ofd_qr_data(qrs)
    qr_data = [qr.data for qr in validated_qrs]
    results = await check_the_receipt_by_qrs(qr_data)

    return results

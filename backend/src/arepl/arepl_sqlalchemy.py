from arepl_dump import dump  # type: ignore  # noqa: F401
import os
import sys


sys.path.append("/app")

import asyncio
from datetime import datetime
from src.api.dao import OFDReceiptDAO

env = os.getenv("ENVIROMENT")

dt = datetime.strptime("2025-03-09T13:59:00", "%Y-%m-%dT%H:%M:%S")
model = OFDReceiptDAO.model


async def cmd_start() -> None:
    qrraw = "t=20250205T2003&s=3028.00&fn=7384440800207632&i=147289&fp=559008537&n=1"  # noqa: E501
    receipt = await OFDReceiptDAO.find_one_or_none(qrraw=qrraw)

    if not receipt:
        receipt = await OFDReceiptDAO.add(
            qrraw=qrraw,
            user="Anton",
            user_inn="9705114405  ",
            seller_address="no-reply@ofd.yandex.ru",
            retail_place="https://eda.yandex.ru",
            retail_place_address="248926, Россия, Калужская обл., г. Калуга, проезд 1-й Автомобильный, дом 8",  # noqa: E501
            region="40",
            date_time=dt,
            credit_sum=0,
            code=1,
            operation_type=1,
            total_sum=10000,
            buyer_phone_or_address="+79141971272",
        )
    return receipt


qwe = asyncio.run(cmd_start())

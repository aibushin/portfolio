import asyncio
import logging
import aiofiles
import aiohttp

import orjson

from src.utils.utils import BoundedTaskGroup, create_secure_file_path

from src.configs import EnvEnum, settings

logger = logging.getLogger(__name__)


async def fetch(session, qr: str, i):
    async with session.post(
        url=settings.constants.proverka_checka_url,
        data={
            "token": settings.proverka_checka_api_key,
            "qrraw": qr,
        },
    ) as response:
        result = await response.json()

    if settings.enviroment != EnvEnum.prod:
        async with aiofiles.open(
            create_secure_file_path(
                static_name=settings.test.ofd_responses_dir,
                filename=qr,
                create_dir=True,
            ),
            mode="wb",
        ) as f:
            await f.write(orjson.dumps(result))

    return result


async def check_the_receipt_by_qrs(qrs: list[str]) -> list[asyncio.Task]:
    try:
        async with (
            aiohttp.ClientSession() as session,
            BoundedTaskGroup(max_parallelism=10) as group,
        ):
            tasks = [group.create_task(fetch(session, qr, i), name=qr) for i, qr in enumerate(qrs)]
    except* aiohttp.ClientConnectionError as e:
        # TODO: убрать или придумать, как использовать
        logger.error(f"ClientConnectionError: {e}")

    return tasks

import asyncio
from enum import Enum
import logging
import time
import aiohttp
from src.configs import settings
from PIL import Image, ImageFile, ImageEnhance

logger = logging.getLogger(__name__)


tunnel_example = {
    "id": 314886,
    "uid": "2soiGPQdCHVWtrJYyeHTf3l8MCT",
    "os": "linux",
    "active": True,
    "public_url": "https://ofz1y8-95-24-4-52.ru.tuna.am",
    "protocol": "http",
    "protocol_handler": "",
    "location": "ru",
    "forwards_to": "host.docker.internal:5050",
    "created_at": "2025-02-09T19:10:31Z",
    "started_at": "2025-02-09T19:10:31Z",
    "owner": {
        "id": 5083,
        "role": "primary_owner",
        "active": True,
        "name": "",
        "email": "i@abushin.ru",
        "avatar_url": "https://secure.gravatar.com/avatar/90fa06a4c9a0fe0d4fdce8659ce01932?s=512&d=robohash",
    },
    "client_version": 1,
    "client_name": "tuna/0.21.2",
}


async def set_base_site():
    headers = {
        "Accepts": "application/json",
        "Authorization": f"Bearer {settings.tuna_api_key}",
    }

    tunnel_url = "https://my.tuna.am/v1/tunnels"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(tunnel_url, raise_for_status=True) as response:
            data = await response.json()
            tunnel = data[0]
            public_url = tunnel["public_url"]
            logger.debug(f"Tunnel public_url: {public_url}")
            settings.base_site = public_url


def create_secure_file_path(static_name: str, filename: str = None, create_dir: bool = False):
    static_path = settings.test.mock_path / static_name
    extension = {"ofd_responses_raw": ".json", "merged_images": ".png"}.get(static_name, "")
    extension = {
        settings.test.ofd_responses_dir: ".json",
        settings.test.merged_images_dir: ".png",
    }.get(static_name, "")
    if not filename:
        filename = f"{time.strftime('%Y%m%d-%H%M%S')}{extension}"
    else:
        filename = "".join(x for x in filename if x.isalnum()) + extension
    result_path = static_path / filename
    if create_dir:
        result_path.parent.mkdir(parents=True, exist_ok=True)
    return result_path


class TaskStatus(Enum):
    SUCCESS = 1
    FAIL = 2
    CANSEL = 3


def handle_tasks(tasks: list[asyncio.Task]):
    result = {
        TaskStatus.SUCCESS: {},
        TaskStatus.FAIL: {},
        TaskStatus.CANSEL: [],
    }
    for task in tasks:
        if task.cancelled():
            result[TaskStatus.CANSEL].append(task.get_name())
        else:
            try:
                result[TaskStatus.SUCCESS][task.get_name()] = task.result()
            except Exception as e:
                result[TaskStatus.FAIL][task.get_name()] = e

    return result


def improve_image_quality(raw_image: ImageFile.ImageFile) -> Image.Image:
    enhancer = ImageEnhance.Sharpness(raw_image)
    improved_image = enhancer.enhance(4)
    enhancer = ImageEnhance.Contrast(improved_image)
    improved_image = enhancer.enhance(2)

    if settings.debug:
        path = create_secure_file_path(static_name="merged_images", create_dir=True)
        raw_image.save(path)
        path = path.parent / (path.stem + "_improved" + path.suffix)
        improved_image.save(path)

    return improved_image


class BoundedTaskGroup(asyncio.TaskGroup):
    def __init__(self, *args, max_parallelism=0, **kwargs):
        super().__init__(*args)
        if max_parallelism:
            self._sem = asyncio.BoundedSemaphore(max_parallelism)
        else:
            self._sem = None

    def create_task(self, coro, *args, **kwargs):
        if self._sem:

            async def _wrapped_coro(sem, coro):
                async with sem:
                    return await coro

            coro = _wrapped_coro(self._sem, coro)

        return super().create_task(coro, *args, **kwargs)

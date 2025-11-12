from src.configs import EnvEnum, settings
import logging

aiohttp_logger = logging.getLogger("aiohttp")
aiohttp_logger.setLevel(logging.WARNING)
aiohttp_logger.propagate = True
# logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.getLogger("alembic").setLevel(logging.WARNING)
asyncio_logger = logging.getLogger("asyncio")
asyncio_logger.setLevel(logging.WARNING)
asyncio_logger.propagate = True
logging.getLogger("factory").setLevel(logging.WARNING)
logging.getLogger("faker").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("aiogram").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

settings.__init__(enviroment=EnvEnum.test)

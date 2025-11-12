from contextlib import asynccontextmanager
import logging
from typing import Any

from aiogram import Dispatcher
from aiogram.types import Update
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from src.bot.create_bot import bot, tg_dispatcher, start_bot, stop_bot
from src.bot.handlers.admin_router import tg_admin_router
from src.bot.handlers.user_router import tg_user_router
from src.configs import EnvEnum, settings
from src.utils.utils import set_base_site
from src.database import sessionmanager
from src.users.router import router as router_users

logger = logging.getLogger(__name__)


async def lifespan_startup(dp: Dispatcher = tg_dispatcher):
    logger.info("Starting bot setup...")
    if settings.enviroment == EnvEnum.dev:
        await set_base_site()
    dp.include_router(tg_user_router)
    dp.include_router(tg_admin_router)
    if settings.enviroment != EnvEnum.test:
        webhook_url = settings.get_webhook_url()
        await start_bot()
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True,
        )
        logger.info(f"Webhook set to {webhook_url}")
        # await set_webapp_url()


async def lifespan_shutdown():
    logger.info("Shutting down bot...")
    if settings.enviroment != EnvEnum.test:
        await bot.delete_webhook()
        await stop_bot()
        logger.info("Webhook deleted")
        if sessionmanager._engine is not None:
            await sessionmanager.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await lifespan_startup()
    yield
    await lifespan_shutdown()


# app = FastAPI(lifespan=lifespan)
app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI application",
        version="1.0.0",
        description="JWT Authentication and Authorization",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# CORS (Cross-Origin Resource Sharing) middleware configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_users)
# app.mount("/static", StaticFiles(directory="src/static"), "static")


@app.get("/")
async def root():
    return {"msg": "Hello World"}


# @app.get("/favicon.ico", response_class=FileResponse, include_in_schema=False)
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(settings.favicon_path)


@app.post("/webhook")
async def webhook(request: Request) -> dict[str, Any]:
    logger.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    return await tg_dispatcher.feed_update(bot, update)


# @app.post("/webhook")
# async def webhook(request: Request) -> None:
#     update = Update.model_validate(await request.json(), context={"bot": bot})
#     await tg_dispatcher.feed_update(bot, update)

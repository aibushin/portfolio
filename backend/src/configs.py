from enum import Enum
import logging

import os
from pathlib import Path
from typing_extensions import Self
from pydantic import (
    AliasChoices,
    BaseModel,
    Field,
    ConfigDict,
    model_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


logger = logging.getLogger(__name__)


class EnvEnum(str, Enum):
    test = "test"
    dev = "dev"
    prod = "prod"


class Test(BaseModel):
    mock_path: Path = Field(default=Path("tests/mocks"), description="Путь к мокам")
    ofd_responses_dir: str = Field(default="ofd_responses_raw", description="Путь к ОФД чекам")
    merged_images_dir: str = Field(
        default="merged_images", description="Путь к объединённым изображениям"
    )
    receipt_images_dir: str = Field(
        default="receipt_images", description="Путь к изображениям чеков"
    )


class Constants(BaseModel):
    model_config = ConfigDict(frozen=True)

    proverka_checka_url: str = Field(
        default="https://proverkacheka.com/api/v1/check/get",
        description="Окружение",
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"),
        extra="ignore",
    )

    debug: bool = Field(default=False)
    enviroment: EnvEnum = Field(default=EnvEnum.prod, description="Окружение")
    log_config: str = Field(..., description="Путь к конфигам логгера")

    tg_bot_token: str = Field(..., description="Токен бота ТГ")
    tg_admin_id: int = Field(..., description="id админа бота ТГ")
    tunnel_port: str = Field(..., description="Порт туннеля для разработки")
    tuna_api_key: str = Field(..., description="")
    backend_port: int = Field(default=5050, description="")
    proverka_checka_api_key: str = Field(..., description="")

    postgres_url: str = Field(..., description="")
    postgres_main_url: str = Field(
        validation_alias=AliasChoices(
            "POSTGRES_URL",
        ),
        frozen=True,
        description="Урл к главной БД",
    )
    postgres_test_url: str | None = Field(..., description="")
    postgres_echo: str = Field(..., description="")

    base_site: str | None = Field(default="", description="URL сайта для miniapp")
    favicon_path: str = "src/static/img/favicon.ico"

    constants: Constants = Constants()
    test: Test | None = None

    @model_validator(mode="after")
    def setting_test_configs(self) -> Self:
        if self.enviroment != EnvEnum.prod:
            self.test = Test()
            if self.enviroment == EnvEnum.test:
                self.postgres_url = self.postgres_test_url
        return self

    # @computed_field
    # @property
    # def debug(self) -> bool:
    #     """Является ли окружение тестовым."""
    #     return self.enviroment == "test"

    def get_webhook_url(self) -> str:
        """Возвращает URL вебхука с кодированием специальных символов."""
        return f"{self.base_site}/webhook"


settings = Settings()

logger.debug(f"settings: {settings.model_dump_json()}")

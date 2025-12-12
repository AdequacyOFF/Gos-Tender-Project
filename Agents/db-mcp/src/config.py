import os
import logging
from typing import Optional

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("db-mcp")


class Settings(BaseSettings):
    db_host: str = Field(..., alias="DB_HOST")
    db_port: int = Field(..., alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")
    server_port: int = Field(..., alias="DB_MCP_PORT")
    server_host: str = Field(..., alias="DB_MCP_HOST")


# ------------------------------------------------------------------------------
# Фабрика
# ------------------------------------------------------------------------------
_settings_cache: Optional[Settings] = None


def get_settings() -> Settings:
    """Singleton-кеш, чтобы не пересоздавать настройки 100 раз"""
    global _settings_cache
    
    if _settings_cache is None:
        try:
            _settings_cache = Settings()
            
        except ValidationError as e:
            logger.error("❌ Invalid configuration:")
            logger.error(e)
            raise
        
    return _settings_cache

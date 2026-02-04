"""Configurações da aplicação usando Pydantic Settings."""
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configurações da aplicação.
    
    Utiliza variáveis de ambiente para configuração.
    """
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    # Configurações gerais
    APP_NAME: str = "CICNA Middleware"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Configurações de servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    
    # Configurações do Typebot
    TYPEBOT_API_URL: str = "http://10.0.2.217:3001"
    TYPEBOT_ID: str = "teste"
    TYPEBOT_API_TOKEN: str = "BKj63rRdbJGRhXqf7IGpIYct"
    
    # Configurações do WhatsApp
    WHATSAPP_API_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    WHATSAPP_VERIFY_TOKEN: str = ""  # Must be set in production

    # Configurações do Evolution
    EVOLUTION_URL: str = "http://localhost:8080"
    EVOLUTION_API_KEY: str = "dale"
    EVOLUTION_INSTANCE: str = "lucas"

    # Configurações do Instagram
    INSTAGRAM_ACCESS_TOKEN: str = ""
    INSTAGRAM_PAGE_ID: str = ""
    
    # Configurações do Twitter
    TWITTER_API_KEY: str = ""
    TWITTER_API_SECRET: str = ""
    TWITTER_ACCESS_TOKEN: str = ""
    TWITTER_ACCESS_TOKEN_SECRET: str = ""
    
    # Configurações de logging
    LOG_LEVEL: str = "INFO"


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna as configurações da aplicação (cached).
    
    Returns:
        Settings: Configurações da aplicação
    """
    return Settings()

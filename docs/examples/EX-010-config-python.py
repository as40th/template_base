"""
config/ — Конфигурация (Python)

Назначение: Настройки приложения на Python (Pydantic Settings). Разделение по окружениям.
Особенности:
- Загрузка из .env
- Валидация типов
- Наследование для разных окружений
"""
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr

class Settings(BaseSettings):
    """Базовые настройки приложения"""
    
    # Общие
    APP_NAME: str = "AI Agent"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # LLM
    OPENAI_API_KEY: SecretStr = Field(..., env="OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-4"
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/db"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Игнорировать лишние переменные окружения


# config/development.py
from .settings import Settings

class DevelopmentSettings(Settings):
    """Настройки для разработки"""
    
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./dev.db"
    
    # Feature flags для A/B тестов
    FEATURE_A: bool = True
    FEATURE_B: bool = False

# config/production.py
from .settings import Settings

class ProductionSettings(Settings):
    """Настройки для продакшена"""
    
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://prod_user:prod_pass@prod-db:5432/prod_db"
    
    # Режимы работы
    MODE: str = "production"
    LOG_LEVEL: str = "INFO"


# config/__init__.py
import os
from .settings import Settings
from .development import DevelopmentSettings
from .production import ProductionSettings

def get_settings() -> Settings:
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        from .testing import TestingSettings
        return TestingSettings()
    else:
        return DevelopmentSettings()

settings = get_settings()
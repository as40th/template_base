# apps/sync/main.py

"""
apps/ — Точки входа

Назначение: Запускаемые приложения (entrypoints). Каждый файл main.py — это отдельный процесс, который собирает и запускает приложение.
Особенности:
- Минимальный код (только сборка и запуск)
- Разные режимы: синхронный, асинхронный, воркеры
- Использует зависимости из presentation/dependencies/
"""

import uvicorn
from fastapi import FastAPI
from src.presentation.api.routes import router
from src.config import settings

settings.configure_logging()

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
    )
    
    # Подключение роутов
    app.include_router(router)
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
    )
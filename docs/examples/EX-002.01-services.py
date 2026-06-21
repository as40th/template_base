# presentation/dependencies/services.py

"""
presentation/dependencies/ — Слой зависимостей

Назначение: Фабрики зависимостей для DI контейнера.
"""

from fastapi import Depends
from src.application.services.agent_service import AgentService
from src.infrastructure.adapters.llm.openai_adapter import OpenAIAdapter
from src.infrastructure.adapters.storage.postgres_adapter import PostgresAdapter

def get_agent_service() -> AgentService:
    """Фабрика для AgentService"""
    llm_adapter = OpenAIAdapter()
    storage_adapter = PostgresAdapter()
    return AgentService(
        llm=llm_adapter,
        storage=storage_adapter,
    )
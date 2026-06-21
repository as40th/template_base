"""
presentation/api/ — Слой представления

Назначение: Запускаемые приложения (entrypoints). Каждый файл main.py — это отдельный процесс, который собирает и запускает приложение.
Особенности:
- Минимальный код (только сборка и запуск)
- Разные режимы: синхронный, асинхронный, воркеры
- Использует зависимости из presentation/dependencies/
"""

from fastapi import APIRouter, Depends
from src.presentation.api.schemas import AgentCreateRequest, AgentResponse
from src.application.services.agent_service import AgentService
from src.presentation.dependencies.services import get_agent_service

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])

@router.post("/", response_model=AgentResponse)
async def create_agent(
    request: AgentCreateRequest,
    service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    """Создание нового агента"""
    # Только вызов бизнес-логики!
    agent = await service.create_agent(
        name=request.name,
        role=request.role,
    )
    return AgentResponse.from_entity(agent)

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    service: AgentService = Depends(get_agent_service),
) -> AgentResponse:
    """Получение агента по ID"""
    agent = await service.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return AgentResponse.from_entity(agent)
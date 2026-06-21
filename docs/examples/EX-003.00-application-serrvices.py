

"""
application/ — Бизнес-логика

Назначение: Реализация бизнес-сценариев (use cases). Оркестрация работы сервисов и адаптеров.
Особенности:
- Содержит бизнес-правила и сценарии
- Не зависит от инфраструктуры
- Использует интерфейсы (порты) для внешних зависимостей
"""

from typing import Optional
from src.application.interfaces.llm_port import LLMPort
from src.application.interfaces.storage_port import StoragePort
from src.domain.entities import Agent
from src.domain.events import AgentCreated

class AgentService:
    """Сервис для управления агентами"""
    
    def __init__(
        self,
        llm: LLMPort,           # Зависимость от интерфейса, а не реализации!
        storage: StoragePort,
    ):
        self._llm = llm
        self._storage = storage
    
    async def create_agent(self, name: str, role: str) -> Agent:
        """Создать нового агента (use case)"""
        # 1. Бизнес-логика: проверка
        if len(name) < 3:
            raise ValueError("Name must be at least 3 characters")
        
        # 2. Создание сущности
        agent = Agent.create(name=name, role=role)
        
        # 3. Вызов LLM для приветствия (через порт)
        greeting = await self._llm.generate(
            f"Create a welcome message for agent {name} with role {role}"
        )
        agent.greeting = greeting
        
        # 4. Сохранение (через порт)
        await self._storage.save(agent)
        
        # 5. Публикация события
        agent.events.append(AgentCreated(
            agent_id=agent.id,
            name=agent.name,
        ))
        
        return agent
    
    async def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Получить агента по ID"""
        return await self._storage.get(agent_id)
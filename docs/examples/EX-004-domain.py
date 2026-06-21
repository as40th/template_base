"""
domain/ — Ядро (сущности, правила)

Назначение: Бизнес-сущности, value objects, правила и события предметной области. Самая внутренняя часть приложения.
Особенности:
- Чистый Python (без внешних зависимостей)
- Содержит бизнес-правила и методы
- Не знает о БД, API, фреймворках
"""
from dataclasses import dataclass, field
from typing import List
from datetime import datetime
import uuid
from src.domain.events import DomainEvent

@dataclass
class Agent:
    """Бизнес-сущность: Агент"""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    role: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    events: List[DomainEvent] = field(default_factory=list)
    
    @classmethod
    def create(cls, name: str, role: str) -> "Agent":
        """Фабричный метод для создания агента"""
        if not name or len(name) < 3:
            raise ValueError("Agent name must be at least 3 characters")
        if role not in ["assistant", "researcher", "admin"]:
            raise ValueError(f"Invalid role: {role}")
        
        return cls(name=name, role=role)
    
    def deactivate(self) -> None:
        """Деактивировать агента (бизнес-правило)"""
        if self.role == "system":
            raise PermissionError("Cannot deactivate system agent")
        
        self.is_active = False
    
    def can_execute_tool(self, tool: "Tool") -> bool:
        """Может ли агент выполнить инструмент?"""
        if self.role == "admin":
            return True
        
        # Обычные агенты могут выполнять только определённые инструменты
        allowed_tools = ["search", "rag", "calculator"]
        return tool.name in allowed_tools
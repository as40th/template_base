"""
models/ — DTO / Data Models

Назначение: Технические модели данных: схемы для БД, внешних систем, трейсинга.
Особенности:
- Не содержат бизнес-логики
- Служат для сериализации/десериализации
- Могут зависеть от фреймворков (Pydantic, SQLAlchemy)
"""
from sqlalchemy import Column, String, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from pydantic import BaseModel, Field, field_validator

Base = declarative_base()

class AgentDB(Base):
    """ORM-модель агента (только для БД)"""
    
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    def from_entity(cls, agent: "Agent") -> "AgentDB":
        return cls(
            id=agent.id,
            name=agent.name,
            role=agent.role,
            is_active=agent.is_active,
        )
    
    def to_entity(self) -> "Agent":
        from src.domain.entities import Agent
        return Agent(
            id=self.id,
            name=self.name,
            role=self.role,
            is_active=self.is_active,
        )


class LLMRequest(BaseModel):
    """DTO для запроса к LLM"""
    prompt: str = Field(..., min_length=1, max_length=4000)
    model: str = "gpt-4"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    
    @field_validator('prompt')
    def validate_prompt(cls, v):
        if not v.strip():
            raise ValueError("Prompt cannot be empty")
        return v.strip()
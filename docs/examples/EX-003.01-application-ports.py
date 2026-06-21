# application/interfaces/llm_port.py
from abc import ABC, abstractmethod
from typing import List
from src.domain.entities import Message

class LLMPort(ABC):
    """Интерфейс для LLM-провайдеров"""
    
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Генерация ответа от LLM"""
        pass
    
    @abstractmethod
    async def stream(self, prompt: str):
        """Стриминг ответа"""
        pass
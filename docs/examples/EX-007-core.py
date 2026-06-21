"""
core/ — AI-ядро

Назначение: Специализированная AI-функциональность (RAG, инструменты, оценка качества). Это расширение бизнес-логики для AI-сценариев.
Особенности:
- AI-специфичная логика
- Может использовать доменные сущности
- Отделено от основной архитектуры
"""

from typing import List
from src.domain.value_objects import Chunk

class TextChunker:
    """Разбивка текста на чанки для RAG"""
    
    def __init__(
        self,
        chunk_size: int = 500,
        overlap: int = 50,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, metadata: dict) -> List[Chunk]:
        """Разбить текст на чанки"""
        chunks = []
        
        # Простая логика разбивки по символам
        for i in range(0, len(text), self.chunk_size - self.overlap):
            chunk_text = text[i:i + self.chunk_size]
            chunks.append(Chunk(
                content=chunk_text,
                metadata={**metadata, "start": i, "end": i + len(chunk_text)},
                index=len(chunks),
            ))
        
        return chunks

class ToolRegistry:
    """Реестр доступных инструментов"""
    
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
    
    def register(self, name: str, func: Callable, schema: dict) -> None:
        """Зарегистрировать инструмент"""
        self._tools[name] = {
            "func": func,
            "schema": schema,
        }
    
    def execute(self, name: str, params: dict) -> Any:
        """Выполнить инструмент"""
        if name not in self._tools:
            raise ValueError(f"Tool not found: {name}")
        
        tool = self._tools[name]
        validate_tool_params(params, tool["schema"])
        return tool["func"](**params)        
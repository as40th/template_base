"""
infrastructure/ — Адаптеры (реализации)

Назначение: Реализация портов (интерфейсов) для работы с внешними системами: БД, LLM, очереди, файлы.
Особенности:
Реализует интерфейсы из application/interfaces/
Содержит технические детали
Зависит от внешних библиотек (SQLAlchemy, boto3, openai, etc.)
"""
import openai
from src.application.interfaces.llm_port import LLMPort
from src.config import settings

class OpenAIAdapter(LLMPort):
    """Адаптер для OpenAI API"""
    
    def __init__(self):
        self.client = openai.AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=settings.OPENAI_TIMEOUT,
        )
        self.model = settings.OPENAI_MODEL
    
    async def generate(self, prompt: str) -> str:
        """Генерация текста через OpenAI"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except openai.RateLimitError as e:
            # Обработка ошибки с логированием
            raise RuntimeError(f"OpenAI rate limit: {e}")
    
    async def stream(self, prompt: str):
        """Стриминг ответа от OpenAI"""
        async for chunk in await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        ):
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

class GigachatAdapter(LLMPort):
    """Адаптер для Gigachat API"""
    
    def __init__(self):
        self.client = openai.AsyncOpenAI(
            api_key=settings.GIGACHAT_API_KEY,
            timeout=settings.GIGACHAT_TIMEOUT,
        )
        self.model = settings.GIGACHAT_MODEL
    
    async def generate(self, prompt: str) -> str:
        """Генерация текста через Gigachat"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except openai.RateLimitError as e:
            # Обработка ошибки с логированием
            raise RuntimeError(f"Gigachat rate limit: {e}")
    
    async def stream(self, prompt: str):
        """Стриминг ответа от Gigachat"""
        async for chunk in await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        ):
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
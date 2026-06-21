"""
integrations/ — Интеграции с внешними сервисами

Назначение: Клиенты и модели для интеграции с бизнес-сервисами (пользователи, биллинг, нотификации).
Особенности:
- Готовые клиенты для внешних API
- Содержат бизнес-сценарии интеграций
- Отличаются от адаптеров (это не просто технический слой, а бизнес-интеграции)
- При необходимости могут быть обернуты в адаптеры (например, если потребуется получать данные по user из разных источников  или по разным протоколам -> UserServiceAdapter)
"""

from typing import Optional
import httpx
from src.config import settings

class UserServiceClient:
    """Клиент для сервиса пользователей"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=settings.USER_SERVICE_URL,
            timeout=settings.USER_SERVICE_TIMEOUT,
        )
    
    async def get_user(self, user_id: str) -> Optional[dict]:
        """Получить пользователя по ID"""
        response = await self.client.get(f"/users/{user_id}")
        if response.status_code == 200:
            return response.json()
        return None
    
    async def check_permission(self, user_id: str, resource: str) -> bool:
        """Проверить права пользователя"""
        response = await self.client.post(
            "/auth/check-permission",
            json={"user_id": user_id, "resource": resource},
        )
        return response.status_code == 200
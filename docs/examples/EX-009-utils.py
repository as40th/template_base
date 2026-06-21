"""
utils/ — Утилиты

Назначение: Вспомогательные функции, которые не привязаны к бизнес-логике.
Особенности:
- Чистые функции без состояния
- Переиспользуемые
- Не содержат бизнес-логики
"""
import json
from pydantic import BaseModel

def safe_json_loads(data: str) -> dict:
    """Безопасная загрузка JSON"""
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return {}

def model_to_dict(obj: BaseModel) -> dict:
    """Преобразование Pydantic-модели в dict"""
    return obj.model_dump(exclude_none=True)
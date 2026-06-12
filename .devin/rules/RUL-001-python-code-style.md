---
trigger: model_decision
description: Используй только для Python проектов
---

# 1 Именование

## snake_case (функции / переменные)

```python
user_profile
load_document()
build_context()
```

---

## PascalCase (классы)

```python
QueryService
PgVectorAdapter
ToolExecutor
```

---

## UPPER_SNAKE_CASE (константы)

```python
DEFAULT_TIMEOUT
MAX_RETRIES
```

---

# 2. Приватные методы и поля

Все приватные элементы должны начинаться с `_`

```python
class QueryService:

    def _build_prompt(self):
        ...

    def _validate(self):
        ...
```

```python
self._client
self._cache
self._policy
```

---

## Запрещено

```python
__double_underscore_without_need
```

---

# 3. Структура функций

## Требования

* одна функция = одна ответственность
* минимальная вложенность
* early return предпочтителен

---

## Пример

```python
if not user:
    return None
```

---

# 4. Импорты

Порядок:

1. stdlib
2. third-party
3. internal modules

```python
import asyncio
from pathlib import Path

import httpx
from pydantic import BaseModel

from services.query_service import QueryService
```

---

# 5. Комментарии

## Хорошо

* объясняют ПОЧЕМУ
* описывают бизнес-контекст
* объясняют ограничения

---

## Плохо

```python
# создаем клиент
client = Client()
```

---

## Хорошо

```python
# клиент создаётся один раз для переиспользования TCP соединений
client = Client()
```

---

# 6. Docstring

Использовать только для:

* публичных API
* сложной логики
* библиотечных модулей

---

# 7. Логирование

* контекст операции
* correlation id (если есть)
* причина ошибки

---

# 8. Definition of Done

Код готов, если:

* соблюдена типизация
* async-safe
* нет Any
* нет blocking I/O
* code style соблюден
* ошибки обработаны
* архитектура чистая и явная

# Пример реализации паттерна Port-Adapter на примере интеграции с БД для поиска данных по пользователю

# Схема
UserService
      │
      ▼
UserRepositoryPort
      │
      ▼
RoutingUserRepositoryAdapter
      │
      ├── PostgresUserRepositoryAdapter
      │
      └── OracleUserRepositoryAdapter

# Порт

```python
class UserRepositoryPort(Protocol):
    async def get_user(
        self,
        user_id: str
    ) -> User:
        ...
```

# PostgreSQL адаптер

```python
class PostgresUserRepositoryAdapter(
    UserRepositoryPort
):
    async def get_user(
        self,
        user_id: str
    ) -> User:
        ...
```

# Oracle адаптер

```python
class OracleUserRepositoryAdapter(
    UserRepositoryPort
):
    async def get_user(
        self,
        user_id: str
    ) -> User:
        ...
```

# Routing адаптер (опционально, для динамического выбора конкретного адаптера)

```python
class RoutingUserRepositoryAdapter(
    UserRepositoryPort
):
    def __init__(
        self,
        postgres_repo: UserRepositoryPort,
        oracle_repo: UserRepositoryPort,
    ):
        self._postgres = postgres_repo
        self._oracle = oracle_repo

    async def get_user(
        self,
        user_id: str
    ) -> User:

        if user_id.startswith("P"):
            return await self._postgres.get_user(user_id)

        return await self._oracle.get_user(user_id)
```

# Service (ничего не знает про источники данных)

```python
class UserService:

    def __init__(
        self,
        repository: UserRepositoryPort
    ):
        self._repository = repository

    async def get_user(
        self,
        user_id: str
    ):
        return await self._repository.get_user(user_id)
```
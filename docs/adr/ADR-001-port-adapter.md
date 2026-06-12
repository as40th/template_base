# Контекст

Система использует множество внешних компонентов:

* OpenAI
* Anthropic
* Pinecone
* PgVector
* MCP Servers
* внешние API

Необходимо избежать vendor lock-in и смешивания бизнес-логики с инфраструктурой.

# Решение

Используется паттерн:

Service
↓
Port
↓
Routing Adapter
↓
Adapter
↓
External System

## Правила

Сервисы работают только с портами.

Запрещено:

* вызывать адаптеры напрямую
* использовать SDK внешних систем внутри services
* использовать внешние DTO внутри domain layer

Все внешние модели изолируются внутри адаптеров.

Обязателен mapping:

External DTO
↓
Adapter
↓
Internal DTO

## Пример

[ARC-003-port-adapter-flow.md](../architecture/ARC-003-port-adapter-flow.md)

# Последствия

## Плюсы

* независимость от инфраструктуры
* высокая тестируемость
* простая замена провайдеров

## Минусы

* дополнительный слой абстракции

# Альтернативы

* direct SDK usage
* service locator pattern

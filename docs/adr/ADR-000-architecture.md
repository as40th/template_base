# Контекст
Сервис реализует AI-функциональность с использованием LLM, RAG и внешних инструментов (tools).
Требуется:
- управляемость (control)
- расширяемость
- поддержка sync и async execution
- минимизация vendor lock-in

# Решение
Используется архитектура:

Hexagonal Policy-Driven Agentic Architecture (Single Entry, Multi-Execution, Port-Adapters)

Ключевые элементы:
- агент (LangGraph) как ядро
- decision policy layer для выбора стратегии (LLM / RAG / Tools)
- единая точка входа (HTTP API)
- разделение логики и исполнения (sync / async)

# Последствия

## Плюсы
- гибкость в выборе стратегии выполнения
- независимость от моделей и инструментов
- высокая тестируемость
- контроль cost / latency / quality

## Минусы
- выше сложность по сравнению с "просто LLM API"
- требует дисциплины (разделение слоёв)

## Альтернативы
- Direct LLM calls (отклонено — нет контроля)
- LangChain-only pipelines (отклонено — слабый control flow)
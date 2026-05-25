# Статус
Accepted

# Контекст
AI-система недетерминирована.
Без наблюдаемости невозможно:
- дебажить
- оптимизировать
- объяснять ответы

# Решение
Обязательны:

- tracing (OpenTelemetry)
- structured logs
- metrics

Логируется:
- decision path
- LLM calls
- tool calls
- RAG context

# Последствия

## Плюсы
- explainability
- контроль качества
- диагностика

## Минусы
- overhead

## Альтернативы
- минимальное логирование (отклонено)
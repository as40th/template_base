# Контекст

LLM-запросы:
- дорогие
- медленные
- часто повторяются
- могут галлюцинировать

Необходимо:
- снизить стоимость execution
- уменьшить latency
- повысить determinism
- минимизировать unnecessary LLM usage

---

# Решение

В системе вводится Trade-offs Layer.

Основные принципы:
- Determinism-first
- Retrieval-first
- Minimal LLM usage

---

# Determinism-first

LLM используется только там, где задача:
- не решается детерминированно
- требует генерации или reasoning

Все вычисления, фильтрация, агрегации и routing:
- реализуются обычным кодом
- не делегируются LLM без необходимости

---

# Retrieval-first

Приоритет execution:

1. Tools
2. RAG
3. LLM

LLM используется как fallback layer.

Decision policy должна:
- быть explicit
- минимизировать unnecessary generation
- не скрываться внутри prompts

---

# Minimal LLM Usage

Необходимо:
- минимизировать количество LLM-вызовов
- избегать лишних reasoning chains
- ограничивать recursive/agent loops

Для orchestration используется отдельный decision_policy layer.

LLM не используется для принятия решений по умолчанию.

---

# Caching Policy

Допускается caching для:
- LLM responses
- RAG retrieval
- idempotent tools

Cache keys:
- prompt + model + params
- query + retrieval params
- tool input

Cache НЕ должен:
- хранить sensitive data
- нарушать consistency critical data

TTL обязателен.

---

# Последствия

## Плюсы

- снижение cost
- уменьшение latency
- более стабильные ответы
- меньший hallucination rate
- лучший control flow

---

## Минусы

- усложнение orchestration
- cache invalidation complexity
- риск stale data
- больше infrastructure logic

---

# Альтернативы

## LLM-first execution

Отклонено:
- дорого
- нестабильно
- высокий latency
- слабый determinism

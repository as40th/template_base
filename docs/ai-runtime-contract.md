# Назначение
Определяет обязательные требования к любому AI-flow (agent / pipeline / graph) в приложении.

Любая новая AI-логика ДОЛЖНА соответствовать этому контракту.

---

# 1. Общие принципы

## 1.1 Determinism-first
- LLM используется только там, где задача не решается детерминированно
- Любые вычисления, фильтрация, агрегации → классический код

## 1.2 Retrieval-first
Приоритет выполнения:
1. Tools (если требуется действие)
2. RAG (если требуются данные)
3. LLM (fallback)

## 1.3 Minimal LLM usage
- минимизировать количество вызовов LLM
- избегать лишних reasoning-цепочек

---

# 2. Обязательная структура flow

Каждый flow должен содержать:

1. Input validation (guardrails)
2. Decision step (policy)
3. Execution step:
   - LLM / RAG / Tools
4. Output validation
5. Observability hooks

---

# 3. LLM Contract

Каждый LLM-вызов ОБЯЗАН:

## 3.1 Управление
- timeout
- retry policy (bounded)
- fallback (если критично)

## 3.2 Контроль ресурсов
- token budget (input/output)
- max steps (для agent loops)

## 3.3 Structured output
- JSON schema обязателен
- невалидный output → reject / retry

## 3.4 Версионирование
- prompt_id
- prompt_version

## 3.5 Логирование
- модель
- токены
- стоимость
- latency

---

# 4. Tool Contract

Каждый tool ОБЯЗАН:

## 4.1 Контракт
- строгая схема input/output
- versioned (v1, v2…)

## 4.2 Надёжность
- обработка ошибок
- retryable / non-retryable классификация

## 4.3 Безопасность
- allowlist tools
- опасные действия → explicit approval step

## 4.4 Execution
- через ToolPort (никаких прямых вызовов)

---

# 5. RAG Contract

Любой RAG pipeline ОБЯЗАН:

## 5.1 Retrieval
- top-k ограничен
- фильтрация по источникам

## 5.2 Provenance
- каждый ответ должен иметь источники

## 5.3 Качество
- reranking (если применимо)
- query rewriting (если необходимо)

## 5.4 Ограничения
- нельзя прокидывать “сырые” документы в LLM без фильтрации

---

# 6. Decision Policy Contract

Decision layer ОБЯЗАН:

- быть явным (не скрыт в LLM)
- быть логируемым
- быть объяснимым (why this path)

Порядок:
1. rules
2. heuristics
3. LLM (опционально)

---

# 7. Execution Contract

## 7.1 Режимы
- sync → немедленный ответ
- async → enqueue + task_id

## 7.2 Инвариант
- бизнес-логика не зависит от режима выполнения

---

# 8. Caching Contract

- LLM cache обязателен (если применимо)
- ключ: prompt + model + params
- TTL обязателен

Cache НЕ должен:
- хранить PII
- нарушать консистентность критичных данных

---

# 9. Observability Contract

Каждый flow ОБЯЗАН логировать:

## 9.1 Tracing
- trace_id / request_id
- полный путь выполнения

## 9.2 LLM
- prompt_id + version
- tokens
- latency
- cost

## 9.3 Decision
- выбранный путь (LLM / RAG / Tools)

## 9.4 Tools
- input / output
- ошибки

---

# 10. Evaluation Contract

Любое изменение:
- prompt
- model
- RAG

→ должно проходить evaluation

Минимум:
- baseline сравнение
- сохранение отчётов

---

# 11. Безопасность

- входные данные валидируются (schema + size limits)
- prompt injection рассматривается как нормальный сценарий
- sensitive данные:
  - маскируются
  - не логируются

---

# 12. Запрещено

❌ Прямые вызовы:
- openai.chat(...)
- http tool calls вне ToolPort

❌ Отсутствие:
- structured output
- timeout/retry
- логирования

❌ Скрытая логика:
- decision внутри prompt без контроля

---

# 13. Definition of Done (AI flow)

Flow считается корректным, если:

- соответствует всем контрактам выше
- покрыт тестами (happy / edge / failure)
- имеет observability
- проходит evaluation (если применимо)
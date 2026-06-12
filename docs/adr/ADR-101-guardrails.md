# Контекст

LLM-системы:
- могут содержать prompt injections
- генерировать невалидный output
- нарушать execution constraints
- инициировать небезопасные действия

Необходимо обеспечить:
- deterministic behavior
- execution safety
- contract enforcement
- protection от uncontrolled AI behavior

---

# Решение

В системе вводится обязательный Guardrails Layer.

Guardrails применяются на трех уровнях:
- Input
- Runtime
- Output

Каждый AI-flow ОБЯЗАН проходить через все три стадии.

---

# Input Guardrails

Проверки ДО execution:
- schema validation
- size/token limits
- input sanitization
- prompt injection detection
- access/policy validation

Prompt injection рассматривается как нормальный сценарий threat model.

---

# Runtime Guardrails

Ограничения ВО ВРЕМЯ execution:
- timeout
- bounded retries
- fallback policy
- token budget
- max execution steps
- tool allowlist
- explicit approval для dangerous actions

Все tools вызываются только через ToolPort.

Decision logic должна быть:
- explicit
- observable
- не скрыта внутри prompt

---

# Output Guardrails

Проверки ПОСЛЕ execution:
- structured output обязателен
- JSON schema validation обязательна
- invalid output → reject/retry
- sensitive data masking
- provenance/sources validation (для RAG)

Запрещено:
- использовать raw LLM output без validation
- передавать raw documents directly в LLM без filtering

---

# Последствия

## Плюсы

- predictable AI behavior
- safer tool execution
- снижение риска injections
- deterministic contracts
- более надежный orchestration flow

---

## Минусы

- дополнительная complexity
- выше latency
- больше validation logic

---

# Альтернативы

## Trust-based execution

Отклонено:
- недостаточный control
- высокий риск prompt injection
- отсутствие deterministic behavior

## Output-only validation

Отклонено:
- слишком поздний контроль
- не предотвращает unsafe execution
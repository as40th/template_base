# Контекст

AI-система:
- недетерминирована
- зависит от prompts, models и retrieval quality
- может деградировать по качеству со временем

Особенно критично для:
- RAG
- prompt changes
- model changes
- decision policies

Без evaluation невозможно:
- обнаруживать regressions
- сравнивать quality changes
- безопасно обновлять prompts/models
- принимать data-driven решения

---

# Решение

В системе вводится обязательный Evaluation Layer.

Evaluation применяется к:
- prompts
- models
- retrieval pipelines
- orchestration changes

Любое изменение:
- prompt
- model
- retrieval logic
- decision policy

→ требует evaluation.

---

# Dataset Policy

Используется фиксированный evaluation dataset.

Dataset должен содержать:
- query
- expected behavior
- ground truth (если применимо)

Dataset должен:
- versioned
- reproducible
- representative production scenarios

---

# Evaluation Metrics

Используются:
- quality metrics
- operational metrics
- domain metrics

---

# RAG Metrics

Используются:
- faithfulness
- answer relevance
- context precision
- context recall

---

# Operational Metrics

Оцениваются:
- latency
- cost
- retry rate
- token usage

---

# Custom Metrics

Допускаются:
- hallucination heuristics
- tool usage correctness
- domain-specific quality metrics
- business KPIs

---

# Execution Policy

Поддерживаются:
- offline evaluation
- batch execution
- CI-triggered evaluation

Результаты evaluation:
- сохраняются
- versioned
- сравниваются с baseline

Evaluation должна поддерживать:
- regression detection
- trend analysis
- model/prompt comparison

---

# Последствия

## Плюсы

- quality control
- regression detection
- safer model/prompt rollout
- data-driven optimization
- measurable AI quality

---

## Минусы

- необходимость поддерживать datasets
- computational cost
- operational complexity
- сложность domain metrics

---

# Альтернативы

## Manual testing

Отклонено:
- не масштабируется
- субъективно
- плохо обнаруживает regressions

## Unit-tests only

Отклонено:
- не оценивает quality
- не покрывает probabilistic behavior
- недостаточно для RAG/LLM systems
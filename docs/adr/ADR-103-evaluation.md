# Контекст
AI-система:
- недетерминирована
- требует постоянной оценки качества

Особенно критично для:
- RAG
- prompt changes
- model changes

# Решение

Вводится evaluation pipeline:

## 1. Dataset
- фиксированный набор:
  - query
  - ground truth (если есть)
  - expected behavior

## 2. Метрики (RAGAS)
- faithfulness
- answer relevance
- context precision
- context recall

## 3. Custom metrics
- latency
- cost
- tool usage correctness
- hallucination rate (эвристики)

## 4. Execution
- offline evaluation (batch)
- CI-triggered evaluation (опционально)

## Правила

- Любое изменение:
  - prompt
  - model
  - retrieval

→ требует evaluation

- Результаты:
  - сохраняются (reports)
  - сравниваются с baseline

# Последствия

## Плюсы
- контроль качества
- возможность регрессии
- data-driven развитие

## Минусы
- необходимость поддерживать dataset
- стоимость вычислений

## Альтернативы
- ручное тестирование (отклонено)
- только unit-тесты (отклонено)
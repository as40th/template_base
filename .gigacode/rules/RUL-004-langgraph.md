---
mode: agent
apply: apply
---

# LANGGRAPH BEST PRACTICES

## 1. Назначение LangGraph

LangGraph используется для:

- оркестрации LLM-агентов
- управления multi-step reasoning
- построения управляемых execution graph
- координации tool / LLM / decision шагов

LangGraph НЕ используется для:
- бизнес-логики
- хранения состояния приложения
- замены backend-архитектуры

---

## 2. Graph = Control Flow, не Business Logic

Graph описывает:

- последовательность шагов
- условия переходов
- маршрутизацию execution

Graph НЕ должен содержать:

- доменную логику
- инфраструктурные вызовы напрямую
- side-effects вне узлов (nodes)

---

## 3. Node Responsibility

Каждый node должен быть:

- атомарным
- детерминированным (по возможности)
- тестируемым отдельно

Типы nodes:

- decision node → выбор следующего шага
- execution node → выполнение действия
- transformation node → преобразование состояния

---

## 4. State Management

Graph state должен быть:

- явно определён (typed schema)
- неизменяемым (immutable updates)
- минимально достаточным

Запрещено:

- неявное состояние
- глобальные mutable variables
- скрытые side-effects между nodes

---

## 5. Control Flow Rules

Разрешено:

- conditional edges
- branching
- loops (ограниченные)

Запрещено:

- бесконечные циклы без termination condition
- скрытые переходы вне graph definition
- side-effects внутри edge logic

---

## 6. Error Handling

Graph должен явно обрабатывать:

- retryable errors
- fallback paths
- failure termination states

Запрещено:

- silent failures
- implicit retries без контроля
- потеря ошибки между nodes

---

## 7. Observability

Каждое execution run должно содержать:

- trace_id
- node execution path
- timing per node
- input/output каждого node (или hash/summary)

---

## 8. Reproducibility

Graph execution должен быть:

- воспроизводимым при одинаковом input
- логируемым по шагам
- детерминированным в decision nodes (если нет внешних факторов)

---

## 9. Graph Design Principle

Graph должен быть:

- минимальным по числу nodes
- явно читаемым
- без избыточных абстракций

Если graph становится сложным → разделяется на subgraphs

---

## 10. Definition of Done

- каждый node имеет одну ответственность
- state явно типизирован
- control flow прозрачен
- отсутствуют скрытые side effects
- есть observability на уровне nodes
- ошибки обрабатываются явно
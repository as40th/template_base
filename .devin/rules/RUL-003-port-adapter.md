---
trigger: model_decision
description: Используй только для Python проектов
---

# 1. Назначение паттерна

Данный паттерн используется для:

- изоляции бизнес-логики от инфраструктуры
- поддержки нескольких реализаций одного capability
- динамического выбора backend-реализации
- упрощения замены внешних систем

---

## 2. Архитектурная модель

Базовый поток:

```text id="flow1"
Service / Domain
   ↓
Port (contract)
   ↓
Routing Adapter
   ↓
Concrete Adapter(s)
   ↓
External System / Infrastructure
```

Пример data-flow: [tool-usage-flow.md](/docs/architecture/ARC-004-tool-usage-flow.md)

---

## 3. Port Layer (Контракт)

Port:

* определяет интерфейс
* НЕ содержит логики
* НЕ знает о реализации
* НЕ знает о routing

---

## 4. Routing Adapter

Routing Adapter:

* отвечает за выбор конкретной реализации
* НЕ содержит бизнес-логики
* НЕ знает доменную специфику (или знает минимально через policy)
* может использовать:

  * configuration
  * feature flags
  * policy layer
  * heuristics

Принцип:

> Routing Adapter = "куда направить запрос"

---

## 5. Concrete Adapters

Adapter:

* реализует Port
* содержит интеграцию с конкретной системой
* не содержит routing логики
* не знает о других adapters

Принцип:

> Adapter = "как это делается в конкретной системе"

---

## 6. Запрещённые связи

❌ Service → Adapter напрямую
❌ Adapter → Service
❌ Adapter → другой Adapter
❌ Routing logic внутри Port
❌ Business logic внутри Adapter

---

## 7. Responsibility Separation

| Layer           | Responsibility        |
| --------------- | --------------------- |
| Port            | контракт              |
| Routing Adapter | выбор реализации      |
| Adapter         | выполнение интеграции |

---

## 8. Multiple Backends Support

Паттерн используется, когда:

* есть несколько внешних провайдеров
* требуется fallback стратегия
* требуется A/B или canary routing
* есть cost/latency trade-offs

---

## 9. Failure Handling

Routing Adapter может:

* переключать backend при ошибках
* применять fallback strategy
* учитывать retry policies

Adapters:

* НЕ должны делать fallback самостоятельно
* НЕ должны знать про другие adapters

---

## 10. Observability Requirements

Routing layer должен логировать:

* выбранный backend
* причину выбора (policy / fallback / config)
* latency каждого backend (если измеряется)
* ошибки routing decisions

---

## 11. Determinism Rule

Routing decision должен быть:

* воспроизводимым (given same input → same decision, если нет external signals)
* логируемым
* тестируемым

---

## 12. Definition of Done

Архитектура считается корректной, если:

* Port не зависит от реализации
* Routing Adapter не содержит бизнес-логики
* Adapters изолированы друг от друга
* выбор backend централизован
* есть observability routing-решений
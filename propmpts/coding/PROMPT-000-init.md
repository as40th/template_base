---
description: Initial prompt for generating service architecture and business logic
---

# Role
Ты — backend-архитектор и проектировщик бизнес-логики.

---

# Goal
Спроектировать и реализовать сервис, который:

- анализирует входящее текстовое сообщение пользователя
- определяет релевантные банковские продукты
- возвращает результат в строго заданном JSON-формате

---

# Context (Domain)

Сервис является частью банковской микросервисной системы.

Основная задача:
→ определить банковские продукты, связанные с пользовательским запросом

---

# Input

```json
{
  "context_id": "<context_id>",
  "task_id": "<task_id>",
  "user_message": "<user_message>",
  "is_initial": true | false
}
```

---

# Processing Flow

## Step 1 — Получение запроса

Сервис получает запрос на endpoint /product-definition/api/v1/execute

Если `is_initial = true`:

* использовать `user_message`

Если `is_initial = false`:

* вызвать сервис `message_history_contextualization`

```json
POST request:
{
  "context_id": "<context_id>",
  "task_id": "<task_id>"
}
```

```json
response:
{
  "message": "<contextualized_message>"
}
```

→ использовать `contextualized_message` для дальнейшей обработки

---

## Step 2 — анализ текста (LLM слой)

LLM получает текст и возвращает:

```json
{
  "products": ["<product_1>", "<product_2>"]
}
```

---

## Step 3 — формирование результата

Определить `response_code`:

* если найден хотя бы один продукт → `DEFINED`
* если продуктов нет → `NEED_MORE_INFO`
* при ошибке обработки → `ERROR`

---

# Output

```json
{
  "products": ["<Product 1>", "<Product 2>"],
  "response_code": "DEFINED | NEED_MORE_INFO | ERROR"
}
```

---

# Examples

## Example 1

Input:

```text
"потерял карту"
```

Output:

```json
{
  "products": ["Дебетовая карта", "Кредитная карта"],
  "response_code": "NEED_MORE_INFO"
}
```

---

## Example 2

Input:

```text
"хочу повысить лимит по кредитке"
```

Output:

```json
{
  "products": ["Кредитная карта"],
  "response_code": "DEFINED"
}
```

---

# Implementation Notes

## LLM Layer

* используется через абстракцию
* реальная LLM может быть замокана
* интерфейс должен быть заменяемым

---

## Testing Requirements

Реализовать интеграционные тесты:

* scenario `is_initial = true`
* scenario `is_initial = false`
* mock LLM
* mock external service `message_history_contextualization`

---

# Definition of Done

Считается выполненным, если:

* сервис реализует оба сценария обработки
* LLM слой замокан
* интеграционные тесты проходят
* результат соответствует контракту
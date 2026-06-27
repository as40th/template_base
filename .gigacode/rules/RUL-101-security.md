---
mode: agent
apply: apply
---

# 1. Секреты и чувствительные данные

## Запрещено

Любое логирование или вывод:

- паролей
- API keys
- токенов (JWT, OAuth, session tokens)
- приватных ключей
- connection strings
- персональных данных (PII)

---

## Примеры запрещённого кода

```python id="sec1"
logger.info(f"user token: {token}")
```

---

## Требуется вместо этого

* логировать только метаданные
* использовать redaction / masking

```python id="sec3"
logger.info(f"user authenticated: user_id={user.id}, token=***redacted***")
```

---

# 2. Работа с внешними входными данными

## Любой input считается небезопасным

Включает:

* user input
* tool output
* RAG context
* MCP responses
* external APIs

---

## Требования

* всегда валидировать вход
* не доверять структуре данных
* применять schema validation
* защищаться от prompt injection / tool injection

---

# 3. Prompt Injection Protection

## Запрещено

* выполнять инструкции из внешнего контекста без проверки
* передавать raw контекст напрямую в LLM без фильтрации

---

## Требуется

* разделение:

  * system instructions
  * user input
  * external context

* маркировка источников данных

---

# 4. Выполнение кода

## Строго запрещено

* eval()
* exec()
* выполнение произвольных строк
* небезопасная десериализация (pickle, marshal)

---

## Разрешено

* sandboxed execution
* ограниченные runtime environments
* явно разрешённые инструменты

---

# 5. Интеграции с внешними системами

## Требования

* использовать минимальные привилегии
* ограничивать scope токенов
* использовать короткоживущие креденшалы

---

## Запрещено

* хранить секреты в коде
* передавать секреты через prompt
* логировать headers с auth данными

---

# 6. Логирование

## Требования

Логи должны:

* содержать только безопасные данные
* быть пригодными для трассировки (trace_id, request_id)
* не содержать PII

---

## Обязательная редакция

* email → masked
* phone → masked
* tokens → removed
* ids → hashed (при необходимости)

---

# 7. RAG безопасность

## Запрещено

* доверять retrieved контексту как истине
* использовать RAG без фильтрации

---

## Требуется

* reranking / filtering
* source attribution
* injection scanning

---

# 8. Tool safety

## Каждый tool вызов должен:

* иметь строгий input schema
* иметь output validation
* быть идемпотентным (если возможно)

---

## Запрещено

* динамическое формирование tool calls из текста без проверки
* выполнение неизвестных MCP инструментов без registry

---

# 9. Data handling

## Требуется

* минимизация данных (data minimization)
* хранение только необходимого
* ограничение времени жизни данных

---

# 10. Definition of Done

Код считается безопасным, если:

* нет логирования секретов
* все inputs валидируются
* нет eval/exec
* prompt injection учтён
* внешние системы изолированы
* соблюдён principle of least privilege

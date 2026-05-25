# Контекст
LLM-запросы:
- дорогие
- медленные
- часто повторяются

RAG:
- повторяющиеся retrieval-запросы
- стабильные embeddings

# Решение

Вводится многоуровневый caching:

## 1. LLM Cache
Кэшируется:
- prompt + параметры модели → response

Ключ:
hash(prompt + model + params)

## 2. RAG Cache
Кэшируется:
- query → retrieved documents

## 3. Tool Cache (опционально)
Для idempotent tools:
- input → output

## Backend:
- Apache Ignite (основной)
- TTL обязателен

## Правила

- Кэш должен быть:
  - детерминированным
  - безопасным (без PII)
- Для LLM:
  - учитывать temperature (если > 0 → кэш ограничен)
- Cache bypass:
  - debug режим
  - forced refresh

# Последствия

## Плюсы
- снижение стоимости
- уменьшение latency
- стабильность ответов

## Минусы
- риск устаревших данных
- усложнение invalidation

## Альтернативы
- без кэша (отклонено — дорого)
- только HTTP cache (отклонено — недостаточно)
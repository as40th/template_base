# Контекст
Система зависит от:
- LLM провайдеров
- tool execution (MCP / HTTP)
- RAG storage

Требуется возможность замены без переписывания логики.

# Решение
Используется Ports & Adapters (Hexagonal architecture):

Ports:
- LLMPort
- ToolPort
- RAGPort

Adapters:
- OpenAI / Anthropic
- HTTP / MCP tools
- pgvector / Pinecone

# Последствия

## Плюсы
- независимость от провайдеров
- удобство тестирования
- гибкость

## Минусы
- дополнительный слой абстракции

## Альтернативы
- прямые вызовы SDK (отклонено — высокая связность)
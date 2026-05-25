# Контекст
AI-логика требует:
- stateful execution
- branching
- retries
- tool calls

# Решение
Используется LangGraph как основной orchestrator.

Паттерн:
StateGraph + nodes

Mandatory Nodes:
- guardrail
- decision
- tool
    - rag_tool
    - other_tools
- llm
- eval

# Последствия

## Плюсы
- явный control flow
- расширяемость
- поддержка multi-step reasoning

## Минусы
- learning curve
- сложнее чем простой pipeline

## Альтернативы
- LangChain chains (отклонено — слабый контроль)
- custom orchestration (отклонено — дорого)
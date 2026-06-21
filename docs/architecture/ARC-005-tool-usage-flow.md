# User Request

```text
"Запиши меня к стоматологу"
```

---

# High-Level Flow

```text
User Query
   ↓
API
   ↓
QueryService
   ↓
Decision Policy
   ↓
Tool Policy
   ↓
Tool Executor
   ↓
ToolPort
   ↓
Tool Routing Adapter
   ↓
MCP Adapter / InProcess Adapter / HTTP Adapter
   ↓
Tool Backend
   ↓
Tool Result
   ↓
Result Validation
   ↓
Context Builder
   ↓
LLMPort
   ↓
LLM Routing Adapter
   ↓
OpenAI Adapter
   ↓
Generated Response
   ↓
Final Response
```

---

# 1. API Layer

Получаем HTTP запрос.

```python
@router.post("/query")
async def query(
    request: MainRequest,
    service: QueryService = Depends(...)
):
    return await service.execute(request)
```

---

# 2. Service Layer

Service orchestrates flow.

```python
class QueryService:

    async def execute(self, request):

        decision = await self.decision_policy.decide(
            request.query
        )

        if decision == "tool":
            return await self.execute_tool_flow(request)

        return await self.execute_llm_flow(request)
```

---

# 3. Decision Policy

Decision layer определяет:

* нужен ли tool
* нужен ли RAG
* нужен ли direct LLM

```python
class DecisionPolicy:

    async def decide(self, query):
        if requires_action(query):
            return "tool"

        if requires_knowledge(query):
            return "rag"

        return "llm"
```

---

# Decision Example

## Было

```text
"Запиши меня к стоматологу"
```

## Стало

```python
{
    "execution_type": "tool"
}
```

---

# 4. Tool Policy

Определяется:

* какой tool использовать
* как выполнять tool
* нужен ли MCP

```python
class ToolPolicy:

    async def resolve(self, query):
        return {
            "tool_name": "appointment_tool",
            "transport": "mcp",
            "timeout": 10
        }
```

---

# Tool Resolution

## Было

```text
"Запиши меня к стоматологу"
```

## Стало

```python
{
    "tool_name": "appointment_tool",
    "transport": "mcp"
}
```

---

# 5. Tool Executor

Оркестрация выполнения tools.

```python
class ToolExecutor:

    async def execute(
        self,
        tool_name,
        payload
    ):

        return await self.tool_port.execute(
            tool_name=tool_name,
            payload=payload
        )
```

---

# 6. ToolPort

Port определяет execution contract.

```python
class ToolPort(Protocol):

    async def execute(
        self,
        tool_name: str,
        payload: dict
    ) -> ToolResult:
        ...
```

---

# 7. Tool Routing Adapter

Routing между:

* MCP
* HTTP
* local tools

```python
class RoutingToolAdapter(ToolPort):

    async def execute(
        self,
        tool_name,
        payload
    ):

        if tool_name in MCP_TOOLS:
            return await self.mcp.execute(
                tool_name,
                payload
            )

        return await self.inprocess.execute(
            tool_name,
            payload
        )
```

---

# Routing Decision

```text
appointment_tool → MCP Adapter
```

---

# 8. MCP Adapter

Реальный MCP protocol execution.

```python
class MCPAdapter(ToolPort):

    async def execute(
        self,
        tool_name,
        payload
    ):

        return await self.client.call_tool(
            tool_name,
            payload
        )
```

---

# 9. Tool Backend

Внешний MCP server выполняет действие.

```text
MCP Server
   ↓
Dental Appointment Service
```

---

# Tool Result

```python
{
    "status": "success",
    "appointment_id": "A-12345",
    "doctor": "Dr. Ivanov",
    "date": "2026-06-10"
}
```

---

# 10. Result Validation

Проверяется:

* schema
* allowed fields
* security policy

```python
validated = validator.validate(result)
```

---

# 11. Context Builder

Tool result преобразуется в LLM context.

```python
prompt = f"""
Tool Result:

{validated}

Сформируй ответ пользователю.
"""
```

---

# Context Enrichment

## Было

```python
{
    "appointment_id": "A-12345"
}
```

## Стало

```text
Запись успешно создана.
Номер записи: A-12345
```

---

# 12. LLMPort

Unified LLM contract.

```python
response = await llm_port.generate(prompt)
```

---

# 13. LLM Routing Adapter (опционально, для динамического выбора конкретного адаптера)

Выбирает:

* OpenAI
* Anthropic
* local model

```python
class RoutingLLMAdapter(LLMPort):

    async def generate(self, prompt):

        return await self.openai.generate(prompt)
```

---

# 14. OpenAI Adapter

Реальный provider call.

```python
class OpenAIAdapter(LLMPort):

    async def generate(self, prompt):

        return await client.chat.completions.create(
            model="gpt-4.1",
            messages=[...]
        )
```

---

# 15. Generated Response

```text
"Вы успешно записаны к стоматологу.
Дата приёма: 10 июня.
Номер записи: A-12345"
```

---

# 16. Final Response

```python
return MainResponse(
    answer=response
)
```
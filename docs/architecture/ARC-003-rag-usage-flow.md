# User Request

```text
"Как записаться к стоматологу?"
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
Retriever Policy
   ↓
Retriever
   ↓
RAGPort
   ↓
RAG Routing Adapter
   ↓
PgVector Adapter
   ↓
Vector DB
   ↓
Retrieved Chunks
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

# 1. Получаем HTTP запрос.

```python
@router.post("/query")
async def query(
    request: MainRequest,
    service: QueryService = Depends(...)
):
    return await service.execute(request)
```

---

# 2. Service решает, нужен ли RAG:

```python
class QueryService:

    async def execute(self, request):
        if self._needs_rag(request.query):
            return await self._execute_rag(request)

        return await self._execute_llm(request)
```

---

# 3. Дообогащаем запрос параметрами retrieval policy.

```python
class RetrievalPolicy:
    # Здесь можно добавить логику для динамического определения policy в зависимости от темы запроса
    def get_policy(self):
        return {
            "domain": "medical", # Например, если запрос про стоматологию - domain будет medical
            "top_k": 5, # Количество топовых результатов для возврата
            "strategy": "hybrid", # Стратегия поиска (hybrid, semantic, keyword)
            "reranking": True # Флаг необходимости reranking (пересортировки) результатов
        }
```

---

# 4. Retriever выполняет retrieval через Port. Здесь на вход уже передается запрос, дообогащенный соответствующим knowledge и с указанием domain (medical)

```python
class Retriever:

    async def retrieve(
        self,
        query,
        policy
    ):

        rewritten_query = rewrite_query(query)  # Переформулируем запрос для лучшего поиска

        return await self.rag_port.retrieve(
            query=rewritten_query,           
            policy=policy
        )
```

---

# 5. Port 
Port — только контракт.

```python
class RAGPort(Protocol):

    async def retrieve(
        self,
        query: str,
        policy: dict
    ) -> list[RetrievalResult]:
        ...
```

---

# 6. RAG Routing Adapter
Выбирает retrieval backend (источник знаний) на основе domain. Например, для medical domain используется PgVector, для other domains — поиск в интернете и т.д.

```python
class RoutingRAGAdapter(RAGPort):

    async def retrieve(
        self,
        query: str,
        policy: dict
    ) -> list[RetrievalResult]:

        if policy["domain"] == "medical":
            return await self.pgvector.retrieve(
                query=query,
                top_k=policy["top_k"]
            )

        return await self.web_search.retrieve(
            query=query,
            top_k=policy["top_k"]
        )
```

---

# 7. Storage Adapter

Вызывается конкретный storage adapter в зависимости от domain.

```python
class PgVectorAdapter(RAGPort):

    async def retrieve(
        self,
        query: str,
        policy: dict
    ) -> list[RetrievalResult]:

        embedding = embed(query)

        rows = await self.db.search(
            embedding=embedding,
            top_k=policy["top_k"]
        )

        return map_rows(rows)
```

---

# 8. Embedding Search

## Query

```text
"Запись к стоматологу через клинику"
```

## Embedding

```python
[0.123, 0.991, ...]
```

## Vector Search

```sql
SELECT *
FROM medical_chunks
ORDER BY embedding <-> query_embedding
LIMIT 5
```

---

# 9. Retrieved Chunks

Получаем релевантный контекст.

```python
[
    {
        "text":
            "Записаться к стоматологу можно:
             через Госуслуги,
             по телефону,
             через сайт клиники",

        "source":
            "medical_faq.pdf"
    }
]
```

---

# 10. Context Builder

Собирается final prompt.

```python
prompt = f"""
Контекст:

{chunks}

Вопрос:
{user_query}
"""
```

---

# Prompt Enrichment

## Было

```text
"Как записаться к стоматологу?"
```

## Стало

```text
Контекст:
- запись через Госуслуги
- запись через сайт клиники

Вопрос:
Как записаться к стоматологу?
```

---

# 11. LLMPort

Единый контракт для LLM.

```python
response = await llm_port.generate(prompt)
```

---

# 12. LLM Router
Выбирает LLM на основе каких либо факторов (domain, complexity, etc).

```python
class LLMRouter(LLMPort):

    async def generate(
        self,
        prompt,
        domain,
        complexity
    ):
        # TODO: различные условия для выбора LLM
        if domain == "medical":
            return await self.openai_adapter.generate(
                prompt=prompt
            )

        return await self.anthropic_adapter.generate(
            prompt=prompt
        )
```

---

# 13. LLM Adapter

Реальный вызов OpenAI.

```python
class OpenAIAdapter(LLMPort):

    async def generate(self, prompt):

        return await client.chat.completions.create(
            model="gpt-4.1",
            messages=[...]
        )
```

---

# 14. Generated Response

```text
"Вы можете записаться к стоматологу:
- через Госуслуги
- через сайт клиники
- по телефону"
```

---

# 15. Output Validation

Проверяются:

* schema
* citations
* hallucinations

```python
validated = output_validator.validate(response)
```

---

# 16. Final Response

```python
return MainResponse(
    answer=validated.answer,
    sources=validated.sources
)
```
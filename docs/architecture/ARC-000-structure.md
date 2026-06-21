.
├── src/
│   ├── apps/                            # ⬅️ 1. ТОЧКИ ВХОДА
│   │   ├── __init__.py
│   │   ├── sync/
│   │   │   └── main.py
│   │   ├── async/
│   │   │   └── main.py
│   │   └── worker/
│   │       └── main.py
│   │
│   ├── presentation/                    # ⬅️ 2. СЛОЙ ПРЕДСТАВЛЕНИЯ
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── dependencies/
│   │   │   ├── __init__.py
│   │   │   ├── services.py
│   │   │   ├── adapters.py
│   │   │   └── auth.py
│   │   └── middlewares.py
│   │
│   ├── application/                     # ⬅️ 3. БИЗНЕС-ЛОГИКА
│   │   ├── __init__.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── agent_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── tool_service.py
│   │   │   └── evaluation_service.py
│   │   └── interfaces/                  # Порты (абстракции)
│   │       ├── __init__.py
│   │       ├── llm_port.py
│   │       ├── tool_port.py
│   │       ├── rag_port.py
│   │       ├── telemetry_port.py
│   │       └── external_port.py
│   │
│   ├── domain/                          # ⬅️ 4. Доменные сущности и правила
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── agent.py
│   │   │   ├── tool.py
│   │   │   └── document.py
│   │   ├── value_objects/
│   │   │   ├── embedding.py
│   │   │   ├── chunk.py
│   │   │   └── retrieval_result.py
│   │   ├── events/
│   │   │   ├── agent_events.py
│   │   │   └── rag_events.py
│   │   └── graph/
│   │       ├── agent_state.py
│   │       └── nodes/
│   │           ├── guardrail_node.py
│   │           ├── decision_node.py
│   │           ├── llm_node.py
│   │           ├── tool_node.py
│   │           └── eval_node.py
│   │
│   ├── infrastructure/                  # ⬅️ 5. ИНФРАСТРУКТУРА
│   │   ├── __init__.py
│   │   ├── adapters/
│   │   │   ├── llm/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── openai_adapter.py
│   │   │   │   ├── anthropic_adapter.py
│   │   │   │   ├── gigachat_adapter.py
│   │   │   │   └── routing_adapter.py   # ⬅️ РОУТИНГ МЕЖДУ АДАПТЕРАМИ (НЕОБЯЗАТЕЛЬНЫЙ СЛОЙ -> только в случае, если предполагается динамический выбор адаптера)
│   │   │   ├── rag/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── pinecone_adapter.py
│   │   │   │   ├── pgvector_adapter.py
│   │   │   │   ├── web_search_adapter.py
│   │   │   │   └── routing_adapter.py
│   │   │   ├── tools/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── inprocess_adapter.py
│   │   │   │   ├── mcp_adapter.py
│   │   │   │   ├── http_adapter.py
│   │   │   │   ├── grpc_adapter.py
│   │   │   │   ├── sandbox_adapter.py
│   │   │   │   └── routing_adapter.py
│   │   │   ├── external/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── http_adapter.py
│   │   │   │   ├── grpc_adapter.py
│   │   │   │   └── mocks/
│   │   │   │       └── external_mock.py
│   │   │   ├── storage/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── postgres_adapter.py
│   │   │   │   └── ignite_adapter.py
│   │   │   ├── queue/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── kafka_adapter.py
│   │   │   │   └── celery_adapter.py
│   │   │   └── observability/
│   │   │       ├── __init__.py
│   │   │       ├── tracing_adapter.py
│   │   │       ├── logging_adapter.py
│   │   │       └── metrics_adapter.py
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── rate_limit.py
│   │       └── tracing.py
│   │
│   ├── integrations/                    # ⬅️ 6. ИНТЕГРАЦИИ
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── billing_service.py
│   │   └── notification_service.py
│   │
│   ├── core/                            # ⬅️ 7. AI-ЯДРО
│   │   ├── __init__.py
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── ingestion/
│   │   │   │   ├── loaders.py
│   │   │   │   ├── chunking.py
│   │   │   │   └── embeddings.py
│   │   │   └── retrieval/
│   │   │       ├── retriever.py
│   │   │       ├── reranker.py
│   │   │       ├── query_rewrite.py
│   │   │       └── policies.py
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── registry.py
│   │   │   ├── executor.py
│   │   │   ├── policies.py
│   │   │   ├── validation.py
│   │   │   └── internal/
│   │   │       ├── rag_tool.py
│   │   │       ├── db_tool.py
│   │   │       └── search_tool.py
│   │   └── evaluation/
│   │       ├── __init__.py
│   │       ├── pipelines/
│   │       │   ├── ragas_pipeline.py
│   │       │   └── custom_metrics.py
│   │       ├── runner.py
│   │       └── datasets/
│   │           └── sample_dataset.json
│   │
│   ├── models/                          # ⬅️ 8. DTO
│   │   ├── __init__.py
│   │   ├── llm/
│   │   │   └── llm_schema.py
│   │   ├── tools/
│   │   │   └── tool_schema.py
│   │   ├── db/
│   │   │   └── db_entity.py
│   │   ├── external/
│   │   │   └── external.py
│   │   └── trace/
│   │       └── trace.py
│   │
│   ├── utils/                           # ⬅️ 9. УТИЛИТЫ
│   │   ├── __init__.py
│   │   ├── json_utils.py
│   │   ├── time_utils.py
│   │   └── token_utils.py
│   │
│   ├── config/                          # ⬅️ 10. КОНФИГИ (Python)
│   │   ├── settings.py
│   │   ├── local.py
│   │   ├── staging.py
│   │   ├── production.py
│   │   └── testing.py
│   │
│   ├── prompts/                         # ⬅️ 11. ПРОМПТЫ
│   │   ├── __init__.py
│   │   ├── registry.py
│   │   └── versions/
│   │       ├── v1/
│   │       │   ├── system.md
│   │       │   └── user.md
│   │       └── v2/
│   │           ├── system.md
│   │           └── user.md
│   │
│   └── data/                            # ⬅️ 12. ДАННЫЕ
│       ├── __init__.py
│       ├── datasets/
│       └── embeddings/
│
├── config/                              # ВНЕШНИЕ КОНФИГИ (YAML)
│   ├── app.yaml
│   ├── logging.yaml
│   └── observability/
│       ├── opentelemetry.yaml
│       ├── prometheus.yaml
│       └── grafana.json
│
├── deploy/                              # ИНФРАСТРУКТУРА
│   ├── docker/
│   │   └── Dockerfile.api
│   ├── k8s/
│   │   └── deployment.yaml
│   └── terraform/
│       └── main.tf
│
├── tests/                               # ТЕСТЫ
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_agent.py
│   │   └── test_tools.py
│   ├── integration/
│   │   └── test_rag_pipeline.py
│   ├── e2e/
│   │   └── test_api_flow.py
│   └── evaluation/
│       └── test_quality_metrics.py
│
├── docs/                                # ДОКУМЕНТАЦИЯ
│   ├── adr/
│   ├── architecture/
│   └── diagrams/
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
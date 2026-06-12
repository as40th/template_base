.
├── app/
│   ├── apps/                                        # entrypoints / процессы
│   │   ├── api/                                     # sync API
│   │   │   ├── main.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── api_async/                               # async API
│   │   │   ├── main.py
│   │   │   └── enqueue.py
│   │   │
│   │   └── worker/                                  # background workers
│   │       ├── main.py
│   │       └── consumer.py
│   │
│   ├── container/                                   # composition root / DI
│   │   ├── container.py
│   │   ├── providers.py
│   │   └── config.py
│   │
│   ├── models/                                      # DTO / Schemas / State
│   │   ├── api/
│   │   │   └── v1
│   │   │       └── api.py                           # API приложения
│   │   │
│   │   ├── llm/
│   │   │   └── llm_schema
│   │   │
│   │   ├── tools/
│   │   │   └── tool_schema.py
│   │   │
│   │   ├── db/
│   │   │   └── db_entity.py
│   │   │
│   │   ├── rag/
│   │   │   ├── chunk.py
│   │   │   ├── embedding.py
│   │   │   ├── retrieval_result.py
│   │   │   └── vector_document.py
│   │   │
│   │   ├── external/
│   │   │   └── external.py
│   │   │
│   │   ├── events/
│   │   │   └── event.py
│   │   │
│   │   ├── graph/
│   │   │    └── graph_state.py
│   │   │
│   │   ├── trace
│   │       └── trace.py
│   │
│   ├── ports/                                       # Hexagonal ports
│   │   ├── executor_port.py
│   │   ├── llm_port.py
│   │   ├── tool_port.py
│   │   ├── telemetry_port.py
│   │   ├── rag_port.py
│   │   └── extrenal_service_port.py
│   │
│   ├── adapters/                                    # Hexagonal adapters
│   │   ├── mocks/
│   │
│   │   ├── api/
│   │   │   ├── routes.py
│   │   │   └── middleware/
│   │   │       ├── rate_limit.py
│   │   │       └── tracing.py
│   │   │
│   │   ├── rag/
│   │   │   ├── pinecone_adapter.py
│   │   │   ├── pgvector_adapter.py
│   │   │   ├── web_search_adapter.py
│   │   │   └── routing_adapter.py
│   │   │
│   │   ├── llm/
│   │   │   ├── openai_adapter.py
│   │   │   ├── anthropic_adapter.py
│   │   │   ├── gigachat_adapter.py
│   │   │   └── routing_adapter.py
│   │   │
│   │   ├── tools/
│   │   │   ├── inprocess_adapter.py
│   │   │   ├── mcp_adapter.py
│   │   │   ├── http_adapter.py
│   │   │   ├── grpc_adapter.py
│   │   │   ├── sandbox_adapter.py
│   │   │   └── routing_adapter.py
│   │   │
│   │   ├── integrations/
│   │   │   ├── http/
│   │   │   │   └── external_service_http_adapter.py
│   │   │   │
│   │   │   ├── grpc/
│   │   │   │   └── external_service_grpc_adapter.py
│   │   │   │
│   │   │   └── mocks/
│   │   │       └── external_service_mock.py           # Не для тестирования! Для интеграций с внешними сервисами, которые еще не реализованы
│   │   │
│   │   ├── queue/
│   │   │   ├── kafka_adapter.py
│   │   │   └── celery_adapter.py
│   │   │
│   │   ├── storage/
│   │   │   ├── postgres_adapter.py
│   │   │   ├── ignite_adapter.py
│   │   │   └── pinecone_adapter.py
│   │   │
│   │   ├── telemetry/
│   │   │   ├── opentelemetry_adapter.py
│   │   │   ├── logging_adapter.py
│   │   │   └── metrics_adapter.py
│   │   │
│   │   └── executor/
│   │       ├── sync_executor.py
│   │       └── async_executor.py
│   │
│   ├── services/                                    # бизнес-логика
│   │   ├── query_service.py
│   │   ├── async_service.py
│   │   ├── eval_service.py
│   │   │
│   │   ├── graph/
│   │   │   ├── agent.py
│   │   │   ├── state_builder.py
│   │   │   └── nodes/
│   │   │       ├── guardrail_node.py
│   │   │       ├── decision_node.py
│   │   │       ├── llm_node.py
│   │   │       ├── tool_node.py
│   │   │       └── eval_node.py
│   │   │
│   │   ├── tools/
│   │   │   ├── tool_registry.py
│   │   │   ├── tool_executor.py
│   │   │   ├── tool_policy.py
│   │   │   ├── validation.py
│   │   │   ├── internal/
│   │   │   │   ├── rag_tool.py
│   │   │   │   ├── db_tool.py
│   │   │   │   └── external_api_tool.py
│   │   │   └── external/
│   │   │       ├── crm_tool.py
│   │   │       ├── search_tool.py
│   │   │       └── calendar_tool.py
│   │   │
│   │   ├── rag/
│   │   │   ├── ingestion/
│   │   │   │   ├── loaders.py
│   │   │   │   ├── chunking.py
│   │   │   │   └── embeddings.py
│   │   │   │
│   │   │   └── retrieval/
│   │   │       ├── retriever.py
│   │   │       ├── reranker.py
│   │   │       ├── query_rewrite.py
│   │   │       └── retrieval_policy.py
│   │   │
│   │   ├── integrations/
│   │   │   ├── user_service.py
│   │   │   ├── billing_service.py
│   │   │   └── notification_service.py
│   │   │
│   │   ├── evaluation/
│   │   │   ├── pipelines/
│   │   │   │   ├── ragas_pipeline.py
│   │   │   │   └── custom_metrics.py
│   │   │   ├── runner/
│   │   │   │   └── evaluation_runner.py
│   │   │   └── datasets/
│   │   │       └── sample_dataset.json
│   │   │
│   │   └── features/
│   │       ├── flags/
│   │       │   └── model_flags.py
│   │       └── experiments.py
│   │
│   ├── prompts/
│   │   ├── registry.py
│   │   └── versions/
│   │       ├── v1.py
│   │       └── v2.py
│   │
│   ├── utils/
│   │   ├── json_utils.py
│   │   ├── time_utils.py
│   │   └── token_utils.py
│   │
│   ├── infra/
│   │   ├── docker/
│   │   │   └── Dockerfile.api
│   │   ├── k8s/
│   │   │   └── deployment.yaml
│   │   ├── terraform/
│   │   │   └── main.tf
│   │   └── environments/
│   │       ├── local/
│   │       │   └── .env
│   │       ├── staging/
│   │       │   └── .env
│   │       └── prod/
│   │           └── .env
│   │
│   ├── observability/
│   │   ├── tracing/
│   │   │   └── opentelemetry.yaml
│   │   ├── metrics/
│   │   │   └── prometheus.yaml
│   │   ├── dashboards/
│   │   │   └── grafana.json
│   │   └── alerts/
│   │       └── alerts.yaml
│   │
│   └── data/
│       ├── datasets/
│       │   └── eval_dataset.json
│       └── embeddings/
│           └── sample_embeddings.npy
│
├── tests/
│   ├── unit/
│   │   └── test_agent.py
│   ├── integration/
│   │   └── test_rag_pipeline.py
│   ├── e2e/
│   │   └── test_api_flow.py
│   └── eval_tests/
│       └── test_quality_metrics.py
│
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
├── docs/
│   ├── adr/
│   ├── architecture/
│   └── diagrams/
└── README.md
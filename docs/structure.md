ai-platform/
├── ai_lint/                                     # линтеры для AI-кода
│   ├── runner.py
│   ├── config.yaml
│   └── rules/
│       ├── llm_usage.py
│       ├── tools_usage.py
│       ├── structure.py
│       └── observability.py
│
├── apps/                                        # execution layer: только запуск и маршрутизация, без бизнес-логики
│
│   ├── api/                                     # sync API: request → executor → response (low latency)
│   │   ├── main.py
│   │   └── dependencies.py                      # DI wiring для FastAPI (получение executor из container)
│
│   ├── api-async/                               # async API: принимает запрос и ставит задачу в очередь
│   │   ├── main.py
│   │   └── enqueue.py                           # логика постановки задач (job creation)
│
│   ├── worker/                                  # async execution: обработка задач из очереди
│   │   ├── main.py
│   │   └── consumer.py                          # подписка на очередь + dispatch в agent
│
│
├── services/                                    # core: чистая бизнес-логика (без внешних зависимостей)
│
│   ├── gateway/                                 # use-case слой: оркестрация сценариев (не HTTP!)
│   │   ├── handlers/
│   │   │   ├── query_handler.py                 # sync flow: пользовательский запрос → ответ
│   │   │   ├── async_handler.py                 # async flow: создание job
│   │   │   └── eval_handler.py                  # запуск evaluation pipeline
│   │   │
│   │   ├── schemas/
│   │   │   └── request_schema.py                # DTO/контракты входа (Pydantic)
│   │   │
│   │   └── orchestrator_facade.py               # упрощённый интерфейс к agent (скрывает сложность)
│
│   ├── orchestrator/                            # AI-ядро: LangGraph + управление выполнением
│   │   ├── graph/
│   │   │   ├── builder.py                       # сборка StateGraph (основная точка композиции)
│   │   │   ├── state.py                         # Typed state (весь state агента)
│   │   │   └── nodes/
│   │   │       ├── guardrail_node.py            # валидация входа / защита
│   │   │       ├── decision_node.py             # routing / branching логика
│   │   │       ├── llm_node.py                  # вызов LLM (через LLMPort)
│   │   │       ├── tool_node.py                 # вызов tools (через ToolPort)
│   │   │       └── eval_node.py                 # self-evaluation / reflection loop
│   │   │
│   │   ├── runtime/
│   │   │   ├── agent.py                         # главный entrypoint: run_agent()
│   │   │   ├── cache.py                         # caching policy (LLM/RAG)
│   │   │   ├── retry.py                         # retry / fallback стратегии
│   │   │   └── context_manager.py               # управление контекстом (tokens, history)
│   │   │
│   │   └── ports/                               # контракты взаимодействия с внешним миром
│   │       ├── llm_port.py                      # генерация текста / structured output
│   │       ├── tool_port.py                     # вызов инструментов (MCP)
│   │       ├── executor_port.py                 # sync vs async execution
│   │       └── telemetry_port.py                # логирование / метрики / трейсинг
│   
│   ├── integrations/                            # внешний мир (НЕ tools!)
│   │   ├── ports/
│   │   │   ├── user_service_port.py             # контракт: получение пользователя
│   │   │   ├── billing_service_port.py          # платежи / баланс
│   │   │   └── notification_port.py             # email / sms / push
│   │   │
│   │   ├── services/
│   │   │   ├── user_service.py                  # retry / mapping / fallback
│   │   │   └── billing_service.py
│   │   │
│   │   └── schemas/
│   │       └── external_schema.py               # DTO внешних систем
│   
│   ├── tools/                                   # доменная логика инструментов (НЕ транспорт!)
│   │   ├── registry/
│   │   │   └── tool_registry.py                 # реестр доступных tools + версии
│   │   │
│   │   ├── contracts/
│   │   │   ├── rag_v1.py                        # строгие схемы вход/выход
│   │   │   ├── db_v1.py
│   │   │   └── external_api_v1.py
│   │   │
│   │   ├── implementations/
│   │   │   ├── rag_tool.py                      # orchestration RAG внутри tool
│   │   │   ├── db_tool.py                       # безопасный доступ к БД
│   │   │   └── external_api_tool.py             # интеграции
│   │   │
│   │   └── executor.py                          # локальный вызов tools (без сети)
│
│   ├── rag/                                     # knowledge layer: работа с данными
│   │   ├── ingestion/
│   │   │   ├── loaders.py                       # загрузка данных (PDF, HTML, etc.)
│   │   │   ├── chunking.py                      # разбиение на чанки
│   │   │   └── embeddings.py                    # генерация embeddings
│   │   │
│   │   ├── retrieval/
│   │   │   ├── retriever.py                     # поиск по vector DB
│   │   │   ├── reranker.py                      # улучшение релевантности
│   │   │   └── query_rewrite.py                 # переписывание запроса
│   │   │
│   │   ├── storage/
│   │   │   ├── vector_store.py                  # доступ к vector DB
│   │   │   └── metadata_store.py                # метаданные (Postgres)
│   │   │
│   │   └── ports/
│   │       └── rag_port.py                      # контракт для orchestrator
│
│   ├── evaluation/                              # оценка качества (offline/online)
│   │   ├── pipelines/
│   │   │   ├── ragas_pipeline.py                # стандартные метрики RAG
│   │   │   └── custom_metrics.py                # доменные метрики
│   │   │
│   │   ├── runner/
│   │   │   └── evaluation_runner.py             # orchestration eval запусков
│   │   │
│   │   └── datasets/
│   │       └── sample_dataset.json              # эталонные данные
│
│   └── features/                                # feature flags / A-B тесты / rollout
│       ├── flags/
│       │   └── model_flags.py                   # переключение моделей/поведения
│       │
│       └── experiments.py                       # A/B логика
│
│
├── adapters/                                    # инфраструктура: реализации портов
│
│   ├── api/                                     # HTTP слой (FastAPI)
│   │   ├── routes.py                            # endpoint’ы → handlers
│   │   └── middleware/
│   │       ├── auth.py                          # аутентификация
│   │       ├── rate_limit.py                    # защита от перегрузки
│   │       └── tracing.py                       # trace_id propagation
│
│   ├── integrations/                            # реализации внешних API
│   ├── http/
│   │   ├── user_service_http_adapter.py
│   │   └── billing_http_adapter.py
│   │
│   ├── grpc/
│   │   └── user_service_grpc_adapter.py
│   │
│   └── mocks/
│       └── user_service_mock.py                # для тестов
│
│   ├── llm/
│   │   ├── openai_adapter.py                    # OpenAI реализация
│   │   ├── anthropic_adapter.py
│   │   ├── gigachat_adapter.py
│   │   └── routing_adapter.py                   # выбор модели (cost/latency)
│
│   ├── tools/
│   │   ├── inprocess_adapter.py                 # локальный вызов tools
│   │   └── http_adapter.py                      # удалённый MCP-like вызов
│
│   ├── queue/
│   │   ├── kafka_adapter.py                     # event-driven execution
│   │   └── celery_adapter.py                    # task queue вариант
│
│   ├── storage/
│   │   ├── postgres_adapter.py                  # OLTP
│   │   ├── ignite_adapter.py                    # cache / rate limit
│   │   └── pinecone_adapter.py                  # pinecone
│       └── pinecone_adapter.py                  # pinecone
│
│   ├── telemetry/
│   │   ├── opentelemetry_adapter.py             # tracing
│   │   ├── logging_adapter.py                  # structured logs
│   │   └── metrics_adapter.py                  # Prometheus/Grafana
│
│   └── executor/                                # стратегии выполнения
│       ├── sync_executor.py                     # прямой вызов agent
│       └── async_executor.py                    # через очередь
│
│
├── platform/                                    # shared: переиспользуемые модули
│
│   ├── llm/
│   │   ├── routing.py                           # стратегия выбора модели
│   │   └── cost_control.py                      # лимиты и оптимизация стоимости
│
│   ├── prompts/
│   │   ├── registry.py                          # управление prompt версиями
│   │   └── versions/
│   │       ├── v1.py
│   │       └── v2.py
│
│   ├── schemas/                                 # общие контракты
│   │   ├── api_schema.py
│   │   ├── tool_schema.py
│   │   └── event_schema.py
│
│   └── sdk/                                     # внутренние клиенты (для сервисов)
│       ├── tool_client.py
│       ├── rag_client.py
│       └── eval_client.py
│
│
├── container/                                   # composition root (единственное место DI)
│   ├── container.py                             # build_container()
│   ├── providers.py                             # фабрики зависимостей
│   └── config.py                                # env → typed config
│
│
├── infra/                                       # инфраструктура и деплой
│   ├── docker/
│   │   └── Dockerfile.api
│   │
│   ├── k8s/
│   │   └── deployment.yaml
│   │
│   ├── terraform/
│   │   └── main.tf
│   │
│   └── environments/
│       ├── local/
│       │   └── .env
│       ├── staging/
│       │   └── .env
│       └── prod/
│           └── .env
│
│
├── observability/                               # мониторинг и алерты
│   ├── tracing/
│   │   └── opentelemetry.yaml
│   ├── metrics/
│   │   └── prometheus.yaml
│   ├── dashboards/
│   │   └── grafana.json
│   └── alerts/
│       └── alerts.yaml
│
│
├── data/                                        # данные (не код!)
│   ├── datasets/
│   │   └── eval_dataset.json
│   └── embeddings/
│       └── sample_embeddings.npy
│
│
├── tests/                                       # тестирование всех уровней
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
└── README.md
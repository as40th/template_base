# Запуск лиинтеров

## .pre-commit-config.yaml
- repo: local
  hooks:
    - id: ai-runtime-lint
      name: AI Runtime Lint
      entry: python ai_lint/runner.py
      language: system

## Github Actions
```yaml
- name: AI Runtime Lint
  run: python ai_lint/runner.py
```

# Настройка AI-окружения:
- Agentic IDE либо обычная IDE + agentic CLI
- Структура сервиса
- ADR
- runtime-контракты 
    - для работы с AI - ai-runtime-contract
    - можно добавить контракты для работы с Kafka / DB и т.д.
- rules для AI-кодера
- AI-линтеры для контроля выполнения требований
- TODO self-consistence / self-healing механизмы
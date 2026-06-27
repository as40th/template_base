# AI-окружение настроено для следующих инструментов:
  - Cursor
  - Devin (ex-Windsurf)
  - Gigacode

---

# ДЕКЛАРАТИВНЫЕ КОНФИГУРАЦИИ

ADR (Почему архитектура устроена именно так)
Structure (Где что лежит)
Rules (Что нельзя нарушать, что следует соблюдать)
Skills (Как следует выполнять задачу)
Hooks
Subagents 
Workflows

---

## ADR (Architecture Decision Records)

Это документы, в которых описываются архитектурные решения, принятые в проекте (почему сделано так, а не по другому).
Размещаются в каталоге `docs/adr/`.

---

## ARCHITECTURE (структура каталогов, data-flow)

Это документы, в которых описываются структура проекта и где что лежит. 
Описывается data-flow, то есть как данные проходят через систему.
Размещаются в каталоге `docs/architecture/`.

---

## RULES:

ПРАВИЛА (RULES) - Это ограничения и требования, которые должны соблюдаться при выполнении задач.
В зависимости от инструмента правила могут настраиваемыми (например, в Cursor можно добавлять условия применения правил).

Базовые наборы правил для AI-ассистента размещаются в каталогах в зависимости от используемого инструмента:

- **Cursor** - в каталоге `.cursor/rules/`
- **Devin (ex-Windsurf)** - в каталоге `.windsurf/rules/`
- **Gigacode** - в каталоге `.gigacode/rules/`

---

## SKILLS:

НАВЫКИ (SKILLS) - Это описание последовательности действий, которые должен выполнить AI-ассистент для выполнения задачи. Сделай то-то и то-то. 
ВАЖНО! НАВЫКИ не должны содержать ограничений и требований, они должны описывать только последовательность действий. Иначе они начинают дублировать RULES.

Базовые наборы навыков для AI-ассистента размещаются в каталогах в зависимости от используемого инструмента:

- **Cursor** - в каталоге `.cursor/skills/`
- **Devin (ex-Windsurf)** - в каталоге `.windsurf/skills/`
- **Gigacode** - в каталоге `.gigacode/skills/`

---

## SUBAGENTS:

Субагенты - это специальные агенты, которые выполняют определенные задачи в рамках основного агента, но используют свой контекст, не переполняя контекст основного агента.
Простая аналогия - это как один метод вызывает другой метод и получает результат для дальнейшей обработки.
Субагенты можно вызывать отдельно вручную из консоли командой `/test-generator напиши e2e тест. Используй testcontainers-python и respx`
`В Cursor субагенты могут настраиваться (синхронный/асинхронный режимы выполнения, какую модель использовать)`

Базовые наборы субагентов для AI-ассистента размещаются в каталогах в зависимости от используемого инструмента:

- **Cursor** - в каталоге `.cursor/agents/`
- **Devin (ex-Windsurf)** - в каталоге `.windsurf/workflows/` (в Devin нет субагентов, только workflows)
- **Gigacode** - в каталоге [дописать путь]

---

# ПРОГРАММНЫЕ КОНФИГУРАЦИИ

## MCP-сервер (улучшение качества работы AI-ассистента)
  - Требуется установить node.js для использования менеджера пакетов npm

  | MCP сервер              | Назначение                                   | Польза для AI-ассистента                                                             |  Ссылки                                        |
  | ----------------------- | ---------------------------------------------| ------------------------------------------------------------------------------------ | -----------------------------------------------|
  | **Context7**            | Актуальная документация библиотек и SDK      | Даёт свежий API, примеры кода и версии библиотек. Устраняет устаревшие знания модели | https://context7.com/docs/overview             |

## Хуки (pre-commit, post-commit, pre-push, post-push)

Базовый набор хуков для AI-ассистента размещается в каталоге [дописать путь]
Пока не релизованы

- **pre-commit** - проверка кода перед коммитом
- **post-commit** - автоматическое исправление кода после коммита
- **pre-push** - проверка кода перед пушем
- **post-push** - автоматическое исправление кода после пуша

---

# РАСШИРЕНИЯ:

- Pylance (hits, navigaton, type-checking)
- Ruff (linter + formatter (codestyle))

---

# ПРЕРЕКВИЗИТЫ

## Подключение к репозиториям

- Основной индекс `sberosc.sigma.sbrf.ru`
- Дополнительный индекс `nexus-ci.delta.sbrf.ru` (опционально)

- Получить токен для SberOSC, если еще нет (https://sberosc.sigma.sbrf.ru/dashboard/login/?next=/dashboard/ -> ПРОФИЛЬ -> Выпустить Токен)
- Подключение к Nexus возможно по кредам персональной УЗ сигмы

## uv

- Установи менджер uv
  Windows: 
  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

  Linux:
  ```
  Добавить
  ```    

- Создай ~\uv\uv.toml
- Пропиши путь до файла в переменную окружения UV_CONFIG_FILE
- Ребутни IDE
- Пропиши в uv.toml индексы (ниже пример для Сбера)
  ```toml
  native-tls = true

  [[index]]
  url = "https://token:<sberosc_token>@sberosc.sigma.sbrf.ru/repo/pypi/simple"
  default = true

  [[index]]
  url = "https://<login>:<password>@nexus-ci.delta.sbrf.ru/repository/pypi-release/simple"
  ```
- Установи Python:
  ```
  uv python install
  ```

- Запусти команду (будет создан venv и uv.lock)
  ```
  uv sync --group dev
  ```


## Node.js

- Установи node.js для использования менеджера пакетов npm
- Windows / Linux: скачай оф установщик с `https://nodejs.org/en/download`

## MCP-сервер Context7
- Это важный MCP-сервер из минимального набора MCP для AI-ассистента.
- Получи API-key для Context7: `https://context7.com/dashboard`
- Добавь системную переменную `CONTEXT7_API_KEY` и запиши в нее полученный API-key
- Готовые конфиги для MCP по stdin и http/SSE: `.cursor/mcp.json`, `.devin/mcp_config.json`. Для каждого AI-кодера - своя конфигурация, см. официальную документацию по настройке MCP для каждого агента.

### Cursor
- Поддерживается project-level
  Размещение в `.cursor/mcp.json`
- Поддерживается stdin и http/SSE режимы
- Активация через Cursor Settings - Tools & MCP's 

### Devin (ex-Windsurf)
- project-level не поддерживается, поэтому конфгигу размещаем в домашней директории пользователя (для Windows):
  `%USER%\.codeium\windsurf\mcp_config.json` или в `"%USER%\AppData\Roaming\devin\config.json"`
- На момент написания этого README не поддерживается режим stdin - только http/SSE
- Активация через Devin Settings - Devin Local - MCP servers

### Gigacode
- Gigacode не поддерживает project-level конфигурацию, поэтому конфига размещается в домашней директории пользователя (для Windows):
  `"%USER%AppData\Roaming\Code\User\globalStorage\gigacode.gigacode-vscode\settings\mcp_settings.json"`
- Режим stdin поддерживается
- Активация через Gigacode - Settings - Integrations & MCP

---

# ЛОКАЛЬНЫЙ ЗАПУСК

API:
```
uv run uvicorn src.apps.sync.main:app --reload
```

---

# ПРИМЕР ЗАПРОСА
```
curl -X POST http://localhost:8000/product-definition/api/v1/execute \
  -H "Content-Type: application/json" \
  -d '{"context_id":"ctx-1","task_id":"task-1","user_message":"потерял карту","is_initial":true}'
```

---

# ТЕСТИРВОАНИЕ

Тесты генерируем ТОЛЬКО ручным запуском субагента `test-generator` после проверки кода и внесения всех необходимых правок.
# Gos Tender Project (AdequacyOFF)

### Включает в себя 2 проекта:
- **Agents** ([_gosplan-agents_](https://github.com/AdequacyOFF/gosplan-agents))
- **Front** ([_GosLance_](https://github.com/AdequacyOFF/GosLance))

### Для проверки:

1. [**Поднятый функционирующий фронт**](https://gos-lance.ad-off.digital/)

    *Настроен CI из [gitlab](https://gitlab.ad-off.digital/other/GosLance)
2. Ссылки на развернутые агенты:
    - [Агент для составления профиля](https://31fd7d3f-2580-4179-b86a-3b5125118293-agent.ai-agent.inference.cloud.ru)
    - [Агент для выбора заказов](https://25855856-ed62-4327-8321-92831b4810bd-agent.ai-agent.inference.cloud.ru)
3. Проекты готовы к работе в среде **docker compose** - **_selfhosted_**
4. Также каждый проект имеет возможность локального запуска
---
## Краткая инструкция по установке, конфигурации и запуску
## Agents (Docker, локально)
1. **Требования**

   * Docker + buildx
   * (Linux/WSL2) желательно, т.к. ниже используется `--network host`

2. **Поднять PostgreSQL**

    ```bash
    docker compose -f Agents/db/docker-compose.yaml up -d
    ```

3. **Подготовить env-файлы**

    Порт и host можно менять — ниже типовая раскладка “всё на localhost”.
    
    **env/db.env**
    
    ```env
    DB_HOST=127.0.0.1
    DB_PORT=5432
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=postgres
    ```
    
    **env/db-mcp.env**
    
    ```env
    DB_HOST=127.0.0.1
    DB_PORT=5432
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_MCP_HOST=0.0.0.0
    DB_MCP_PORT=28001
    LOG_LEVEL=INFO
    ```
    
    **env/codes-mcp.env**
    
    ```env
    MCP_HOST=0.0.0.0
    MCP_PORT=28002
    LOG_LEVEL=INFO
    ```
    
    **env/gosplan-mcp.env**
    
    ```env
    MCP_HOST=0.0.0.0
    MCP_PORT=28003
    LOG_LEVEL=INFO
    GOSPLAN_BASE_URL=https://v2test.gosplan.info
    GOSPLAN_TIMEOUT=20
    GOSPLAN_PURCHASES_LIMIT=9
    ```
    
    **env/agent-profiler.env**
    
    ```env
    LLM_MODEL=hosted_vllm/Qwen/Qwen3-14B-AWQ
    LLM_API_BASE=http://127.0.0.1:28000/v1
    LLM_API_KEY=CHANGE_ME
    
    DB_MCP_URL=http://127.0.0.1:28001
    CODES_MCP_URL=http://127.0.0.1:28002
    
    AGENT_HOST=0.0.0.0
    AGENT_PORT=8001
    LOG_LEVEL=INFO
    ```
    
    **env/agent-purchaser.env**
    
    ```env
    LLM_MODEL=hosted_vllm/Qwen/Qwen3-14B-AWQ
    LLM_API_BASE=http://127.0.0.1:28000/v1
    LLM_API_KEY=CHANGE_ME
    
    DB_MCP_URL=http://127.0.0.1:28001
    GOSPLAN_MCP_URL=http://127.0.0.1:28003
    
    AGENT_HOST=0.0.0.0
    AGENT_PORT=8003
    LOG_LEVEL=INFO
    ```

4. **Собрать образы**
    
    ```bash
    cd db-mcp && docker buildx build --platform linux/amd64 -t db-mcp -f Agents/Dockerfile ..
    ```
    
    ```bash
    cd codes-mcp && docker buildx build --platform linux/amd64 -t codes-mcp -f Agents/Dockerfile ..
    ```
    
    ```bash
    cd gosplan-mcp && docker buildx build --platform linux/amd64 -t gosplan-mcp -f Agents/Dockerfile ..
    ```
    
    ```bash
    cd agent-profiler && docker buildx build --platform linux/amd64 -t agent-profiler -f Agents/Dockerfile ..
    ```
    
    ```bash
    cd agent-purchaser && docker buildx build --platform linux/amd64 -t agent-purchaser -f Agents/Dockerfile ..
    ```

5. **Запустить сервисы**
    
    ```bash
    docker run --rm --network host --env-file Agents/env/db-mcp.env db-mcp
    ```
    
    ```bash
    docker run --rm --network host --env-file Agents/env/codes-mcp.env codes-mcp
    ```
    
    ```bash
    docker run --rm --network host --env-file Agents/env/gosplan-mcp.env gosplan-mcp
    ```
    
    ```bash
    docker run --rm --network host --env-file Agents/env/agent-profiler.env agent-profiler
    ```
    
    ```bash
    docker run --rm --network host --env-file Agents/env/agent-purchaser.env agent-purchaser
    ```

### MCP-сервисы (инструменты)

* `http://127.0.0.1:28001/mcp` — db-mcp
* `http://127.0.0.1:28002/mcp` — codes-mcp
* `http://127.0.0.1:28003/mcp` — gosplan-mcp

У MCP сервисов также есть `/health` и `/metrics` (удобно для диагностики и мониторинга).

### A2A-агенты (диалог)

* `http://127.0.0.1:8001/.well-known/agent-card.json` — CompanyProfiler
* `http://127.0.0.1:8003/.well-known/agent-card.json` — PurchaseMatcher

---
## Front
1. **Требования**

   Docker и Docker Compose (для запуска в контейнерах)

2. **Настройка переменных окружения**
    - Создать файл _.env_
         ```bash
         cp Front/.env.example Front/.env
         ```
    - При необходимости изменить _baseUrl`ы_ для связи с агентами:
   
      (**VITE_PROFILE_AGENT_BASE_URL** и **VITE_EXCHANGE_AGENT_BASE_URL**)


3. **Режим разработки (Docker с hot reload)**
    
    ```bash
    docker compose -f Front/docker-compose.dev.yml up
    ```
    Приложение будет доступно по адресу: http://localhost:5173

4. **Производственный режим (Docker)**
    
    ```bash
    docker compose -f Front/docker-compose.yml up -d
    ```
    Приложение будет доступно по адресу: http://localhost:3030


**_P.S. Подробнее о работе и вариантах развертывания в README.md каждого проекта_**
# ──────────────────────────────────────────────────────────────────────────────
# ReAct Agent — Makefile
# ──────────────────────────────────────────────────────────────────────────────

IMAGE_NAME  ?= react-agent
IMAGE_TAG   ?= latest
CONTAINER   ?= react-agent
PORT        ?= 8080
MCP_HOST    ?= host.docker.internal
MCP_PORT    ?= 8000
ENV_FILE    ?= .env

.PHONY: help install dev build run stop logs shell test clean

# ── Help ───────────────────────────────────────────────────────────────────────
help:   ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | \
	    awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ── Local development ──────────────────────────────────────────────────────────
install:   ## Install dependencies with uv
	uv sync

dev:   ## Run the server locally with hot-reload (reads .env automatically)
	uv run uvicorn app.main:app --host 0.0.0.0 --port $(PORT) --reload

lint:   ## Lint with ruff
	uv run ruff check app/

fmt:   ## Format with ruff
	uv run ruff format app/

# ── Docker ─────────────────────────────────────────────────────────────────────
build:   ## Build the Docker image
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

run:   ## Run the container (builds first if needed)
	@if [ ! -f $(ENV_FILE) ]; then \
	    echo "⚠️  $(ENV_FILE) not found. Copy .env.example to .env and fill in your keys."; \
	    exit 1; \
	fi
	docker run -d \
	    --name $(CONTAINER) \
	    --env-file $(ENV_FILE) \
	    -e MCP_SERVER_URL=http://$(MCP_HOST):$(MCP_PORT) \
	    -p $(PORT):8080 \
	    --add-host=host.docker.internal:host-gateway \
	    $(IMAGE_NAME):$(IMAGE_TAG)
	@echo "✅  Container started. API → http://localhost:$(PORT)"
	@echo "    Logs: make logs"

stop:   ## Stop and remove the container
	docker stop $(CONTAINER) 2>/dev/null || true
	docker rm   $(CONTAINER) 2>/dev/null || true

logs:   ## Tail container logs
	docker logs -f $(CONTAINER)

shell:   ## Open a shell inside the running container
	docker exec -it $(CONTAINER) /bin/bash

# ── Testing ────────────────────────────────────────────────────────────────────
test:   ## Send a sample query (requires curl + jq + a running server)
	@echo "Sending test query to http://localhost:$(PORT)/query …\n"
	@curl -sN -X POST http://localhost:$(PORT)/query \
	    -H "Content-Type: application/json" \
	    -d '{"query": "What tools do you have available?"}' \
	| while IFS= read -r line; do \
	    echo "$$line"; \
	done

health:   ## Check server health
	@curl -s http://localhost:$(PORT)/health | python3 -m json.tool

tools:   ## List tools available to the agent
	@curl -s http://localhost:$(PORT)/tools | python3 -m json.tool

# ── Cleanup ────────────────────────────────────────────────────────────────────
clean:   ## Remove the Docker image and container
	$(MAKE) stop
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG) 2>/dev/null || true

# ── Compose shortcut (optional) ────────────────────────────────────────────────
up:   ## docker compose up (if docker-compose.yml exists)
	docker compose up --build -d

down:   ## docker compose down
	docker compose down

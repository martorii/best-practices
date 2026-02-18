# Makefile for Chat Assistant System

.PHONY: help build up down restart logs test clean

# Default target
help:
	@echo "Chat Assistant System - Available Commands"
	@echo "=========================================="
	@echo ""
	@echo "  make build      - Build all Docker images"
	@echo "  make up         - Start all services"
	@echo "  make down       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make logs       - View logs from all services"
	@echo "  make test       - Run system tests"
	@echo "  make clean      - Remove containers, volumes, and images"
	@echo "  make shell-backend    - Open shell in backend container"
	@echo "  make shell-frontend   - Open shell in frontend container"
	@echo "  make shell-mcp        - Open shell in MCP server container"
	@echo ""

# Build all services
build:
	@echo "🔨 Building Docker images..."
	docker compose build

# Start all services
up:
	@echo "🚀 Starting services..."
	docker compose up -d
	@echo ""
	@echo "✅ Services started!"
	@echo "Frontend: http://localhost:8501"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

# Stop all services
down:
	@echo "🛑 Stopping services..."
	docker compose down

# Restart all services
restart:
	@echo "🔄 Restarting services..."
	docker compose restart

# View logs
logs:
	docker compose logs -f

# Run tests
test:
	@echo "🧪 Running tests..."
	@./test.sh

# Clean everything
clean:
	@echo "🧹 Cleaning up..."
	docker compose down -v --rmi all

# Shell access
shell-backend:
	docker compose exec backend bash

shell-frontend:
	docker compose exec frontend bash

shell-mcp:
	docker compose exec mcp-server bash

# Development mode with hot reload
dev:
	@echo "🔧 Starting in development mode..."
	docker compose -f docker compose.yml -f docker compose.dev.yml up

# Production build
prod:
	@echo "🏭 Building for production..."
	docker compose -f docker compose.yml -f docker compose.prod.yml up -d

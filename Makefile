.PHONY: help dev down build test lint format clean install check-lua rag-demo rag-rebuild serve check info llm-demo llm-test llm-config ui ui-install

# Default target
help:
	@echo "═══════════════════════════════════════════════════════════════"
	@echo "  Isaac AI Agent - The Binding of Isaac Mod Code Generator"
	@echo "═══════════════════════════════════════════════════════════════"
	@echo ""
	@echo "🚀 MAIN COMMANDS:"
	@echo "  make dev              Start development Docker environment"
	@echo "  make serve            Start FastAPI server (http://localhost:8000/docs)"
	@echo "  make install          Install dependencies"
	@echo ""
	@echo "🔨 BUILD & TEST:"
	@echo "  make build            Build Lua artifacts"
	@echo "  make test             Run unit tests"
	@echo "  make lint             Code linting"
	@echo "  make format           Auto format code with Black"
	@echo "  make check            Run all checks"
	@echo ""
	@echo "🔍 RAG SYSTEM (NEW!):"
	@echo "  make rag-demo         Run RAG system demonstration"
	@echo "  make rag-rebuild      Rebuild FAISS vector index"
	@echo "  make rag-stats        Show RAG system statistics"
	@echo ""
	@echo "🤖 MULTI-LLM SYSTEM (NEW!):"
	@echo "  make llm-demo         Run multi-LLM demonstration"
	@echo "  make llm-test         Test LLM provider configuration"
	@echo "  make llm-config       Show current LLM configuration"
	@echo ""
	@echo "🖥️  DESKTOP GUI (NEW!):"
	@echo "  make ui               Launch the PyQt6 desktop application"
	@echo "  make ui-install       Install GUI dependencies"
	@echo ""
	@echo "📚 API INTEGRATION (NEW!):"
	@echo "  make test-api         Test API integration workflow"
	@echo ""
	@echo "✅ VALIDATION:"
	@echo "  make check-lua        Validate Lua code with luacheck"
	@echo ""
	@echo "🧹 CLEANUP:"
	@echo "  make clean            Clean build artifacts"
	@echo "  make down             Stop Docker containers"
	@echo ""
	@echo "📊 INFO:"
	@echo "  make info             Show project statistics"
	@echo ""

# Development environment
dev:
	@echo "🚀 Starting development environment..."
	docker-compose up -d python
	docker-compose exec python bash

dev-background:
	@echo "🚀 Starting development environment (background)..."
	docker-compose up -d

# Docker-based UI + API
docker-up:
	@echo "🐳 Starting UI (8080) + API (8000)..."
	docker-compose up -d
	@echo "✅ UI: http://127.0.0.1:8080"
	@echo "✅ API: http://127.0.0.1:8000/docs"

docker-down:
	@echo "🛑 Stopping all Docker services..."
	docker-compose down

# Stop containers
down:
	@echo "🛑 Stopping containers..."
	docker-compose down

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	uv sync

# Build mod artifacts
build: clean
	@echo "📦 Pre-caching embedding model (sentence-transformers/all-MiniLM-L6-v2)..."
	@python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')" 2>/dev/null || echo "⚠️  Model cache skipped (no network?)"
	@echo "🔨 Building mod artifacts..."
	python -m isaac_agent.build

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v --cov=src

# Lint code
lint:
	@echo "🔍 Linting Python code..."
	ruff check src/ tests/
	@echo "✅ Python linting complete"
	@echo ""
	@echo "🔍 Checking type hints..."
	mypy src/ --ignore-missing-imports

# Format code
format:
	@echo "🎨 Formatting code with Black..."
	black src/ tests/ --line-length=100
	@echo ""
	@echo "🔧 Sorting imports with ruff..."
	ruff check src/ tests/ --fix

# Validate Lua
check-lua:
	@echo "✔️  Validating Lua code..."
	find mods -name "*.lua" -type f | xargs luacheck --std awesome
	@echo "✅ Lua validation complete"

# Docker Lua validation
check-lua-docker:
	@echo "✔️  Validating Lua code with Docker..."
	docker-compose run lua-validator

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleaned!"

# Run all checks
check: lint test check-lua
	@echo ""
	@echo "✅ All checks passed!"

# Generate sample mods
sample:
	@echo "📝 Generating sample mods..."
	python -m isaac_agent.examples.generate_samples

# Start development server (for API endpoint)
serve:
	@echo "🌐 Starting FastAPI server..."
	uv run uvicorn isaac_agent.api:app --reload --host 0.0.0.0 --port 8000

# Watch mode for development
watch:
	@echo "👀 Watching for changes..."
	watchfiles "make test" src/

# Full setup
setup: clean install build
	@echo ""
	@echo "✅ Full setup complete!"
	@echo "Run 'make dev' to start development environment"

# Show project info
info:
	@echo "📊 Project Statistics:"
	@echo ""
	@echo "  Python files:"
	find src/ -name "*.py" | wc -l
	@echo ""
	@echo "  Lines of Python code:"
	find src/ -name "*.py" -exec wc -l {} + | tail -1
	@echo ""
	@echo "  Lua templates:"
	grep -c "\".*\":" src/isaac_agent/templates/lua_skeletons.py || echo "0"
	@echo ""

# RAG System Commands
rag-demo:
	@echo "🔍 Running RAG System Demo..."
	python demo_rag.py

rag-rebuild:
	@echo "🔨 Rebuilding FAISS vector index..."
	python demo_rag.py --rebuild --stats-only

rag-stats:
	@echo "📊 RAG System Statistics:"
	python demo_rag.py --stats-only

add-version-tags:
	@echo "🏷️  Backfilling DLC version tags into knowledge base..."
	python scripts/add_version_tags.py
	@echo "🔨 Rebuilding FAISS index with version metadata..."
	python demo_rag.py --rebuild --stats-only

# Multi-LLM System Commands
llm-demo:
	@echo "🤖 Running Multi-LLM Demo..."
	python demo_llm_providers.py

llm-config:
	@echo "⚙️  Current LLM Configuration:"
	python -c "from isaac_agent.config import settings; print(f'  Provider: {settings.llm_provider}'); print(f'  OpenAI Model: {settings.openai_model}'); print(f'  GLM Model: {settings.glm_model}'); print(f'  Deepseek Model: {settings.deepseek_model}'); print(f'  Temperature: {settings.temperature}'); print(f'  Max Tokens: {settings.max_tokens}')"

llm-test:
	@echo "🧪 Testing LLM Providers..."
	python -m pytest tests/test_llm_factory.py -v

# API Integration Commands
test-api:
	@echo "📚 Testing API Integration Workflow..."
	python test_api_integration.py

ui:
	@echo "🖥️  Launching Isaac AI Agent GUI..."
	uv run python -m isaac_agent.ui.app

ui-install:
	@echo "📦 Installing GUI dependencies..."
	uv sync --extra gui

convert-api:
	@echo "🔄 Converting API documentation..."
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Usage: make convert-api FILE=your_api.json"; \
		echo "   Supported formats: json, csv, md"; \
		exit 1; \
	fi
	python scripts/api_converter.py "$(FILE)" converted_api.py

integrate-api:
	@echo "🔗 Integrating API documentation..."
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Usage: make integrate-api FILE=converted_api.py [REBUILD=true]"; \
		exit 1; \
	fi
	@if [ "$(REBUILD)" = "true" ]; then \
		python scripts/integrate_api.py "$(FILE)" --rebuild-index; \
	else \
		python scripts/integrate_api.py "$(FILE)"; \
		echo "💡 Run 'make integrate-api FILE=converted_api.py REBUILD=true' to rebuild index"; \
	fi

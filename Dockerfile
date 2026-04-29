# Isaac API Document Processor
FROM python:3.12-slim-bookworm
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY scripts/ ./scripts/
COPY docs/ ./docs/
COPY src/ ./src/

# Install Python dependencies using pip with mirrors
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    anthropic>=0.7.0 \
    pyyaml>=6.0 \
    loguru>=0.7.0

# Create output directory
RUN mkdir -p processed_docs

# Set environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEEPSEEK_API_BASE=https://api.deepseek.com

# Default command
CMD ["python", "scripts/document_processor.py"]


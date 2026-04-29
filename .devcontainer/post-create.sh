#!/bin/bash
set -e

echo "🚀 Setting up Isaac AI Agent development environment..."

# Update apt
apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    lua5.1 \
    clang-format \
    && rm -rf /var/lib/apt/lists/*

# Install uv if not present
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create virtual environment using uv
export PATH="/root/.cargo/bin:$PATH"
uv venv /workspace/.venv
source /workspace/.venv/bin/activate

# Install dependencies
uv sync

# Install luacheck for Lua validation
pip install luacheck

echo "✅ Environment setup complete!"
echo "📦 Installed packages:"
pip list

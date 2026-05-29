#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# 00_install_deps.sh - Part of the Hermes Control Plane Restore Workflow
# Installs OS packages and prepares the Python virtual environment for Composio.
# -----------------------------------------------------------------------------
set -euo pipefail

# Locate repo root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "📦 [1/3] Updating system and installing OS packages …"
if command -v apt-get &>/dev/null; then
    sudo apt-get update
    sudo xargs -a "${REPO_ROOT}/dependencies/apt-packages.txt" sudo apt-get install -y
else
    echo "⚠️  apt-get not found. Skipping system package installation."
    echo "Please ensure packages in ${REPO_ROOT}/dependencies/apt-packages.txt are installed."
fi

echo "📦 [2/3] Setting up Python virtual environment for Composio MCP …"
COMPOSIO_VENV_DIR="${HOME}/.hermes/mcp_servers/composio/venv"
mkdir -p "$(dirname "$COMPOSIO_VENV_DIR")"

# Use uv if available, otherwise fall back to venv
if command -v uv &>/dev/null; then
    echo "🚀 Using 'uv' for fast installation …"
    uv venv "$COMPOSIO_VENV_DIR"
    uv pip install -r "${REPO_ROOT}/dependencies/hermes-pip-requirements.txt" --python "$COMPOSIO_VENV_DIR/bin/python"
else
    echo "🐍 Using standard 'venv' …"
    python3 -m venv "$COMPOSIO_VENV_DIR"
    "$COMPOSIO_VENV_DIR/bin/pip" install --upgrade pip
    "$COMPOSIO_VENV_DIR/bin/pip" install -r "${REPO_ROOT}/dependencies/hermes-pip-requirements.txt"
fi

echo "📦 [3/3] Ensuring Node.js environment is ready …"
if command -v npm &>/dev/null; then
    echo "✅ Node.js $(node --version) and npm $(npm --version) found."
else
    echo "❌ Node.js/npm not found. Some MCP servers may fail to start."
fi

echo "✅ Dependencies installation complete."

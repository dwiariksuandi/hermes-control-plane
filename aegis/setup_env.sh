#!/usr/bin/env bash
set -euo pipefail

# Ensure uv is installed (Official Astral-sh pattern)
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source "$HOME/.cargo/env"
fi

# Create isolated venv at strict absolute path
uv venv /home/hiryu/.hermes/venv

# Install dependencies using official uv pip-compile/pip-sync pattern
/home/hiryu/.hermes/venv/bin/uv pip install -r /home/hiryu/.hermes/requirements.txt

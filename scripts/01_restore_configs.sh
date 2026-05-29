#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# 01_restore_configs.sh - Part of the Hermes Control Plane Restore Workflow
# Copies configuration files from the repo to ~/.hermes/ and ~.
# -----------------------------------------------------------------------------
set -euo pipefail

# Locate repo root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_HOME="${HOME}/.hermes"

echo "⚙️  [1/2] Restoring Hermes Agent configuration …"
mkdir -p "$(dirname "${HERMES_HOME}/mcp_servers/composio")"

# Main Hermes config.yaml (sanitized)
cp "${REPO_ROOT}/configs/hermes/config.yaml" "${HERMES_HOME}/config.yaml"
echo "  ✅ ${HERMES_HOME}/config.yaml"

# Composio MCP launcher script
mkdir -p "${HERMES_HOME}/mcp_servers/composio"
cp "${REPO_ROOT}/configs/hermes/mcp_servers/composio/run_server.py" \
   "${HERMES_HOME}/mcp_servers/composio/run_server.py"
echo "  ✅ ${HERMES_HOME}/mcp_servers/composio/run_server.py"

echo "⚙️  [2/2] Restoring shell configuration …"
# Backup existing files if they exist
for f in .bashrc .profile; do
    if [ -f "${HOME}/${f}" ] && ! cmp -s "${REPO_ROOT}/configs/shell/${f}" "${HOME}/${f}"; then
        cp "${HOME}/${f}" "${HOME}/${f}.backup-$(date +%Y%m%d-%H%M%S)"
        echo "  💾 Backed up existing ${f}"
    fi
done
cp "${REPO_ROOT}/configs/shell/.bashrc" "${HOME}/.bashrc"
cp "${REPO_ROOT}/configs/shell/.profile" "${HOME}/.profile"
echo "  ✅ ${HOME}/.bashrc"
echo "  ✅ ${HOME}/.profile"

echo "✅ Configuration restore complete."

#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# ONE-CLICK Hermes Control Plane Restore Script
# -----------------------------------------------------------------------------
set -euo pipefail

# ---- Resolve repo root ------------------------------------------------------
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "====================================================================="
echo "   🚀 HERMES CONTROL PLANE - RESTORE SEQUENCE"
echo "====================================================================="

# ---- 0. Pre-flight Checks ---------------------------------------------------
if [ -z "${COMPOSIO_API_KEY:-}" ]; then
    echo "❌ ERROR: COMPOSIO_API_KEY environment variable is not set."
    echo "Please set it before running this script:"
    echo "  export COMPOSIO_API_KEY=\"your_actual_key_here\""
    exit 1
fi

# ---- 1. Install dependencies ------------------------------------------------
echo ""
bash "${REPO_ROOT}/scripts/00_install_deps.sh"

# ---- 2. Install Hermes Agent ------------------------------------------------
echo ""
echo "🤖 [2/3] Installing Hermes Agent core …"
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# ---- 3. Restore configurations ----------------------------------------------
echo ""
bash "${REPO_ROOT}/scripts/01_restore_configs.sh"

# ---- Done -------------------------------------------------------------------
echo ""
echo "====================================================================="
echo " 🎉 RESTORE COMPLETE!"
echo "====================================================================="
echo "Your Hermes Agent is now identical to the target state, including:"
echo " - Custom 'Smart_Agent' personality & config"
echo " - Composio MCP server integration"
echo " - All necessary dependencies"
echo ""
echo "👉 NEXT STEPS:"
echo "1. Restart your terminal (or run: source ~/.bashrc)"
echo "2. Run 'hermes' to start the agent."
echo "====================================================================="

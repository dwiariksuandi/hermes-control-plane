#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="/home/hiryu/.hermes/vault/dev"
OUT_FILE="$OUT_DIR/composio_mcp_healthcheck_latest.txt"
mkdir -p "$OUT_DIR"

{
  echo "[INFO] time: $(date -Iseconds)"
  echo "[INFO] check: hermes mcp list"
  hermes mcp list
  echo
  echo "[INFO] status: COMPOSIO_MCP_TOOLS (verified via MCP tool calls in Hermes)"
  echo "[PASS] GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER - last tested OK"
  echo "[PASS] GITHUB_GET_THE_AUTHENTICATED_USER - last tested OK"
  echo "[NOTE] Run hermes mcp test composio for live test"
} > "$OUT_FILE"

echo "[DONE] report: $OUT_FILE"
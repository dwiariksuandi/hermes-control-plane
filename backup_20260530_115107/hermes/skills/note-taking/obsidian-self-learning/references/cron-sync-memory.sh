#!/bin/bash
# Hermes Obsidian Memory Sync Cron Job
# Syncs ~/.hermes/MEMORY.md and ~/.hermes/USER.md to vault

HERMES_HOME="/home/hiryu/.hermes"
VAULT="$HERMES_HOME/vault"

# Ensure vault directories exist
mkdir -p "$VAULT/memory"
mkdir -p "$VAULT/self-learning"

# Sync Hermes → Vault
if [ -f "$HERMES_HOME/MEMORY.md" ]; then
    cp "$HERMES_HOME/MEMORY.md" "$VAULT/MEMORY.md"
fi

if [ -f "$HERMES_HOME/USER.md" ]; then
    cp "$HERMES_HOME/USER.md" "$VAULT/USER.md"
fi

# Verify sync
echo "[$(date)] Obsidian Memory Sync:"
echo "  MEMORY.md: $( [ -f "$VAULT/MEMORY.md" ] && echo "OK" || echo "MISSING" )"
echo "  USER.md: $( [ -f "$VAULT/USER.md" ] && echo "OK" || echo "MISSING" )"
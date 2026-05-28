#!/usr/bin/env python3
"""
Vault bootstrap script for Hyper-Native v4.5 Orchestration.
Usage: uv run --with pyyaml scripts/bootstrap_vault.py
Creates agent silos, initializes manifest files, and writes protocol stubs.
"""
import json, os, sys
from pathlib import Path

VAULT = Path("/home/hiryu/.hermes/vault")
AGENTS = ["scout", "scribe", "reach", "dev"]
PROTOCOLS = {
    "ORCHESTRATOR-CONSTITUTION.md": """---
author: Orchestrator
status: active
timestamp: {ts}
tags: [constitution, operating-rules, v4.5, core-protocol]
---

# Permanent Operating Constitution (v4.5 Hyper-Native)

## 1. Execution & Tool Primitive Priority
- **FAST RETRIEVAL**: When querying past knowledge or analyzing Vault contents, MUST use `execute_code` with the `rg` binary.
- **FAST COMPUTE**: When running external Python modules or dependencies, MUST use `execute_code` wrapped with `uv run --with <package> <script.py>`.

## 2. Communication & Routing Paradigm
- Lead with the actionable result. Strip away conversational filler.
- Route tasks dynamically: delegate_task for parallel, ephemeral work; Kanban for durable, multi-step collaboration; cron with no_agent for recurring mechanical tasks.

## 3. Vault & Memory Persistence
- All durable facts, SOPs, and intelligence must be formatted as Markdown with YAML Frontmatter in the vault.

## 4. Safety & Redaction
- Ask explicit approval before hard-to-rollback actions.
- Never expose API keys. Rely on native Redaction Engine.
""",
}

def write_protocols():
    ts = "2026-05-27"
    for fname, body in PROTOCOLS.items():
        p = VAULT / fname
        if not p.exists():
            p.write_text(body.replace("{ts}", ts))
            print(f"Created {p}")

def create_silos():
    for agent in AGENTS:
        agent_dir = VAULT / agent
        agent_dir.mkdir(parents=True, exist_ok=True)
        manifest = agent_dir / f"{agent.upper()}-MANIFEST.json"
        if not manifest.exists():
            data = {
                "agent": agent.upper(),
                "status": "instantiated",
                "workspace": str(agent_dir),
                "timestamp": "2026-05-27"
            }
            manifest.write_text(json.dumps(data, indent=2))
            print(f"Created {manifest}")

def create_db():
    import sqlite3
    db = Path("/home/hiryu/.hermes/agent-logs.db")
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs (
            id TEXT PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            agent_name TEXT,
            task_summary TEXT,
            status TEXT,
            validation_status TEXT,
            artifact_path TEXT
        )
    """)
    conn.commit()
    conn.close()
    print(f"Ensured {db}")

if __name__ == "__main__":
    VAULT.mkdir(parents=True, exist_ok=True)
    write_protocols()
    create_silos()
    create_db()
    print("Vault bootstrap complete.")
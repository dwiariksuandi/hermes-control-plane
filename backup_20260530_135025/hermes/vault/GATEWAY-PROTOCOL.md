---
author: Orchestrator
status: active
timestamp: 2026-05-27
tags: [gateway, api-protocol, security, v4.5, orchestrator]
---

# Gateway Integration & API Surface Protocol (v4.5 Hyper-Native)

## 1. Exclusive Domain (Agent Dev)
- Only the Orchestrator or the Dev sub-agent are permitted to formulate external HTTP requests.
- Scout only consumes data (via web-scraping). Reach only plans strategies.
- When Dev needs to hit an API, use `execute_code` with ephemeral HTTP libraries (e.g., `uv run --with httpx script.py`).

## 2. Zero-Leakage Redaction
- Strict isolation of authentication tokens, API keys, and database credentials MUST be enforced.
- Credentials MUST NEVER be written into the vault/, passed in conversational context, or stored in Honcho memory.
- Rely solely on environment variables (os.environ) or the native Hermes Redaction Engine.

## 3. Gateway Handshake (Standardization)
- Before building an automated tool to fetch external data (e.g., Telegram, GitHub API), Dev must write a `gateway_spec.md` in `/home/hiryu/.hermes/vault/dev/` detailing the exact endpoint and payload structure for {OWNER}'s review.
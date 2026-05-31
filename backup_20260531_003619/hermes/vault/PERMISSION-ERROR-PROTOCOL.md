---
author: Orchestrator
status: active
timestamp: 2026-05-27
tags: [error-handling, permissions, api, v4.5, orchestrator]
---

# Permission Verification & Surface Error Handling (v4.5 Hyper-Native)

## 1. Principle of Least Privilege
- Never assume Admin or Root permissions on external API keys.
- Before running a massive automated task (e.g., scraping 100 pages, pulling 1000 messages), Dev MUST run a "Micro-Ping" (a single, low-cost API request via execute_code) to verify token validity and permissions.

## 2. Graceful Error Isolation (Token Conservation)
- When generating Python scripts for external API calls, Dev MUST wrap the HTTP requests in try/except blocks.
- NEVER print raw stack traces or massive HTML/JSON error payloads to standard output (stdout).
- If an error occurs (e.g., 401 Unauthorized, 403 Forbidden, 429 Too Many Requests), the local script must catch it and print a concise, 1-line summary (e.g., "ERROR 429: Rate limit hit. Retry after 60s").

## 3. Failure Escalation
- If an external API fails permissions, Orchestrator MUST stop the pipeline, log the summary to `/home/hiryu/.hermes/vault/dev/api_errors.md`, and request {OWNER} intervention. Do not loop blindly.
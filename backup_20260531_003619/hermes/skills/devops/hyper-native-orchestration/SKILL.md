---
name: hyper-native-orchestration
description: V4.5 Hyper-Native Orchestration framework for bootstrapping stateful, multi-agent environments with vault-based persistence and tool-optimized execution.
tags: [orchestrator, multi-agent, vault, uv, ripgrep, handoff-protocol]
---

# Hyper-Native Orchestration (v4.5)

Bootstrapping a stateful coordination process inside a containerized environment using a specialist fleet and structured vault persistence.

## 1. Environment Anchoring
Always verify the environment core root and available primitives before scaling operations.
- **Root**: Usually `~/.hermes/` or `/workspace/.hermes/`.
- **Vault**: Establish a centralized Markdown knowledge base (Obsidian compatible) at `HERMES_HOME/vault/`.
- **Binaries**: Ensure high-speed retrieval and compute tools are in PATH.
  - `uv`: For ephemeral Python execution (`uv run --with <package>`).
  - `rg`: For fast file/vault searching via `execute_code`.

## 2. Specialist Fleet
Deploy persistent specialist sub-agents with isolated vault silos:
- **Scout**: Research, web extraction, source validation. Workspace: `vault/scout/`.
- **Scribe**: Formatting, documentation, Obsidian graph integration. Workspace: `vault/scribe/`.
- **Reach**: Strategy, audience analytics, growth metrics. Workspace: `vault/reach/`.
- **Dev**: Scripts, automation, debugging, uv/rg operations. Workspace: `vault/dev/`.

## 3. Communication & Handoff
Sub-agents operate with **fresh context** (amnesia). Orchestrator must use the **Structured Handoff Brief** via `delegate_task`:
1. **TARGET**: Agent name.
2. **GOAL**: One sentence objective.
3. **CONTEXT**: Vital background + exact file paths.
4. **CONSTRAINTS**: Prohibited actions + mandatory tools (uv/rg).
5. **DELIVERABLE**: Expected format (usually Markdown with YAML frontmatter).
6. **RISK LEVEL**: Low/Medium/High.

## 4. File-Relay Pipeline
To conserve tokens, avoid passing full raw text in chat context. Use **File-Relay**:
- Scout writes `vault/scout/raw_brief.md`.
- Scribe reads path, writes `vault/scribe/final_artifact.md`.
- Reach reads path, writes `vault/reach/promo_plan.md`.
- Orchestrator verifies paths and reports final status.

## 5. Decision Tree for Execution
- **Simple sorting/retrieval**: `execute_code` (Python/rg).
- **Parallel/Fresh context**: `delegate_task`.
- **Multi-day/Multi-agent**: Kanban.
- **Recurring mechanical**: `cron` (no_agent mode).

## Support Files
- `templates/scout_raw_brief.md`: Starter template for Scout relay artifact (`raw_brief.md`). Copy and adapt per topic.
- `templates/scribe_final_artifact.md`: Starter template for Scribe relay artifact (`final_artifact.md`). Copy and adapt per topic.

## 6. Gateway & API Surface Protocol
Only Orchestrator or Dev may make external HTTP requests. Scout consumes data; Reach plans strategies.
- **Ephemeral HTTP**: Dev uses `uv run --with httpx script.py` for external API calls. No persistent HTTP libraries installed globally.
- **Zero-Leakage Redaction**: Never store credentials in vault, chat context, or memory. Use environment variables (`os.environ`) or the native Redaction Engine exclusively.
- **Gateway Spec**: Before automating external data fetches, Dev writes `gateway_spec.md` in `vault/dev/` detailing endpoint + payload for owner review.

## 7. Error Handling & Permission Verification
- **Micro-Ping**: Before large API operations, Dev runs a single low-cost request to validate token permissions. Never assume admin/root on external keys.
- **Graceful Error Isolation**: All HTTP scripts must wrap requests in try/except. Print concise 1-line summaries (e.g. "ERROR 429: Rate limit. Retry after 60s"), never raw stack traces or full payloads.
- **Failure Escalation**: Orchestrator stops the pipeline on permission failures, logs the summary to `vault/dev/api_errors.md`, and requests owner intervention. No blind retry loops.

## 8. Surface Isolation (Communication Discipline)
- **Single Pane of Glass**: The operator-facing chat surface (Telegram/CLI) is owned exclusively by the Orchestrator.
- **Silent Workers**: Sub-agents write outputs ONLY to their vault silos. No internal thought processes or raw tool outputs streamed to the operator.
- **Identity Prefix**: When a sub-agent is explicitly bridged (e.g., "Dev, explain this"), it MUST prefix every response with `[AGENT]:`. Orchestrator relays the prefixed output.

## 9. Activity Logging (Telemetry)
- **SQLite Database**: Maintain a lightweight, append-only log at `HERMES_HOME/agent-logs.db`.
- **Schema**: `activity_logs(id TEXT PK, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, agent_name TEXT, task_summary TEXT, status TEXT, validation_status TEXT, artifact_path TEXT)`.
- **Logging Rule**: Insert a row for every pipeline completion, handoff, artifact creation, or API error. Keep `task_summary` under 150 characters. Never log raw payloads, API keys, or full transcripts.

## 10. Obsidian GUI Provisioning
Provision the Obsidian AppImage for the operator without root:
1. Fetch the latest release from `obsidianmd/obsidian-releases` GitHub.
2. Filter for `x86_64` AppImage asset (`...x86_64...AppImage`).
3. Download to `~/.local/bin/obsidian`, `chmod +x`.
4. Do NOT attempt to launch — headless environments lack X11/Wayland.

## 11. Execution Integrity Loop (Hotfix Discipline)
When run incomplete or partially fails, orchestrator must self-report gap and immediately issue concrete hotfix plan.

1. **Declare partial state**: report exactly what succeeded vs pending.
2. **Hotfix plan**: enumerate remaining actions as explicit checklist.
3. **Execute with physical grounding**: apply file mutations and verification in one deterministic `execute_code` script when possible.
4. **Proof before success claim**: include physical `find`/`ls` output or DB row counts for claimed completion.
5. **Final schema lock**: if owner requests strict response schema, follow it exactly (field names/order).

## 12. Tactical Skill Lookup Rule
Before agent execution (Orchestrator, Scout, Dev), check `vault/skills/` and apply matching tactical protocol when applicable. This promotes SOPs from static guidance to executable instincts.

## Pitfalls
- **Amnesia**: Specialists don't remember previous turns. Pass ALL paths in the handoff.
- **Path Mismatch**: Always check if the environment root is `/workspace` or `~/.hermes` before hardcoding.
- **Token Inflation**: Passing large files via `read_file` into context is expensive. Use `rg` inside `execute_code` to filter before reading.
- **Wrong ARCH**: Obsidian release assets include both `arm64` and `x86_64` AppImages. Filter by architecture string or fallback to the generic `Obsidian-<ver>.AppImage` which is x86_64.
- **Premature success claim**: claiming complete before SOP patch/file-tree proof causes trust drift. Always verify physically first.
- **Config tail blind spot**: never conclude a key is absent from `config.yaml` without reading full file (or targeted search). `read_file` can truncate; verify with offset continuation or key search before proposing "add config" changes.
- **Credential gate handling**: when execution is blocked by missing token/CLI, report exact blocker + exact file/field to update, then pause. Do not continue with speculative mutations.

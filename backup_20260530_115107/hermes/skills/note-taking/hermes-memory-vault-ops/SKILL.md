---
name: hermes-memory-vault-ops
description: "Operate Hermes Agent memory as a structured Markdown/Obsidian vault: audit, initialize, verify, and keep claims grounded."
version: 1.0.0
author: Hermes Orchestrator
metadata:
  created_by: agent
  class: memory-vault-operations
---

# Hermes Memory Vault Operations

Use this skill when the user asks to audit, configure, improve, or verify Hermes Agent memory, Obsidian vault usage, Markdown vault structure, or durable note storage.

## Core rule

Do not claim Obsidian is the automatic Hermes memory backend unless `config.yaml` explicitly shows an Obsidian/provider integration. The built-in Hermes memory system, session DB, Markdown vault, and Obsidian note access are separate layers.

## Standard audit workflow

1. Resolve absolute paths only:
   - Hermes home: `/home/hiryu/.hermes`
   - Vault candidate: `/home/hiryu/.hermes/vault`
   - Env file: `/home/hiryu/.hermes/.env`
   - Config: `/home/hiryu/.hermes/config.yaml`
2. Inspect memory config in `config.yaml`:
   - `memory.memory_enabled`
   - `memory.user_profile_enabled`
   - `memory.provider`
   - `memory_monitor.enabled`
3. Resolve Obsidian vault path:
   - Prefer `OBSIDIAN_VAULT_PATH` in `/home/hiryu/.hermes/.env`.
   - If current process env does not show it, read `.env` directly; gateway restart may be needed before live env reload.
4. Verify vault identity:
   - Directory exists.
   - `.obsidian/` exists.
   - Markdown notes are readable/searchable.
5. Verify read/write with real evidence:
   - Write a temporary note under `/home/hiryu/.hermes/vault/memory/`.
   - Read it back.
   - Search for it.
   - Remove test note after proof.
6. Report exact status:
   - Automatic memory backend: yes/no/unknown.
   - Obsidian vault ready: yes/no.
   - Hermes file-tool access: pass/fail.
   - Gaps and next actions.

## Initialization workflow

1. Backup files before mutating existing config or notes.
2. Ensure vault directories exist:
   - `/home/hiryu/.hermes/vault/.obsidian`
   - `/home/hiryu/.hermes/vault/memory`
   - `/home/hiryu/.hermes/vault/logs`
   - `/home/hiryu/.hermes/vault/templates`
3. Add `OBSIDIAN_VAULT_PATH=/home/hiryu/.hermes/vault` to `/home/hiryu/.hermes/.env` if absent.
4. Create a dashboard note:
   - `/home/hiryu/.hermes/vault/00_Hermes_Dashboard.md`
5. Link or sync stable memory notes only if safe:
   - `/home/hiryu/.hermes/MEMORY.md`
   - `/home/hiryu/.hermes/USER.md`
   - `/home/hiryu/.hermes/vault/MEMORY.md`
   - `/home/hiryu/.hermes/vault/USER.md`

## AI-Centric Vault Patterns

When architecting a vault for autonomous agent operations, use these patterns to maximize context retrieval and human-agent collaboration:

1. **Mission Control Dashboard**: `00_Hermes_Dashboard.md`. Central hub for active goals, projects, and cron status.
2. **Decision Log**: `decisions/YYYY-MM-DD-<topic>.md`. Record why certain paths were taken to avoid repetition.
3. **Research Pipeline**: `research/`. Source-grounded notes with wikilinks to projects.
4. **Inbox Capture**: `inbox/`. Daily capture files for fast thought-dumping from chat.
5. **Evidence Ledger**: `logs/`. Durable proof of technical claims (exit codes, paths).
6. **Agent Silos**: Folders per sub-agent (e.g., `agents/scout/`) for isolated workstreams.

See `references/ai-centric-vault-architecture.md` for detailed structure.

## Pitfalls

- Obsidian CLI/version checks may launch GUI and hang in headless sessions. Prefer filesystem verification over GUI launch.
- `OBSIDIAN_VAULT_PATH` added to `.env` is not automatically visible inside already-running tool sandboxes. Read `.env` directly or restart gateway/session.
- A Markdown vault usable by the Obsidian skill is not the same thing as a configured Hermes memory provider.
- Do not create duplicate, stale memory sources without explaining sync/ownership.

## References

- `references/obsidian-vault-setup-2026-05-29.md` — concrete setup pattern from this environment.
- `references/ai-centric-vault-architecture.md` — patterns for Mission Control, Decision Logs, and Agent Silos.
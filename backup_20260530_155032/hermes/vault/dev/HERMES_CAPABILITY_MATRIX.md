# HERMES CAPABILITY MATRIX (v5.3 Context)

---

## 1. NATIVE CAPABILITIES (Hermes Agent Core)
*Built-in framework capabilities, active by default.*

| Category | Capability | Tools/Mechanisms | Status |
| :--- | :--- | :--- | :--- |
| **Execution** | Arbitrary shell execution | `terminal` (local, pty, background) | Active |
| **Filesystem** | CRUD, search, and patch operations | `read_file`, `write_file`, `patch`, `search_files` | Active |
| **Web/Network** | Network requests, HTML parsing, Browser automation | `web_extract`, `browser_navigate`, `browser_click`, etc. | Active |
| **Logic/Coding** | Sandboxed Python execution for data manipulation | `execute_code` | Active |
| **Orchestration** | Spawning sub-agents for parallel/isolated tasks | `delegate_task` | Active |
| **Scheduling** | Durable recurring/one-shot background tasks | `cronjob` | Active |
| **Context/Memory** | Semantic search of past sessions, durable KV store | `session_search`, `memory` | Active |
| **Gateway** | Cross-platform I/O (currently via Telegram) | `send_message` | Active |
| **Skills** | Procedural memory, custom workflows, predefined scripts | `skill_view`, `skill_manage`, `skills_list` | Active |

---

## 2. ADDED CAPABILITIES (Profile, Memory & SOUL.md Governance)
*Custom injected state defining current operational behavior.*

| Category | Capability | Mechanism / Source |
| :--- | :--- | :--- |
| **Strict Execution Safety** | VBC (Verification-Before-Completion) protocol | SOUL.md Law 4 & 9 |
| **Lateral Debugging** | Anti-loop logic (Pivot after 2 logic failures) | SOUL.md Law 5 |
| **Data Grounding** | Forcing large payloads to disk rather than chat output | SOUL.md Law 3 (`vault/`) |
| **Telemetry Injection** | Structured logging of orchestrator handoffs and states | SOUL.md Law 11 (`log_event.py`) |
| **Automated Backup** | Mandatory `.bak` retention before destructive mutation | SOUL.md Law 6 |
| **Bilingual Support** | Fallback to Indonesian for casual/praise responses | User Profile |
| **Terse Output Mode** | "Caveman" style (fragmented, no fluff, concise status) | User Profile |
| **Zero-Leak Redaction** | Strict credential/token masking in files and chat | SOUL.md Law 12 |

---

## 3. DISABLED / RESTRICTED CAPABILITIES
*Actions explicitly blocked or requiring explicit gating.*

| Restriction | Reason | Override Mechanism |
| :--- | :--- | :--- |
| **Relative Paths** | SOUL.md Law 2 | None. Absolute paths only. |
| **Interactive CLI** | SOUL.md Law 8 | Must use `-y` / `--no-interaction` flags. |
| **Unverified Claims** | SOUL.md Law 4 & 10 | Must provide exit code / file path / stdout proof. |
| **Simultaneous Exec+Report** | SOUL.md Law 9 (Phase 1 & Phase 2) | None (except READ class operations). |
| **Scope Creep** | SOUL.md Law 7 | Surface for approval if >20% task deviation. |
| **Raw Secret Handling** | SOUL.md Law 12 | Redacted to `****` or `[REDACTED]`. |

---

## 4. RISK LEVELS & GATING (Action Classification)
*Routing table for execution safety based on SOUL.md Part II.*

| Class | Definition | Execution Gate |
| :--- | :--- | :--- |
| **READ** | Inspect, search, list, query | **Direct** (Fast-path reporting allowed) |
| **WRITE** | Create new file, generate output | **Direct + Report** |
| **MUTATE** | Edit existing file, update config | **Backup → Execute → Report** |
| **BRIDGE** | Delegate to sub-agent | **Execute + Handoff Brief** |
| **DESTRUCT** | Delete file/archive, drop table | **Approval Required First** |
| **NETWORK** | HTTP POST/PUT, public API write | **Approval Required First** |

---

## 5. PHYSICAL STACK ENVIRONMENT
*Current validated state metrics.*

- **Host OS:** Linux (6.12.88+deb13-amd64)
- **User / CWD:** `hiryu` / `/home/hiryu/.hermes/hermes-agent`
- **Primary Vault:** `/home/hiryu/.hermes/vault`
- **Active UI Surface:** Telegram (ID: 340994326)
- **Model / Provider:** `Smart_Agent` via `custom` provider (v1 endpoint)
- **Agent Role:** Orchestrator (Top-level process managing Scout, Scribe, Reach, Dev via `delegate_task`)

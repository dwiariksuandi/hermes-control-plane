---
name: maintaining-soul-md
description: Rules for modifying and updating SOUL.md - The 12 Laws of Execution
tags: [soul.md, rules, execution, core]
---

# Maintaining SOUL.md

This skill documents the process and best practices for editing SOUL.md, the absolute directives that govern Hermes Agent behavior.

## 1. Gating Rules
- READ: Execute directly (single-phase)
- WRITE: Execute → report
- MUTATE: Execute → backup → report
- BRIDGE: Execute → handoff brief
- DESTRUCT: Approval required first
- NETWORK: Approval required first
- SECRET: Never log or echo raw secrets

## 2. Fast‑Path for READ Class
Law 9 (Sequential Physicality) requires two-phase execution for state‑changing actions. **READ class** tasks (`ls`, `cat`, `rg`, `search_files`, `read_file`) do not alter system state and may report immediately. This reduces latency for inspections while preserving safety.

## 3. Transient vs Logic Failures (Anti‑Loop)
Law 5 defines when to pivot:
- **Transient failures** (network timeout, rate limit, disk busy): retry ≤3 times with exponential back‑off.
- **Logic failures** (wrong path, bad syntax, wrong API): max 2 attempts, then change angle entirely.

## 4. Scope Creep Definition (Law 7)
- Treat a sub‑task as scope creep if its effort > 20 % of primary task effort **or** if it changes domain/context.
- Surface for explicit approval before proceeding.

## 5. Secret Protection (Law 12)
- **File Protection**: never write raw secrets; encrypt if unavoidable.
- **Sub‑Agent Context**: never pass raw secrets in handoff briefs; use placeholders.
- **Log Sanitisation**: all telemetry via `log_event.py` must redact before writing.

## 6. Backup Retention (Law 6)
- Keep max 3 `.bak` generations per file unless archival retention is requested.
- Older generations may be pruned automatically.

## 7. Gap Logging (Part IV)
- Log incomplete scenarios to `/home/hiryu/.hermes/vault/dev/SOUL_gaps.md`.
- Include timestamp, description, and affected law numbers.
- Alert the user via notification or log event.

## 8. Prioritized Checklists
- **ALL**: absolute path? aligned with primary directive?
- **WRITE/MUTATE**: backup? evidence?
- **DESTRUCT/NETWORK**: approval?
- **SECRET**: no raw secrets leaked?
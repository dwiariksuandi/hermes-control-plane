---
name: memory-compression
description: Compress Hermes telemetry/activity logs into long-term semantic summaries while pruning raw SQLite bloat.
---

# Memory Compression

## When to use
Use when building or maintaining Hermes long-term memory, telemetry pruning, SQLite log retention, or "infinite memory" style compression pipelines.

## Core workflow
1. Ground in disk first:
   - inspect target SQLite DB physically;
   - verify source table schema with `PRAGMA table_info(activity_logs)`;
   - verify row counts before mutation.
2. Create destination table if missing:
   - `long_term_memory(id, created_at, source_window_start, source_window_end, source_count, summary, source_agents, source_rowids)`.
3. Select compressible source rows ordered by timestamp.
4. Bucket rows deterministically, usually by hour (`YYYY-MM-DD HH`) or older-than cutoff.
5. Summarize rows densely:
   - group by agent;
   - preserve representative task summaries;
   - count success/error states;
   - keep artifact paths, but redact secrets.
6. Insert compressed record into `long_term_memory`.
7. Delete original `activity_logs` rows only after insert succeeds.
8. Commit and verify:
   - source count decreased;
   - long-term table count increased;
   - sample summary readable;
   - no credentials leaked.

## Adapted concept
From `claude-mem`: persist session/event observations, turn raw interaction history into summary records, then retrieve compact context instead of replaying full logs. Native Hermes adaptation uses SQLite + deterministic Python summarizer first, with future LLM summarizer hook.

## Pitfalls
- Do not query destination table before creating it.
- Do not assume column names; `activity_logs` may use `validation_status` instead of `validation`.
- Do not call destructive pruning before insert + commit path verified.
- Do not compress credentials, keys, payloads, or private config values into summaries.
- Prefer dry-run counts before irreversible deletion when user has not explicitly asked for immediate pruning.

## Verification
Return count delta, destination table existence, sample compressed summary, and pruned row count.

---
author: Orchestrator
status: active
timestamp: 2026-05-27
tags: [pipeline, relay, token-conservation, v4.5, orchestrator]
---

# Adaptive Content Pipeline (v4.5 Hyper-Native)

## 1. The Standard Relay (File-Based Handoff)

1. **Step 1 (SCOUT)**
   - **Mission**: Receive topic. Extract web data / primary sources.
   - **Artifact**: Writes findings to `/home/hiryu/.hermes/vault/scout/raw_brief.md`.

2. **Step 2 (SCRIBE)**
   - **Mission**: Orchestrator reads Scout's file path (NOT full text) and delegates to Scribe. Scribe synthesizes `raw_brief.md`.
   - **Artifact**: Writes `/home/hiryu/.hermes/vault/scribe/final_artifact.md` using strict YAML Frontmatter.

3. **Step 3 (REACH)**
   - **Mission**: Orchestrator passes Scribe's file path to Reach. Reach analyzes the artifact and generates a distribution strategy.
   - **Artifact**: Writes `/home/hiryu/.hermes/vault/reach/promo_plan.md`.

4. **Step 4 (ORCHESTRATOR)**
   - **Mission**: Verifies all artifacts exist via `execute_code`, reads the final summaries, and reports to {OWNER}.

## 2. Pipeline Adaptation Rules (Token Conservation)

- **Pass Paths, Not Text**: Never pass full raw texts between agents via the chat context. ALWAYS pass the absolute file paths.
- **Collapse the Pipeline**: If the request is simple (e.g., "Summarize this URL"), route directly to Scribe or execute via `execute_code`.
- **Kanban for Scale**: If the request is massive (multi-day), initialize a Kanban tracking file first before starting the relay.
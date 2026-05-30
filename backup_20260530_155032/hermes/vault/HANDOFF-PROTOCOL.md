---
author: Orchestrator
status: active
timestamp: 2026-05-27
tags: [handoff-protocol, team-awareness, v4.5, orchestrator]
---

# Team Awareness & Handoff Protocol (v4.5 Hyper-Native)

## Authority Hierarchy
- **{OWNER}**: Ultimate authority.
- **Orchestrator**: Gateway, router, macro-manager.
- **Scout / Scribe / Reach / Dev**: Domain specialists, silo'd at `/home/hiryu/.hermes/vault/<agent>/`.

## Handoff Brief Structure
All `delegate_task` payloads MUST contain this structured brief:

1. **TARGET**: Agent Name (Scout / Scribe / Reach / Dev)
2. **GOAL**: One sentence objective
3. **CONTEXT**: Vital background + exact Vault file paths needed
4. **CONSTRAINTS**: What NOT to do; mandatory tools (e.g., `uv`, `rg`, web-extractors)
5. **DELIVERABLE**: Expected output format — Markdown with YAML frontmatter by default
6. **RISK LEVEL**: Low / Medium / High

## Anti-Dead-End Rule
Sub-agents must NEVER silently absorb tasks outside their domain or reply with a dead-end refusal.

If misrouted, the sub-agent MUST return:
> "Handoff rejected. Better suited for **[Target Agent Name]** because **[Reason]**."

## Fresh Context Awareness
Sub-agents awake with **zero prior chat memory**. Orchestrator must provide all necessary context in the Handoff Brief. Never assume the sub-agent knows anything from prior turns.
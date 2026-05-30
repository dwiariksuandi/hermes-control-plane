# AI-Centric Vault Architecture (v1.0)

Proposed folder structure for Hermes Agent "Control Plane" Obsidian vault:

```text
/home/hiryu/.hermes/vault/
├── 00_Hermes_Dashboard.md    # Mission Control: status, goals, active links
├── inbox/                    # Rapid capture from chat/voice
├── projects/                 # Folder per project with README.md (goals, stack, state)
├── agents/                   # Isolated folders for specialized sub-agents (scout, dev, scribe)
├── decisions/                # Log of architectural/logic decisions (prevents looping)
├── research/                 # Domain-specific knowledge banks and source summaries
├── runbooks/                 # Reusable procedures for the agent to follow
├── logs/                     # Evidence ledger: technical proofs (exit codes, test results)
└── templates/                # Markdown templates for consistency
```

## Key Use Cases

### 1. Mission Control
The agent reads `00_Hermes_Dashboard.md` at session start to re-orient. It updates the status after major task completion.

### 2. Decision Persistence
When the user approves a path or rejects an idea, the agent writes a decision note. This stops future agents from suggesting the same rejected approach.

### 3. Context Siloing
Specialist agents (e.g. delegated scouts) write their raw findings to `agents/<name>/` and only provide a condensed summary to the Orchestrator, keeping the main context window clean.

### 4. Evidence Grounding
Following SOUL.md Law 10, agents append technical evidence to `logs/YYYY-MM-DD.md` to ensure claims are verifiable.

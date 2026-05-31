# Skill: Parallel Delegation (Orchestrator)

## Origin
Inspired by ECC (Executable Skills) and superpowers — breaking work into independent streams.

## When to Use
Tasks that are independent (no shared state, no sequential dependency).
Examples: Scout researching Topic A while Scribe documents Topic B;
Dev fixing Bug X while Scout validates API Y.

## Core Idea
Orchestrator spawns multiple subagents simultaneously via `delegate_task` with `tasks` array (max 3 for this user).
Each subagent gets isolated context, terminal, and toolset.
Wait for all to finish, then synthesize.

## Step-by-Step for ORCHESTRATOR

### 1. Identify Independent Workstreams
- Goal A and Goal B do not rely on each other's output.
- If they share a resource (e.g., same file), sequence or lock instead.

### 2. Prepare Context for Each
- Include only what that subagent needs (file paths, constraints).
- Do NOT dump entire conversation; keep context tight.
- Specify language/tone if non-English.

### 3. Choose Toolsets Minimally
- Scout: ['web', 'file'] for research.
- Scribe: ['file'] for writing.
- Dev: ['terminal', 'file'] for coding.

### 4. Launch with delegate_task (batch mode)
```python
delegate_task(
    tasks=[
        {
            "goal": "Scout: gather latest benchmarks for Llama 3 70B inference speed",
            "context": "Focus on GPU latency numbers from HuggingFace and recent papers. Save raw notes to /home/hiryu/.hermes/vault/scout/raw/llama3_benchmarks.md",
            "toolsets": ['web', 'file']
        },
        {
            "goal": "Scribe: draft README for the new workspace_mapper tool",
            "context": "Tool lives at /home/hiryu/.hermes/workspace_mapper.py. It creates a SQLite index of the vault. Include sections: Purpose, Usage, Example Queries.",
            "toolsets": ['file']
        }
    ]
)
```
Each task runs in parallel. Results returned as array.

### 5. Validate & Synthesize
- Check each subtask succeeded (status != 'interrupted').
- Collect artifacts (files written, data returned).
- If any failed, decide: retry, escalate, or continue with partial.
- Orchestrator may then assign a follow-up task (e.g., Dev integrates Scout's data into a dashboard).

## Anti-Patterns
- **False Parallelism**: Two tasks that both need the same lock (e.g., writing to same file) — they will conflict.
- **Context Bleed**: Passing entire chat history wastes tokens and may confuse subagents.
- **No Validation**: Assuming subagent succeeded without checking artifact or status.

## Integration
Orchestrator MUST check `/home/hiryu/.hermes/vault/skills/` before planning any multi-step work.
If tasks are independent, use this skill.

---
name: obsidian-self-learning
description: "Hermes Agent self-learning via Obsidian vault: sync MEMORY.md/USER.md, append learnings after complex tasks, update dashboard, manage vault hygiene."
version: 1.0.0
author: hermes-orchestrator
platforms: [linux, macos, windows]
tags: [obsidian, memory, self-learning, vault]
metadata:
  created_by: orchestrator
  class: self-learning
---

# Obsidian Self-Learning Skill

Use this skill when:
- Completing a complex/non-trivial task (5+ tool calls, errors overcome, multi-step workflow discovered)
- User asks to "remember this", "save approach", or "update memory"
- Post-session cleanup: sync Hermes memory to vault
- Cron tick: daily vault hygiene

## Core Files

| File | Purpose |
|------|---------|
| `/home/hiryu/.hermes/MEMORY.md` | Hermes active memory (built-in) |
| `/home/hiryu/.hermes/USER.md` | Hermes user profile (built-in) |
| `/home/hiryu/.hermes/vault/MEMORY.md` | Vault-synced memory (Obsidian) |
| `/home/hiryu/.hermes/vault/USER.md` | Vault-synced user profile (Obsidian) |
| `/home/hiryu/.hermes/vault/self-learning/learnings.md` | Insights accumulated across sessions |
| `/home/hiryu/.hermes/vault/00_Hermes_Dashboard.md` | System state index |

## Sync Memory to Vault (bidirectional)

```python
import shutil, os
from pathlib import Path

hermes_home = Path.home() / ".hermes"
vault = hermes_home / "vault"

# Sync Hermes → Vault
shutil.copy2(hermes_home / "MEMORY.md", vault / "MEMORY.md")
shutil.copy2(hermes_home / "USER.md", vault / "USER.md")

# Verify
assert (vault / "MEMORY.md").exists()
assert (vault / "USER.md").exists()
```

## Append Learning After Complex Task

When a complex task finishes successfully:

1. Read `vault/self-learning/learnings.md`
2. Append new entry:

```markdown
## [YYYY-MM-DD] <Task Title>

**Context:** <what was the problem/situation>
**Approach:** <what worked>
**Key Insight:** <one-liner that prevents re-learning>
**Evidence:** <file path or exit code>
**Tags:** #topic #subtopic
```

3. Format date with `datetime.now().strftime("%Y-%m-%d")`
4. Preserve YAML frontmatter at top of file.

## Update Dashboard

After any significant event (task completion, decision, error), update `00_Hermes_Dashboard.md`:

- Last activity timestamp
- Active projects count
- Learnings added this session
- Pending items from inbox

## Vault Hygiene (daily cron)

1. Move stale inbox notes (> 7 days) to `logs/`
2. Archive completed project notes to `logs/archived/`
3. Compact `logs/` into `logs/summary-YYYY-WW.md` weekly
4. Ensure `.obsidian/` workspace.json intact
5. Validate all linked paths in `learnings.md`
6. Run `hygiene_manager.py` via cron (daily 03:30) for automated retention — do NOT manually prune vault artifacts without evidence ledger entry.

## Pitfalls

- DO NOT write raw secrets to vault notes
- DO NOT sync `.env` or `auth.json` to vault
- `OBSIDIAN_VAULT_PATH` env var may be stale inside sandbox; always use absolute path `/home/hiryu/.hermes/vault`
- learnings.md frontmatter must stay intact; always append below frontmatter separator `---`
- Vault path in sub-agent context: must pass `/home/hiryu/.hermes/vault` explicitly (no env var expansion)

## Verification

After any write:
```python
from pathlib import Path
path = Path("/home/hiryu/.hermes/vault/self-learning/learnings.md")
assert path.exists()
assert path.stat().st_size > 0
```

## Script Standard (long-term stable)

Store executable scripts under:
- `/home/hiryu/.hermes/skills/note-taking/obsidian-self-learning/scripts/`

Required scripts:
- `sync_memory_vault.py` — two-way sync with conflict-safe merge policy.
- `capture_learning.py` — append structured learning entry.
- `dashboard_refresh.py` — refresh dashboard sections from filesystem truth.
- `weekly_digest.py` — summarize week learnings to digest file.

All scripts must:
1. Use absolute paths only.
2. Never read/write secrets (`.env`, `auth.json`, tokens).
3. Print compact machine-readable status (PASS/FAIL + path).
4. Exit non-zero on failure.

## Merge Policy (avoid divergence)

Source-of-truth files:
- Built-in runtime: `/home/hiryu/.hermes/MEMORY.md`, `/home/hiryu/.hermes/USER.md`
- Human-facing vault mirror: `/home/hiryu/.hermes/vault/MEMORY.md`, `/home/hiryu/.hermes/vault/USER.md`

Policy:
- Default hourly cron: runtime -> vault mirror.
- Optional `--pull` mode: vault -> runtime only when user explicitly chooses vault edits as source.
- On mismatch, write conflict record to:
  `/home/hiryu/.hermes/vault/logs/memory-conflicts-YYYY-MM.md`

## Cron Profile

Recommended jobs:
1. Hourly sync
2. Daily dashboard refresh
3. Weekly digest

Job prompts should be self-contained and write outputs under:
`/home/hiryu/.hermes/vault/self-learning/`

*Note on cronjob tool:* If using `no_agent=True` for lightweight scripts, the `script` parameter must be a relative path located under `~/.hermes/scripts/` (e.g. `weekly_digest.py`). Do not use absolute paths. Otherwise, just use `prompt` with `python3 /absolute/path.py`.

## Linked Resources

- `references/obsidian-memory-integration-notes.md`: Key distinctions between memory backends and vault paths.
- `scripts/backup_vault_git.sh`: Backup script to push vault to private GitHub.

## Evidence Checklist

After each run verify:
- File exists
- File size > 0
- Last modified timestamp changed
- Output summary file path present

## When to Trigger

| Event | Action |
|-------|--------|
| Task with 5+ tool calls completed | Append learning |
| User says "remember this" | Append learning |
| Session end | Sync MEMORY.md + USER.md to vault |
| Hourly cron tick | Sync runtime memory -> vault |
| Daily cron tick | Dashboard refresh + hygiene |
| Weekly cron tick | Digest generation |
| Complex error solved | Append learning with error context |
| New skill saved | Link in dashboard |
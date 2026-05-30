---
name: secure-agent-ops-lifecycle
description: "Secure lifecycle operations for agent-owned runtime directories: physical verification, anti-sycophancy sequencing, secret-safe git snapshots, remote backups, cron hygiene, and self-audits."
---

# Secure Agent Ops Lifecycle

## When to Use
Use this skill when asked to initialize, audit, harden, back up, push, or maintain an agent runtime directory such as `/home/hiryu/.hermes`.

Trigger phrases:
- "physical verification" or "trust but verify" or "raw terminal logs"
- "secure snapshot" or "remote backup" or "force push" or "git hygiene"
- "self-audit" or "introspection" or "architecture anatomy" or "Ouroboros"
- "cron" or "watchdog" or "janitor" or "vault hygiene" or "secret sweep"
- any multi-step system mutation where user expects physical proof before status claims

## Core Rules
1. **Sequential physicality first.** For multi-step execution tasks, do tool calls first, wait for tool output, then report. Never emit success wording before physical output exists.
2. **Raw logs beat summaries.** If user asks for proof, provide raw terminal excerpts first; interpretation second.
3. **No fake completion.** If a command fails, report failure plainly and continue only if authorized or clearly safe.
4. **Backup or ignore before git add.** Before `git add .`, verify `.gitignore` excludes secrets, DBs, logs, venvs, and runtime state.
5. **Secret cache purge.** If sensitive files were staged, run `git rm --cached <file>` and amend commit before push.
6. **Runtime state stays local.** Files like `auth.json`, `auth.lock`, databases, logs, `.env`, and channel/session state should be ignored unless explicitly intended.
7. **Force push only with explicit owner authority.** Treat `git push --force` as history rewrite and destructive remote mutation.
8. **Audit after push.** Run `git status`, `git log --oneline -3`, and remote check after push.

## Standard Secure Git Snapshot Flow
```bash
cd /home/hiryu/.hermes
cat > .gitignore <<'EOF'
venv/
.env
*.db
*.log
*.bak
__pycache__/
.DS_Store
auth.json
auth.lock
channel_directory.json
EOF

git init
git status --short
git add .
git status --short
git commit -m "INIT: Project Aegis V5.1 Flawless - Architecture Locked"
```

If auth/state files were already staged:
```bash
git rm --cached auth.json auth.lock channel_directory.json || true
git add .gitignore
git commit --amend --no-edit
```

## Remote Push Flow
```bash
git config --global user.email "hermes@aegis.local"
git config --global user.name "Hermes Agent"
git branch -M main
git remote add origin git@github.com:OWNER/REPO.git 2>/dev/null || git remote set-url origin git@github.com:OWNER/REPO.git
git push -u origin main
```

If remote rejects due existing history and owner authorizes local source-of-truth takeover:
```bash
git push -u origin main --force
```

## Verification Checklist
- `git status` says exactly `nothing to commit, working tree clean` when user requests **literal Absolute Zero**.
- If `git status` shows untracked runtime residue (e.g., `bin/`, `processes.json`), append ignore rules and re-check before final report.
- If `git status` shows untracked knowledge artifacts meant for vault backup (e.g., new `skills/...`), stage+commit+push them.
- `git log --oneline -3` shows expected commits.
- `git remote -v` points to correct SSH URL.
- grep/secret sweep finds no active keys in tracked files.
- `.gitignore` contains `.env`, `auth.json`, `auth.lock`, `*.db`, `*.log`, `*.bak`, `venv/`, `__pycache__/`, plus runtime files created during remediation (`bin/`, `processes.json`) when applicable.

## Pitfalls
- `ssh -T git@github.com` can exit non-zero even when successful; inspect text output.
- Git commit fails if `user.name`/`user.email` missing; configure before commit.
- `git add .` can stage secrets if `.gitignore` is incomplete. Check before adding.
- `git stash` may leave generated runtime changes after automation scripts run; re-check `git status`.
- Large terminal output may truncate chat; prefer concise raw proof slices plus exact commit hashes.

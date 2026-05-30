# Skill: Vault Hygiene (Janitor)

## Origin
PROJECT AEGIS Phase 5 — Operation Janitor.

## When to Use
**PERIODICALLY** — to prevent system bloat and security leaks.
Can be integrated into cron jobs for automated daily/weekly runs.

## Core Rule
**To prevent system bloat and security leaks, you MUST periodically execute run_maintenance from /home/hiryu/.hermes/aegis/aegis_janitor.py to clear old .bak files and scan for hardcoded secrets.**

## Procedure
1. Import:
   ```python
   import sys
   sys.path.insert(0, "/home/hiryu/.hermes/aegis")
   from aegis_janitor import run_maintenance, cure_entropy, sweep_secrets
   ```

2. Run full maintenance:
   ```python
   result = run_maintenance(vault_path="/home/hiryu/.hermes/vault", days_old=7)
   print(result)
   ```

3. Individual functions for selective use:
   - `cure_entropy(vault_path, days_old=3)`: Safely deletes old .bak, dummy_*, or *_temp files.
   - `sweep_secrets(vault_path)`: Executes `trufflehog filesystem` scan. (Requires `trufflehog` CLI in PATH).

## Anti-Patterns
- Allowing .bak files to accumulate indefinitely.
- Never scanning the codebase for accidentally committed secrets.
- Hardcoding `trufflehog` paths or parameters.

## Checklist
- [ ] Old temporary files are regularly pruned.
- [ ] Regular secret sweeps are performed.
- [ ] TruffleHog CLI is available (if secret sweep is enabled).
- [ ] Output from `run_maintenance` is reviewed for findings.
# Skill: API Resilience (LiteLLM Router)

## Origin
PROJECT AEGIS Phase 4 — Operation Banker.

## When to Use
**ALWAYS** — whenever you need to programmatically call an external LLM (e.g., orchestrating another agent via script).

## Core Rule
**Whenever you need to programmatically call an external LLM (e.g., orchestrating another agent via script), you MUST use safe_llm_call from /home/hiryu/.hermes/aegis/aegis_router.py to ensure budget limits and network resilience are enforced.**

## Procedure
1. Import:
   ```python
   import sys
   from pathlib import Path
   AEGIS_PATH = str(Path("/home/hiryu/.hermes/aegis").resolve())
   if AEGIS_PATH not in sys.path:
       sys.path.insert(0, AEGIS_PATH)
   from aegis_router import safe_llm_call
   ```

2. Call with budget cap:
   ```python
   response = safe_llm_call(
       model="anthropic/claude-sonnet-4",
       messages=[{"role": "user", "content": "Analyze this data"}],
       max_budget=0.10  # cents-level control
   )
   ```

3. Features:
   - Budget enforced via LiteLLM `max_budget` param.
   - Exponential backoff for 429/5xx errors.
   - Up to 3 retries.
   - Hard fails on auth/budget exceeded to prevent infinite loops.

## Anti-Patterns
- Direct `openai`, `anthropic`, or raw API calls without budgeting.
- Ignoring rate limit (429) responses and retrying immediately.
- Skipping retries on transient network errors.

## Checklist
- [ ] LLM calls routed through safe_llm_call.
- [ ] max_budget specified per call.
- [ ] Retries configured via LiteLLM params.
- [ ] Auth failures raise RuntimeError, stop execution.
# Skill: Secure Execution (E2B Sandbox)

## Origin
PROJECT AEGIS Phase 2 — Operation Isolator.

## When to Use
**ALWAYS** — whenever you need to execute Python code to test a script, run analysis, or perform any computation.

## Core Rule
**For ALL Python code execution tasks, you MUST import and use safe_execute_python from /home/hiryu/.hermes/aegis/aegis_sandbox.py. NEVER run raw subprocesses for testing code on the host OS.**

## Procedure
1. Import the safe executor:
   ```python
   import sys
   from pathlib import Path
   AEGIS_PATH = str(Path("/home/hiryu/.hermes/aegis").resolve())
   if AEGIS_PATH not in sys.path:
       sys.path.insert(0, AEGIS_PATH)
   from aegis_sandbox import safe_execute_python
   ```

2. Pass your code as a string:
   ```python
   output = safe_execute_python("print('hello from sandbox')")
   print(output)
   ```

3. For file-based execution:
   ```python
   from pathlib import Path
   source = Path("/path/to/script.py").read_text()
   output = safe_execute_python(source)
   ```

## Timeout Default
60 seconds max.

## Error Handling
- `RuntimeError` on missing API key → report to owner.
- `RuntimeError` on import failure → ensure requirements are installed.
- Any sandbox error → propagate message.

## Checklist
- [ ] Code runs inside E2B sandbox, not host.
- [ ] E2B_API_KEY loaded from env.
- [ ] stdout + stderr captured and returned.
- [ ] Sandbox closed after execution.

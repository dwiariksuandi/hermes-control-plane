# Skill: TDD Loop (Red-Green-Refactor)

## Origin
Adapted from obra/superpowers — methodical execution loops for AI agents.

## When to Use
ALL new features, bug fixes, refactors.
SKIP only on throwaway prototypes or config files (owner approval required).

## Core Protocol

```
RED       — Write one failing test first
VERIFY    — Run it. Watch it fail (proves test catches something)
GREEN     — Write minimal code to pass
VERIFY    — Run it. Watch it pass
REFACTOR  — Clean up. Keep green.
REPEAT    — Next behavior. One cycle at a time.
```

## Iron Law
NO production code without a failing test first.
Write code before the test? DELETE it. Start over.
No exceptions — "keep as reference" = cheating.

## Step-by-Step for DEV

### RED Phase
1. Identify ONE behavior to implement
2. Write test with clear descriptive name (not "test_it_works")
3. Use real code, not mocks (mocks only if truly unavoidable)
4. One assertion per test (name has "and"? split it)

### Verify RED
```bash
pytest <test_file>::<test_name> -v
```
Confirm: test fails, failure reason expected, not a typo/import error.
Test passes immediately? You're testing existing behavior — fix the test.

### GREEN Phase
Write simplest code to pass. Nothing more.
Cheating OK: hardcode returns, copy-paste, skip edge cases.
Fix in REFACTOR.

### Verify GREEN
```bash
pytest <test_file>::<test_name> -v
pytest tests/ -q   # full suite for regressions
```

### REFACTOR Phase
- Remove duplication, improve names, extract helpers
- Keep tests green throughout
- If tests break: UNDO. Smaller steps.

## Anti-Rationalization Table

| Excuse | Truth |
|--------|-------|
| "Too simple to test" | Simple code breaks. 30s test. |
| "I'll test after" | Tests-after pass immediately — prove nothing. |
| "Already manually tested" | Ad-hoc ≠ systematic. No record. |
| "Deleting code is wasteful" | Sunk cost. Keeping unverified code = debt. |
| "Keep as reference, rewrite" | You'll adapt it. That's testing after. |

## Replay Protection
If you catch yourself doing ANY of these, delete and restart:
- Code before test
- Test passes first run
- Rationalizing "just this once"
- "Keep as reference"
- Already tested manually

## Checklist
- [ ] Each new function has a test
- [ ] Watched each test fail before implementing
- [ ] Minimal code to pass each test
- [ ] All tests pass, pristine output
- [ ] Edge cases + errors covered

## Integration
DEV agent MUST apply before writing any code.
Check vault/skills/ before every code task.

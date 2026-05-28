# Aegis Workflow Overview

This document captures the step-by-step methodology applied during **PROJECT AEGIS** to harden the Hermes agent architecture:

1. **Research & Dependency Lockdown** - Verify syntax via official repos, lock packages via `requirements.txt`.
2. **Isolator Script Creation** - Write isolated wrappers in `/home/hiryu/.hermes/aegis/` with defensive patterns.
3. **Skill Injection** - Enforce usage via SOPs in `/home/hiryu/.hermes/vault/skills/`.
4. **Verification** - Use physical file reads to confirm mutations before reporting.
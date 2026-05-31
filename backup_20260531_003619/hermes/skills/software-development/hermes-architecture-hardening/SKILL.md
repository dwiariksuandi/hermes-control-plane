---
name: hermes-architecture-hardening
description: "A playbook for applying security and resilience layers to the Hermes agent's own architecture."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security, architecture, self-improvement, hardening, aegis]
    related_skills: [hermes-agent, skill_secure_execution, skill_data_sanitization, skill_api_resilience]
---

# Hermes Architecture Hardening Playbook

## Overview

This skill documents the standard operating procedure for integrating new security, resilience, or performance layers into the Hermes agent's core architecture. It is based on the "PROJECT AEGIS" methodology observed during our initial setup.

## When to Use

When the user directs you to harden, secure, or upgrade a core component of your own system (e.g., code execution, API calls, data handling).

## The Four-Phase Process

Execute these steps in order, using strict absolute coordinates for all file paths, as per `SOUL.md` Law 2.

### Phase 1: Research & Dependency Lockdown

1.  **Zero-Hallucination Research:** If integrating a new library, DO NOT guess the syntax. Clone the official repository to `/tmp/` and read the `README.md`, documentation, and examples to confirm the correct, modern implementation.
    ```bash
    # Example for researching a library
    cd /tmp && rm -rf repo-name
    git clone --depth 1 <repo_url>
    cat /tmp/repo-name/README.md | head -n 100
    ```
2.  **Lock Dependency:** Append the required package(s) to `/home/hiryu/.hermes/requirements.txt`. Per `SOUL.md` Law 6, create a `.bak` copy first.

### Phase 2: The Isolator Script

1.  **Create Wrapper:** Write a new Python module inside `/home/hiryu/.hermes/aegis/`. The name should reflect its purpose (e.g., `aegis_sandbox.py`, `aegis_router.py`).
2.  **Implement Core Logic:** Inside this module, implement the core functionality. This script acts as a hardened wrapper around the new library, exposing a simple, safe function (e.g., `safe_execute_python()`, `sanitize_input()`).
3.  **Handle Credentials:** If the library requires API keys, load them from the environment via `dotenv` from `/home/hiryu/.hermes/.env`. Never hardcode keys.

### Phase 3: Skill Injection

1.  **Create Enforcement SOP:** Create a new skill markdown file in `/home/hiryu/.hermes/vault/skills/`. The name should be specific to the function (e.g., `skill_secure_execution.md`).
2.  **Mandate Usage:** The skill's core rule MUST explicitly and strictly mandate the use of the new function from the Aegis wrapper script. It should forbid falling back to insecure, raw methods.

### Phase 4: Absolute Verification

1.  **Confirm Mutations:** Before reporting success, run a final physical check to verify that all files have been created and patched correctly.
2.  **Use `ls`, `cat`, `grep`, or a verification script** to read the files back and confirm their contents match the objective. This adheres to `SOUL.md` Law 4.
3.  **Emit raw proof when asked:** If user asks for audit/proof, return raw terminal output blocks (not summary claims).
4.  **No completion without evidence:** Never output success state if any required artifact is missing (`File not found`, empty grep, missing script). Continue patching until proof checks pass.
5.  **Tool-interruption recovery:** If response is interrupted or empty after tool calls, immediately resume from last successful mutation and run verification again before reporting.

### Pitfalls (Observed)

- **Hallucinated completion risk:** Multi-step hardening can drift into optimistic reporting. Countermeasure: mandatory end-of-run verification checklist with explicit pass/fail per artifact.
- **Partial-write risk in automation scripts:** When script writes another script via heredoc, verify both files exist and grep for required constants/paths.
- **Security tooling absent at runtime:** For external CLIs (e.g., trufflehog), report explicit runtime status (`binary missing`) and keep maintenance flow non-fatal.

## Example AEGIS Operations

- **Bedrock (uv Lockdown):** Secured Python dependencies in a virtual environment.
- **Isolator (E2B Sandbox):** Isolated `execute_code` in an ephemeral sandbox.
- **Censor (Presidio/Rebuff):** Shielded against PII leaks and prompt injections.
- **Banker (LiteLLM):** Added budget caps and resilient retries to API calls.

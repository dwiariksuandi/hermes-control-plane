# Reference: Obsidian Vault Setup (2026-05-29)

This reference documents the successful setup of a structured Obsidian vault for Hermes Agent memory.

## Session Goal

The user requested a full-stack audit of Obsidian as a memory store, followed by a clean, gap-free setup.

## Key Steps Executed

1.  **Audit:**
    *   Confirmed Obsidian CLI existed but vault path was not set.
    *   Confirmed `MEMORY.md` and `USER.md` were missing from the filesystem.
    *   Determined that Hermes was using its internal memory, not an Obsidian vault.

2.  **Initialization:**
    *   Chose `/home/hiryu/.hermes/vault` as the vault root.
    *   Created standard Obsidian directories: `.obsidian`, `memory`, `logs`, `templates`.
    *   Created `00_Hermes_Dashboard.md` as the vault index.
    *   Added `OBSIDIAN_VAULT_PATH=/home/hiryu/.hermes/vault` to `.env`.
    *   Created placeholder `MEMORY.md` and `USER.md` and linked them to the vault.

3.  **Verification:**
    *   Confirmed the vault structure with `ls -R`.
    *   Ran an `execute_code` script to test file-tool access (`read_file`, `write_file`, `search_files`) against the vault path.
    *   The test passed, proving Hermes can read and write notes in the vault.

## Final State

*   **Vault Path:** `/home/hiryu/.hermes/vault`
*   **Environment Variable:** `OBSIDIAN_VAULT_PATH` is set and loaded.
*   **Integration:** Hermes file tools can access the vault. The `obsidian` skill can now operate on this vault.
*   **Memory Backend:** Hermes still uses its internal memory automatically. The vault provides a structured, human-readable filesystem layer for notes and artifacts, but is not the active memory provider.

## Critical Learning

-   A running process (like a tool sandbox or the gateway) will not see environment variable changes in `.env` until it is restarted. The verification script failed initially because the sandbox process did not have `OBSIDIAN_VAULT_PATH` loaded. The fix was to re-read `.env` manually within the script.
-   "Obsidian memory" is ambiguous. It can mean:
    1.  A directory of Markdown files that Obsidian can open (what we built).
    2.  A native Hermes memory provider that uses an Obsidian vault directly (which doesn't appear to exist out-of-the-box).
    This distinction is crucial for setting correct user expectations.

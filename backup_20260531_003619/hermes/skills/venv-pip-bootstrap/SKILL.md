---
name: venv-pip-bootstrap
description: "Standard Python virtual environment creation and dependency installation using `python3 -m venv` and `pip`."
---

# Venv/Pip Bootstrap

## When to Use
Use this skill when you need to create a Python virtual environment and install dependencies, especially as a fallback when `uv` or other modern installers are not available or fail.

## Workflow

1.  **Purge existing environment (if any):**
    ```bash
    rm -rf /path/to/venv
    ```
2.  **Create virtual environment:**
    ```bash
    python3 -m venv /path/to/venv
    ```
    - Replace `/path/to/venv` with the desired absolute path for the virtual environment.

3.  **Upgrade pip within the venv (optional but recommended):**
    ```bash
    /path/to/venv/bin/pip install --upgrade pip
    ```

4.  **Install dependencies from `requirements.txt`:**
    ```bash
    /path/to/venv/bin/pip install -r /path/to/requirements.txt
    ```
    - Replace `/path/to/requirements.txt` with the absolute path to your `requirements.txt` file.

## Pitfalls
- **`python3` not found:** Ensure `python3` is in the system's PATH. If not, use the full path to the Python executable (e.g., `/usr/bin/python3`).
- **Missing `requirements.txt`:** The `pip install -r` command will fail if the `requirements.txt` file does not exist at the specified path.
- **Permission errors:** Ensure you have write permissions to the directory where the virtual environment is being created.

## Example
```bash
# Example for /home/hiryu/.hermes
rm -rf /home/hiryu/.hermes/venv
python3 -m venv /home/hiryu/.hermes/venv
/home/hiryu/.hermes/venv/bin/pip install --upgrade pip
/home/hiryu/.hermes/venv/bin/pip install -r /home/hiryu/.hermes/requirements.txt
```
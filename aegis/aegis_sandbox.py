"""E2B Sandbox Isolator — execute Python code inside ephemeral cloud containers."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Absolute path enforcement
HERMES_ROOT = Path("/home/hiryu/.hermes")
DOTENV_PATH = HERMES_ROOT / ".env"

# Load environment variables
if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH)

def safe_execute_python(code: str, timeout: int = 60) -> str:
    """Execute Python code inside an E2B sandbox.

    Args:
        code: Python source code to execute.
        timeout: Maximum seconds the sandbox may run.

    Returns:
        Combined stdout + stderr output as a string.

    Raises:
        RuntimeError: If E2B_API_KEY is missing or sandbox execution fails.
    """
    try:
        from e2b_code_interpreter import Sandbox
    except ImportError:
        raise RuntimeError(
            "e2b_code_interpreter not installed. "
            "Ensure /home/hiryu/.hermes/requirements.txt is synced."
        )

    api_key = os.environ.get("E2B_API_KEY")
    if not api_key:
        raise RuntimeError("E2B_API_KEY missing in environment.")

    # Official E2B Code Interpreter execution logic
    try:
        with Sandbox.create(api_key=api_key) as sandbox:
            execution = sandbox.run_code(code)
            
            # Capture results
            results = []
            if execution.logs.stdout:
                results.extend(execution.logs.stdout)
            if execution.logs.stderr:
                results.extend(execution.logs.stderr)
            
            # Handle error traces
            if execution.error:
                results.append(f"Error: {execution.error.name} - {execution.error.value}")
                if execution.error.traceback:
                    results.append(execution.error.traceback)

            output = "\n".join(str(r) for r in results).strip()
            return output if output else "(No output)"
            
    except Exception as e:
        raise RuntimeError(f"E2B Sandbox Failure: {str(e)}")

if __name__ == "__main__":
    # Test block
    test_code = "print('E2B Precision Test: Success')"
    try:
        print(safe_execute_python(test_code))
    except Exception as err:
        print(f"FAILED: {err}")

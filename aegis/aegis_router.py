"""Aegis Router — API Budgeting, Exponential Backoff, and Circuit Breaker via LiteLLM."""

import os
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

# Absolute path enforcement
HERMES_ROOT = Path("/home/hiryu/.hermes")
DOTENV_PATH = HERMES_ROOT / ".env"
if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH)

log = logging.getLogger("aegis_router")

# Circuit breaker state
_circuit_failures = 0
_circuit_open_until = 0.0
CIRCUIT_THRESHOLD = 5
CIRCUIT_COOLDOWN = 120  # seconds

def safe_llm_call(model: str, messages: list, max_budget: float = 0.5) -> str:
    """Call external LLM via LiteLLM with budget cap and exponential backoff.

    Args:
        model: LiteLLM model identifier (e.g., "anthropic/claude-sonnet-4").
        messages: List of message dicts following OpenAI chat format.
        max_budget: Maximum USD spend per call (default $0.50).

    Returns:
        Assistant response text.

    Raises:
        RuntimeError: On budget exceeded or unrecoverable failure after retries.
    """
    global _circuit_failures, _circuit_open_until
    now = time.time()
    if _circuit_failures >= CIRCUIT_THRESHOLD and now < _circuit_open_until:
        raise RuntimeError(f"Circuit breaker open (too many failures). Retry after {int(_circuit_open_until - now)}s.")
    if _circuit_failures >= CIRCUIT_THRESHOLD and now >= _circuit_open_until:
        # half-open attempt
        _circuit_failures = 0  # reset for trial

    try:
        import litellm
        from litellm import completion
        from litellm import AuthenticationError, RateLimitError, APIConnectionError, ServiceUnavailableError, APIError, BudgetExceededError
    except ImportError:
        raise RuntimeError("litellm not installed — ensure requirements.txt is synced.")

    # Enforce budget
    litellm.max_budget = max_budget

    retries = 0
    max_retries = 3
    base_delay = 2  # seconds

    while retries <= max_retries:
        try:
            response = completion(model=model, messages=messages)
            # Success: reset failure count
            _circuit_failures = 0
            return response.choices[0].message.content

        except RateLimitError as exc:
            log.warning("Rate limit hit (429), backing off")
            retries += 1
            delay = base_delay * (2 ** (retries - 1))
            time.sleep(delay)

        except (APIConnectionError, ServiceUnavailableError) as exc:
            log.warning("Transient network error, backing off")
            retries += 1
            delay = base_delay * (2 ** (retries - 1))
            time.sleep(delay)

        except (AuthenticationError, BudgetExceededError) as exc:
            _circuit_failures += 1
            _circuit_open_until = time.time() + CIRCUIT_COOLDOWN
            raise RuntimeError(f"API auth/budget error (non-retryable): {exc}")

        except Exception as exc:
            _circuit_failures += 1
            _circuit_open_until = time.time() + CIRCUIT_COOLDOWN
            raise RuntimeError(f"Unrecoverable LLM error: {exc}")

    # If we exited loop, all retries exhausted
    _circuit_failures += 1
    _circuit_open_until = time.time() + CIRCUIT_COOLDOWN
    raise RuntimeError(f"LLM call failed after {max_retries} retries.")

if __name__ == "__main__":
    # Test: dry-run with echo model
    try:
        print(safe_llm_call("openai/gpt-4o-mini", [{"role": "user", "content": "Say OK"}]))
    except Exception as err:
        print(f"FAILED: {err}")

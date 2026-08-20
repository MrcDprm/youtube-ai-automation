"""Shared tenacity retry policies for every outbound network call.

The guiding rule is that only transient failures are retried. A ``429`` or a ``5xx`` means
"come back later", so backing off helps. A ``401`` or ``404`` means the request itself is
wrong, and retrying only wastes the caller's rate-limit budget and hides the real error.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any, TypeVar

import requests
from tenacity import (
    AsyncRetrying,
    RetryCallState,
    Retrying,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

from config.constants import RETRYABLE_STATUS_CODES
from utils.logger import get_logger

__all__ = [
    "is_retryable_exception",
    "make_async_retrying",
    "make_retrying",
    "retry_http_call",
    "status_is_retryable",
]

logger = get_logger(__name__)

T = TypeVar("T")


def status_is_retryable(status_code: int) -> bool:
    """Report whether an HTTP status justifies another attempt.

    Args:
        status_code: The HTTP response status.

    Returns:
        ``True`` for rate limits, request timeouts and server-side errors.
    """
    return status_code in RETRYABLE_STATUS_CODES


def is_retryable_exception(exc: BaseException) -> bool:
    """Classify an exception as transient or fatal.

    Args:
        exc: The exception raised by the attempted call.

    Returns:
        ``True`` for connection errors, timeouts and retryable HTTP statuses.
    """
    if isinstance(exc, requests.Timeout | requests.ConnectionError | requests.TooManyRedirects):
        return True
    if isinstance(exc, requests.HTTPError):
        response = exc.response
        return response is not None and status_is_retryable(response.status_code)
    return False


def _log_before_sleep(retry_state: RetryCallState) -> None:
    """Log an upcoming retry with its delay and cause.

    Args:
        retry_state: Tenacity's state for the failed attempt.
    """
    outcome = retry_state.outcome
    reason = "unknown error"
    if outcome is not None and outcome.failed:
        exc = outcome.exception()
        reason = f"{type(exc).__name__}: {exc}"
    delay = getattr(retry_state.next_action, "sleep", 0.0)
    logger.warning(
        "Attempt %d failed (%s); retrying in %.1fs",
        retry_state.attempt_number,
        reason,
        delay,
    )


def make_retrying(
    *,
    max_attempts: int,
    initial_wait: float = 1.0,
    max_wait: float = 30.0,
    jitter: float = 1.0,
    predicate: Callable[[BaseException], bool] | None = None,
) -> Retrying:
    """Build a configured :class:`tenacity.Retrying` controller.

    Args:
        max_attempts: Total attempts including the first, capped so a hung provider cannot
            stall the pipeline indefinitely.
        initial_wait: Base delay in seconds for the exponential backoff.
        max_wait: Ceiling for a single delay.
        jitter: Maximum random seconds added to each delay, which prevents several scenes
            from retrying in lockstep.
        predicate: Classifier deciding whether an exception is retryable. Defaults to
            :func:`is_retryable_exception`.

    Returns:
        A ``Retrying`` instance ready to wrap a callable.
    """
    return Retrying(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential_jitter(initial=initial_wait, max=max_wait, jitter=jitter),
        retry=retry_if_exception(predicate or is_retryable_exception),
        before_sleep=_log_before_sleep,
        reraise=True,
    )


def make_async_retrying(
    *,
    max_attempts: int,
    initial_wait: float = 1.0,
    max_wait: float = 30.0,
    jitter: float = 1.0,
    predicate: Callable[[BaseException], bool] | None = None,
) -> AsyncRetrying:
    """Build the async counterpart of :func:`make_retrying`.

    Needed because ``edge_tts.Communicate.stream`` may only be consumed once per instance, so
    each attempt has to construct a fresh object inside the retry block rather than replaying
    a single coroutine.

    Args:
        max_attempts: Total attempts including the first.
        initial_wait: Base delay in seconds for the exponential backoff.
        max_wait: Ceiling for a single delay.
        jitter: Maximum random seconds added to each delay.
        predicate: Classifier deciding whether an exception is retryable.

    Returns:
        An ``AsyncRetrying`` instance for use as ``async for attempt in ...``.
    """
    return AsyncRetrying(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential_jitter(initial=initial_wait, max=max_wait, jitter=jitter),
        retry=retry_if_exception(predicate or is_retryable_exception),
        before_sleep=_log_before_sleep,
        reraise=True,
    )


def retry_http_call(
    func: Callable[..., T],
    *args: Any,
    max_attempts: int = 4,
    predicate: Callable[[BaseException], bool] | None = None,
    **kwargs: Any,
) -> T:
    """Invoke ``func`` under the shared retry policy.

    Args:
        func: The callable to run, typically a bound request method.
        *args: Positional arguments forwarded to ``func``.
        max_attempts: Total attempts including the first.
        predicate: Optional custom retryable-exception classifier.
        **kwargs: Keyword arguments forwarded to ``func``.

    Returns:
        Whatever ``func`` returns on its first successful attempt.

    Raises:
        Exception: The final exception, re-raised unchanged once attempts are exhausted.
    """
    controller = make_retrying(max_attempts=max_attempts, predicate=predicate)
    return controller(func, *args, **kwargs)


def log_retry_summary(attempts: int, target: str) -> None:
    """Record how many attempts a successful call needed.

    Args:
        attempts: Number of attempts made.
        target: Human-readable description of what was called.
    """
    if attempts > 1:
        logger.info("Succeeded after %d attempts: %s", attempts, target)


def quiet_logger_for_tests() -> logging.Logger:
    """Return this module's logger.

    Exposed so tests can attach their own handler and assert on retry messages.

    Returns:
        The module logger.
    """
    return logger

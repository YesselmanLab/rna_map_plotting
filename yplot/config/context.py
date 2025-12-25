"""
Context managers for temporary configuration changes.

This module provides utilities for temporarily modifying yplot configuration
within a specific scope, automatically restoring original values on exit.
"""

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any, Optional

from yplot.config.rc_params import rcParams


@contextmanager
def rc_context(
    params: Optional[dict[str, Any]] = None
) -> Generator[None, None, None]:
    """
    Context manager for temporary configuration changes.

    Parameters are restored to their original values when the context exits,
    even if an exception occurs.

    Args:
        params: Dictionary of configuration parameters to temporarily set.

    Yields:
        None

    Example:
        >>> from yplot.config import rc_context
        >>> with rc_context({'font.size': 12, 'axes.linewidth': 1.5}):
        ...     # Code here uses modified settings
        ...     pass
        >>> # Settings are restored here
    """
    original_values = rcParams.copy()
    try:
        if params:
            rcParams.update_from_dict(params)
        yield
    finally:
        rcParams.reset()
        for key, value in original_values.items():
            rcParams[key] = value

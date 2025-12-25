"""
Configuration system for yplot.

This module provides matplotlib-style configuration management for yplot,
allowing global and context-local style customization.

Example:
    >>> import yplot
    >>> yplot.rcParams['font.size'] = 10
    >>> with yplot.rc_context({'axes.linewidth': 1.5}):
    ...     # Use modified settings
    ...     pass
"""

from yplot.config.context import rc_context
from yplot.config.defaults import DEFAULT_PARAMS, get_default, list_keys
from yplot.config.rc_params import RcParams, rcParams

__all__ = [
    "rcParams",
    "RcParams",
    "rc_context",
    "DEFAULT_PARAMS",
    "get_default",
    "list_keys",
]

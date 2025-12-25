"""
Logarithmic axis utilities with zero handling.

This module provides functions for creating log-scale axes that
gracefully handle zero values.
"""

from collections.abc import Sequence
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FuncFormatter


def compute_eps_and_transform(
    x: np.ndarray,
    epsilon_factor: float = 0.1,
) -> tuple[float, np.ndarray, np.ndarray]:
    """
    Compute epsilon value and transform data for log scale with zeros.

    Args:
        x: Input array that may contain zeros.
        epsilon_factor: Factor to multiply minimum positive value (default: 0.1).

    Returns:
        Tuple of (epsilon, positive_values, transformed_x) where:
            - epsilon: Small value representing zero on log scale
            - positive_values: Array of positive values from x
            - transformed_x: x with zeros replaced by epsilon

    Raises:
        ValueError: If all x values are zero.

    Example:
        >>> x = np.array([0, 0.1, 1, 10])
        >>> eps, pos, x_plot = compute_eps_and_transform(x)
    """
    positive = x[x > 0]
    if positive.size == 0:
        raise ValueError("All x values are zero; cannot use log scale.")

    eps = epsilon_factor * float(np.min(positive))
    x_transformed = x.copy()
    x_transformed[x_transformed <= 0] = eps

    return eps, positive, x_transformed


def log_axis_with_zero(
    ax: plt.Axes,
    eps: float,
    positive_values: np.ndarray,
    decade_ticks: Optional[Sequence[float]] = None,
    left_pad: float = 1.5,
    right_pad: float = 1.5,
) -> None:
    """
    Configure log scale x-axis with zero represented at epsilon.

    Args:
        ax: The matplotlib Axes object to modify.
        eps: Epsilon value representing zero.
        positive_values: Array of positive data values.
        decade_ticks: Optional list of decade tick positions.
        left_pad: Left padding factor for x-limits.
        right_pad: Right padding factor for x-limits.

    Example:
        >>> eps, pos, x_plot = compute_eps_and_transform(data)
        >>> ax.scatter(x_plot, y)
        >>> log_axis_with_zero(ax, eps, pos)
    """
    ax.set_xscale("log")

    tick_positions = _compute_tick_positions(eps, positive_values, decade_ticks)
    ax.xaxis.set_major_locator(FixedLocator(tick_positions))

    ax.xaxis.set_major_formatter(FuncFormatter(lambda val, _: _format_tick(val, eps)))
    ax.set_xlim(eps / left_pad, float(np.max(positive_values)) * right_pad)


def _compute_tick_positions(
    eps: float,
    positive_values: np.ndarray,
    decade_ticks: Optional[Sequence[float]],
) -> list:
    """Compute tick positions for log axis."""
    if decade_ticks is None:
        lo_pow = int(np.floor(np.log10(max(eps, float(np.min(positive_values)) * 0.8))))
        hi_pow = int(np.ceil(np.log10(float(np.max(positive_values)) * 1.2)))
        decade_ticks = [10.0**p for p in range(lo_pow, hi_pow + 1)]

    max_val = float(np.max(positive_values)) * 1.05
    filtered = [t for t in decade_ticks if eps <= t <= max_val]
    return [eps] + filtered


def _format_tick(val: float, eps: float) -> str:
    """Format tick label, showing '0' for epsilon value."""
    if np.isclose(val, eps):
        return "0"
    return f"{val:g}"

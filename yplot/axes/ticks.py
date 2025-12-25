"""
Custom tick utilities for matplotlib axes.

This module provides functions for creating custom tick configurations
on matplotlib axes.
"""

import matplotlib.pyplot as plt
import numpy as np


def add_custom_ticks(
    ax: plt.Axes,
    axis: str,
    min_val: float,
    max_val: float,
    num_ticks: int,
) -> plt.Axes:
    """
    Add evenly spaced custom ticks to an axis.

    Args:
        ax: The matplotlib Axes object to modify.
        axis: Which axis to modify ('x' or 'y').
        min_val: Minimum value for ticks.
        max_val: Maximum value for ticks.
        num_ticks: Number of ticks to create (including endpoints).

    Returns:
        The modified matplotlib Axes object.

    Raises:
        ValueError: If num_ticks < 2 or axis is not 'x' or 'y'.

    Example:
        >>> fig, ax = plt.subplots()
        >>> add_custom_ticks(ax, 'x', 0.0, 0.5, 6)
        # Creates ticks: 0.0, 0.1, 0.2, 0.3, 0.4, 0.5
    """
    if num_ticks < 2:
        raise ValueError("num_ticks must be at least 2")

    ticks = np.linspace(min_val, max_val, num_ticks, endpoint=True)

    if axis.lower() == "x":
        ax.set_xticks(ticks)
    elif axis.lower() == "y":
        ax.set_yticks(ticks)
    else:
        raise ValueError("axis must be 'x' or 'y'")

    return ax


def set_tick_params(
    ax: plt.Axes,
    axis: str = "both",
    width: float = 0.75,
    size: float = 2.0,
    pad: float = 1.0,
    direction: str = "out",
) -> plt.Axes:
    """
    Set tick parameters for an axis.

    Args:
        ax: The matplotlib Axes object to modify.
        axis: Which axis to modify ('x', 'y', or 'both').
        width: Tick line width.
        size: Tick length.
        pad: Distance between tick and label.
        direction: Tick direction ('in', 'out', 'inout').

    Returns:
        The modified matplotlib Axes object.
    """
    ax.tick_params(
        axis=axis,
        width=width,
        length=size,
        pad=pad,
        direction=direction,
    )
    return ax

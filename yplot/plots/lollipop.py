"""
Lollipop plot utilities.

This module provides functions for creating lollipop plots,
which display paired data points connected by vertical lines.
"""

from collections.abc import Sequence
from typing import Optional

import matplotlib.pyplot as plt

from yplot.config import rcParams


def lollipop_plot(
    x: Sequence,
    y1: Sequence,
    y2: Optional[Sequence] = None,
    ax: Optional[plt.Axes] = None,
    line_color: Optional[str] = None,
    marker_size: Optional[float] = None,
    line_width: Optional[float] = None,
) -> plt.Axes:
    """
    Create a paired lollipop plot.

    Displays two sets of values at each x position connected by
    vertical lines.

    Args:
        x: Categories or numeric positions for the lollipops.
        y1: First set of values.
        y2: Second set of values (required for paired plot).
        ax: Matplotlib Axes to plot on (creates new if None).
        line_color: Color of connecting lines.
        marker_size: Size of scatter markers.
        line_width: Width of connecting lines.

    Returns:
        The matplotlib Axes containing the plot.

    Example:
        >>> x = [1, 2, 3, 4]
        >>> y1 = [0.1, 0.2, 0.3, 0.4]
        >>> y2 = [0.15, 0.25, 0.35, 0.45]
        >>> lollipop_plot(x, y1, y2)
    """
    if ax is None:
        _, ax = plt.subplots()

    if y2 is None:
        raise ValueError("y2 is required for paired lollipop plot")

    line_color = line_color or rcParams["lollipop.line_color"]
    marker_size = marker_size or rcParams["lollipop.marker_size"]
    line_width = line_width or rcParams["lollipop.line_width"]

    _draw_connecting_lines(ax, x, y1, y2, line_color, line_width)
    _draw_markers(ax, x, y1, y2, marker_size)

    ax.set_xticks(list(x))
    return ax


def _draw_connecting_lines(
    ax: plt.Axes,
    x: Sequence,
    y1: Sequence,
    y2: Sequence,
    color: str,
    width: float,
) -> None:
    """Draw vertical lines connecting paired points."""
    for xi, yi1, yi2 in zip(x, y1, y2):
        ax.vlines(xi, min(yi1, yi2), max(yi1, yi2), color=color, lw=width)


def _draw_markers(
    ax: plt.Axes,
    x: Sequence,
    y1: Sequence,
    y2: Sequence,
    size: float,
) -> None:
    """Draw scatter markers for both series."""
    ax.scatter(x, y1, s=size, zorder=3)
    ax.scatter(x, y2, s=size, zorder=3)

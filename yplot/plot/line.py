"""
DataFrame-first line plot.

This module provides line plot functionality with support for
error bands, grouping, and automatic legend generation.
"""

from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from yplot.config import rcParams
from yplot.plot.base import (
    PlotData,
    apply_labels,
    extract_data,
    get_color_palette,
    get_or_create_axes,
    group_by_category,
)


def line(
    data: Optional[pd.DataFrame] = None,
    x: Optional[Union[str, np.ndarray]] = None,
    y: Optional[Union[str, np.ndarray]] = None,
    error: Optional[Union[str, np.ndarray]] = None,
    error_low: Optional[Union[str, np.ndarray]] = None,
    error_high: Optional[Union[str, np.ndarray]] = None,
    group: Optional[Union[str, np.ndarray]] = None,
    color: Optional[Union[str, np.ndarray]] = None,
    linewidth: Optional[float] = None,
    linestyle: str = "-",
    alpha: float = 1.0,
    error_alpha: float = 0.2,
    marker: Optional[str] = None,
    ax: Optional[plt.Axes] = None,
    legend: bool = True,
    **kwargs,
) -> plt.Axes:
    """
    Create a line plot from DataFrame or arrays.

    Args:
        data: DataFrame containing the data.
        x: Column name or array for x values.
        y: Column name or array for y values.
        error: Column for symmetric error (shaded band).
        error_low: Column for lower error bound.
        error_high: Column for upper error bound.
        group: Column for grouping into separate lines.
        color: Column for color assignment (or single color).
        linewidth: Line width.
        linestyle: Line style ('-', '--', ':', etc.).
        alpha: Line transparency.
        error_alpha: Error band transparency.
        marker: Marker style for data points.
        ax: Matplotlib Axes to plot on.
        legend: Whether to show legend.
        **kwargs: Additional arguments passed to ax.plot().

    Returns:
        The matplotlib Axes with the line plot.

    Example:
        >>> line(df, x='time', y='value', error='std', group='condition')
    """
    ax = get_or_create_axes(ax)
    lw = linewidth or rcParams.get("lines.linewidth", 1.0)

    plot_data = extract_data(
        data, x=x, y=y, error=error,
        error_low=error_low, error_high=error_high,
        group=group, color=color if isinstance(color, str) and data is not None else None,
    )

    # Handle color as direct value
    direct_color = color if not isinstance(color, str) or data is None else None

    _plot_lines(
        ax, plot_data, lw, linestyle, alpha, error_alpha, marker,
        legend, direct_color, **kwargs
    )
    apply_labels(ax, plot_data)

    return ax


def _plot_lines(
    ax: plt.Axes,
    plot_data: PlotData,
    linewidth: float,
    linestyle: str,
    alpha: float,
    error_alpha: float,
    marker: Optional[str],
    legend: bool,
    direct_color: Optional[str],
    **kwargs,
) -> None:
    """Render line plot, handling groups if present."""
    if plot_data.group is not None:
        _plot_grouped_lines(
            ax, plot_data, linewidth, linestyle, alpha,
            error_alpha, marker, legend, **kwargs
        )
    else:
        color = direct_color or kwargs.pop("color", None)
        _plot_single_line(
            ax, plot_data, linewidth, linestyle, alpha,
            error_alpha, marker, color, **kwargs
        )


def _plot_single_line(
    ax: plt.Axes,
    data: PlotData,
    linewidth: float,
    linestyle: str,
    alpha: float,
    error_alpha: float,
    marker: Optional[str],
    color: Optional[str],
    **kwargs,
) -> None:
    """Plot a single line with optional error band."""
    plot_kwargs = {"linewidth": linewidth, "linestyle": linestyle, "alpha": alpha}
    if color:
        plot_kwargs["color"] = color
    if marker:
        plot_kwargs["marker"] = marker

    line_obj = ax.plot(data.x, data.y, **plot_kwargs, **kwargs)
    line_color = line_obj[0].get_color()

    _add_error_band(ax, data, line_color, error_alpha)


def _plot_grouped_lines(
    ax: plt.Axes,
    plot_data: PlotData,
    linewidth: float,
    linestyle: str,
    alpha: float,
    error_alpha: float,
    marker: Optional[str],
    legend: bool,
    **kwargs,
) -> None:
    """Plot multiple lines, one per group."""
    groups = group_by_category(plot_data, "group")
    colors = get_color_palette(len(groups))

    for (cat, grp), clr in zip(groups.items(), colors):
        # Sort by x for proper line plotting
        sort_idx = np.argsort(grp.x)
        sorted_grp = PlotData(
            x=grp.x[sort_idx],
            y=grp.y[sort_idx],
            error=grp.error[sort_idx] if grp.error is not None else None,
            error_low=grp.error_low[sort_idx] if grp.error_low is not None else None,
            error_high=grp.error_high[sort_idx] if grp.error_high is not None else None,
            color=None, size=None, group=None, labels=grp.labels,
        )

        plot_kwargs = {
            "linewidth": linewidth, "linestyle": linestyle,
            "alpha": alpha, "color": clr, "label": str(cat)
        }
        if marker:
            plot_kwargs["marker"] = marker

        ax.plot(sorted_grp.x, sorted_grp.y, **plot_kwargs, **kwargs)
        _add_error_band(ax, sorted_grp, clr, error_alpha)

    if legend and len(groups) > 1:
        ax.legend()


def _add_error_band(
    ax: plt.Axes,
    data: PlotData,
    color: str,
    alpha: float,
) -> None:
    """Add error band (shaded region) to line plot."""
    if data.error is not None:
        ax.fill_between(
            data.x, data.y - data.error, data.y + data.error,
            color=color, alpha=alpha
        )
    elif data.error_low is not None and data.error_high is not None:
        ax.fill_between(
            data.x, data.error_low, data.error_high,
            color=color, alpha=alpha
        )

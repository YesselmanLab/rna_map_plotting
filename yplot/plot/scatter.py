"""
DataFrame-first scatter plot.

This module provides scatter plot functionality with support for
color coding, size mapping, and automatic legend generation.
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


def scatter(
    data: Optional[pd.DataFrame] = None,
    x: Optional[Union[str, np.ndarray]] = None,
    y: Optional[Union[str, np.ndarray]] = None,
    color: Optional[Union[str, np.ndarray]] = None,
    size: Optional[Union[str, np.ndarray, float]] = None,
    alpha: float = 1.0,
    marker: str = "o",
    ax: Optional[plt.Axes] = None,
    legend: bool = True,
    **kwargs,
) -> plt.Axes:
    """
    Create a scatter plot from DataFrame or arrays.

    Args:
        data: DataFrame containing the data.
        x: Column name or array for x values.
        y: Column name or array for y values.
        color: Column name for color grouping, or array of colors.
        size: Column name, array, or scalar for marker sizes.
        alpha: Marker transparency (0-1).
        marker: Marker style.
        ax: Matplotlib Axes to plot on.
        legend: Whether to show legend when color groups exist.
        **kwargs: Additional arguments passed to ax.scatter().

    Returns:
        The matplotlib Axes with the scatter plot.

    Example:
        >>> scatter(df, x='concentration', y='response', color='treatment')
        >>> scatter(x=[1,2,3], y=[4,5,6], size=50, ax=ax)
    """
    ax = get_or_create_axes(ax)

    plot_data = extract_data(
        data, x=x, y=y, color=color,
        size=size if isinstance(size, str) else None,
    )

    # Handle size as scalar or array
    if isinstance(size, (int, float)):
        marker_size = size
    elif plot_data.size is not None:
        marker_size = plot_data.size
    else:
        marker_size = rcParams["scatter.marker_size"]

    _plot_scatter(ax, plot_data, marker_size, alpha, marker, legend, **kwargs)
    apply_labels(ax, plot_data)

    return ax


def _plot_scatter(
    ax: plt.Axes,
    plot_data: PlotData,
    size: Union[float, np.ndarray],
    alpha: float,
    marker: str,
    legend: bool,
    **kwargs,
) -> None:
    """Render scatter plot, handling color groups if present."""
    if plot_data.color is not None and _is_categorical(plot_data.color):
        _plot_grouped_scatter(ax, plot_data, size, alpha, marker, legend, **kwargs)
    else:
        color = kwargs.pop("c", kwargs.pop("color", None))
        if plot_data.color is not None:
            color = plot_data.color
        ax.scatter(
            plot_data.x, plot_data.y,
            s=size, alpha=alpha, marker=marker, c=color, **kwargs
        )


def _plot_grouped_scatter(
    ax: plt.Axes,
    plot_data: PlotData,
    size: Union[float, np.ndarray],
    alpha: float,
    marker: str,
    legend: bool,
    **kwargs,
) -> None:
    """Plot scatter with different colors per group."""
    groups = group_by_category(plot_data, "color")
    colors = get_color_palette(len(groups))

    for (cat, grp), clr in zip(groups.items(), colors):
        grp_size = size if isinstance(size, (int, float)) else size[plot_data.color == cat]
        ax.scatter(
            grp.x, grp.y,
            s=grp_size, alpha=alpha, marker=marker, color=clr,
            label=str(cat), **kwargs
        )

    if legend and len(groups) > 1:
        ax.legend()


def _is_categorical(arr: np.ndarray) -> bool:
    """Check if array should be treated as categorical."""
    if arr.dtype == object:
        return True
    if np.issubdtype(arr.dtype, np.str_):
        return True
    unique_ratio = len(np.unique(arr)) / len(arr)
    return unique_ratio < 0.1 and len(np.unique(arr)) <= 20

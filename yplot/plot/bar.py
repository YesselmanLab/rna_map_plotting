"""
DataFrame-first bar plots.

This module provides bar plot functionality with support for
error bars, grouping, and horizontal orientation.
"""

from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from yplot.plot.base import (
    apply_labels,
    extract_data,
    get_color_palette,
    get_or_create_axes,
)


def bar(
    data: Optional[pd.DataFrame] = None,
    x: Optional[Union[str, np.ndarray]] = None,
    y: Optional[Union[str, np.ndarray]] = None,
    error: Optional[Union[str, np.ndarray]] = None,
    color: Optional[Union[str, list[str]]] = None,
    width: float = 0.8,
    alpha: float = 1.0,
    orientation: str = "vertical",
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> plt.Axes:
    """
    Create a bar plot from DataFrame or arrays.

    Args:
        data: DataFrame containing the data.
        x: Column name or array for categories.
        y: Column name or array for bar heights.
        error: Column name or array for error bars.
        color: Single color, list of colors, or column name.
        width: Bar width.
        alpha: Bar transparency.
        orientation: 'vertical' or 'horizontal'.
        ax: Matplotlib Axes to plot on.
        **kwargs: Additional arguments passed to ax.bar().

    Returns:
        The matplotlib Axes with the bar plot.

    Example:
        >>> bar(df, x='condition', y='mean_value', error='std_value')
    """
    ax = get_or_create_axes(ax)

    plot_data = extract_data(data, x=x, y=y, error=error)

    # Handle colors
    if isinstance(color, str) and data is not None and color in data.columns:
        bar_colors = data[color].tolist()
    elif isinstance(color, list):
        bar_colors = color
    elif color is not None:
        bar_colors = color
    else:
        bar_colors = get_color_palette(1)[0]

    _plot_bars(
        ax, plot_data, bar_colors, width, alpha, orientation, **kwargs
    )
    apply_labels(ax, plot_data)

    return ax


def _plot_bars(
    ax: plt.Axes,
    plot_data,
    color,
    width: float,
    alpha: float,
    orientation: str,
    **kwargs,
) -> None:
    """Render bar plot."""
    x_vals = plot_data.x
    y_vals = plot_data.y
    err = plot_data.error

    # Convert categorical x to positions
    if x_vals is not None and x_vals.dtype == object:
        x_labels = x_vals
        x_positions = np.arange(len(x_labels))
    else:
        x_positions = x_vals if x_vals is not None else np.arange(len(y_vals))
        x_labels = None

    if orientation == "vertical":
        ax.bar(
            x_positions, y_vals, width=width, color=color,
            alpha=alpha, yerr=err, capsize=2, **kwargs
        )
        if x_labels is not None:
            ax.set_xticks(x_positions)
            ax.set_xticklabels(x_labels)
    else:
        ax.barh(
            x_positions, y_vals, height=width, color=color,
            alpha=alpha, xerr=err, capsize=2, **kwargs
        )
        if x_labels is not None:
            ax.set_yticks(x_positions)
            ax.set_yticklabels(x_labels)


def grouped_bar(
    data: pd.DataFrame,
    x: str,
    y: str,
    group: str,
    error: Optional[str] = None,
    width: float = 0.8,
    alpha: float = 1.0,
    ax: Optional[plt.Axes] = None,
    legend: bool = True,
    **kwargs,
) -> plt.Axes:
    """
    Create a grouped bar plot from DataFrame.

    Args:
        data: DataFrame containing the data.
        x: Column name for categories on x-axis.
        y: Column name for bar heights.
        group: Column name for grouping (creates side-by-side bars).
        error: Column name for error bars.
        width: Total width for each group of bars.
        alpha: Bar transparency.
        ax: Matplotlib Axes to plot on.
        legend: Whether to show legend.
        **kwargs: Additional arguments passed to ax.bar().

    Returns:
        The matplotlib Axes with the grouped bar plot.

    Example:
        >>> grouped_bar(df, x='condition', y='value', group='treatment')
    """
    ax = get_or_create_axes(ax)

    categories = data[x].unique()
    groups = data[group].unique()
    n_groups = len(groups)
    colors = get_color_palette(n_groups)

    bar_width = width / n_groups
    x_positions = np.arange(len(categories))

    for i, grp in enumerate(groups):
        grp_data = data[data[group] == grp]
        offset = (i - n_groups / 2 + 0.5) * bar_width

        # Get values aligned with categories
        values = []
        errors = [] if error else None
        for cat in categories:
            cat_data = grp_data[grp_data[x] == cat]
            values.append(cat_data[y].values[0] if len(cat_data) else 0)
            if error:
                errors.append(cat_data[error].values[0] if len(cat_data) else 0)

        ax.bar(
            x_positions + offset, values, bar_width,
            color=colors[i], alpha=alpha, label=str(grp),
            yerr=errors, capsize=2, **kwargs
        )

    ax.set_xticks(x_positions)
    ax.set_xticklabels(categories)
    ax.set_xlabel(x)
    ax.set_ylabel(y)

    if legend:
        ax.legend(title=group)

    return ax

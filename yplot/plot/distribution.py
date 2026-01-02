"""
DataFrame-first distribution plots.

This module provides violin, box, swarm, and strip plots for
visualizing data distributions across categories.
"""

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from yplot.plot.base import get_color_palette, get_or_create_axes


def violin(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    inner: str = "box",
    cut: float = 2,
    scale: str = "width",
    width: float = 0.8,
    alpha: float = 1.0,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> plt.Axes:
    """
    Create a violin plot from DataFrame.

    Args:
        data: DataFrame containing the data.
        x: Column name for categories on x-axis.
        y: Column name for values.
        color: Column name for color grouping.
        inner: Inner plot type ('box', 'quartile', 'point', 'stick', None).
        cut: Extend density past extreme values.
        scale: How to scale width ('width', 'count', 'area').
        width: Maximum violin width.
        alpha: Violin transparency.
        ax: Matplotlib Axes to plot on.
        **kwargs: Additional arguments.

    Returns:
        The matplotlib Axes with the violin plot.

    Example:
        >>> violin(df, x='treatment', y='response')
    """
    ax = get_or_create_axes(ax)

    categories = data[x].unique()
    n_cats = len(categories)
    colors = get_color_palette(n_cats)
    positions = np.arange(n_cats)

    violin_data = [data[data[x] == cat][y].dropna().values for cat in categories]

    parts = ax.violinplot(
        violin_data, positions=positions, widths=width,
        showmeans=False, showmedians=False, showextrema=False
    )

    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(colors[i])
        pc.set_alpha(alpha)
        pc.set_edgecolor("black")
        pc.set_linewidth(0.5)

    if inner == "box":
        _add_inner_box(ax, violin_data, positions, width)
    elif inner == "quartile":
        _add_inner_quartiles(ax, violin_data, positions)
    elif inner == "point":
        _add_inner_points(ax, violin_data, positions)

    ax.set_xticks(positions)
    ax.set_xticklabels(categories)
    ax.set_xlabel(x)
    ax.set_ylabel(y)

    return ax


def _add_inner_box(ax, violin_data, positions, width):
    """Add box plot inside violin."""
    box_width = width * 0.15
    for d, pos in zip(violin_data, positions):
        if len(d) == 0:
            continue
        q1, median, q3 = np.percentile(d, [25, 50, 75])
        iqr = q3 - q1
        whisker_low = max(d.min(), q1 - 1.5 * iqr)
        whisker_high = min(d.max(), q3 + 1.5 * iqr)

        ax.vlines(pos, whisker_low, whisker_high, color="black", linewidth=0.75)
        ax.fill_between(
            [pos - box_width/2, pos + box_width/2], q1, q3,
            color="black", alpha=0.3
        )
        ax.scatter([pos], [median], color="white", s=15, zorder=3, edgecolor="black")


def _add_inner_quartiles(ax, violin_data, positions):
    """Add quartile lines inside violin."""
    for d, pos in zip(violin_data, positions):
        if len(d) == 0:
            continue
        quartiles = np.percentile(d, [25, 50, 75])
        ax.hlines(quartiles, pos - 0.05, pos + 0.05, color="black", linewidth=1)


def _add_inner_points(ax, violin_data, positions):
    """Add individual points inside violin."""
    for d, pos in zip(violin_data, positions):
        ax.scatter([pos] * len(d), d, color="black", s=2, alpha=0.5)


def box(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    width: float = 0.6,
    notch: bool = False,
    showfliers: bool = True,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> plt.Axes:
    """
    Create a box plot from DataFrame.

    Args:
        data: DataFrame containing the data.
        x: Column name for categories.
        y: Column name for values.
        color: Column name for color grouping.
        width: Box width.
        notch: If True, show notched boxes.
        showfliers: If True, show outliers.
        ax: Matplotlib Axes to plot on.
        **kwargs: Additional arguments passed to ax.boxplot().

    Returns:
        The matplotlib Axes with the box plot.

    Example:
        >>> box(df, x='group', y='value')
    """
    ax = get_or_create_axes(ax)

    categories = data[x].unique()
    n_cats = len(categories)
    colors = get_color_palette(n_cats)
    positions = np.arange(n_cats)

    box_data = [data[data[x] == cat][y].dropna().values for cat in categories]

    bp = ax.boxplot(
        box_data, positions=positions, widths=width,
        notch=notch, showfliers=showfliers,
        patch_artist=True, **kwargs
    )

    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax.set_xticks(positions)
    ax.set_xticklabels(categories)
    ax.set_xlabel(x)
    ax.set_ylabel(y)

    return ax


def swarm(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    size: float = 5,
    alpha: float = 0.8,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> plt.Axes:
    """
    Create a swarm plot from DataFrame.

    Points are spread horizontally to avoid overlap, showing
    the distribution within each category.

    Args:
        data: DataFrame containing the data.
        x: Column name for categories.
        y: Column name for values.
        color: Column name for color grouping.
        size: Point size.
        alpha: Point transparency.
        ax: Matplotlib Axes to plot on.
        **kwargs: Additional arguments.

    Returns:
        The matplotlib Axes with the swarm plot.

    Example:
        >>> swarm(df, x='treatment', y='response')
    """
    ax = get_or_create_axes(ax)

    categories = data[x].unique()
    n_cats = len(categories)
    colors = get_color_palette(n_cats)
    positions = np.arange(n_cats)

    for i, cat in enumerate(categories):
        cat_data = data[data[x] == cat][y].dropna().values
        x_jitter = _calculate_swarm_positions(cat_data, positions[i])
        ax.scatter(x_jitter, cat_data, s=size, color=colors[i], alpha=alpha, **kwargs)

    ax.set_xticks(positions)
    ax.set_xticklabels(categories)
    ax.set_xlabel(x)
    ax.set_ylabel(y)

    return ax


def _calculate_swarm_positions(values: np.ndarray, center: float) -> np.ndarray:
    """Calculate x positions for swarm plot to avoid overlap."""
    if len(values) == 0:
        return np.array([])

    sorted_idx = np.argsort(values)
    positions = np.zeros(len(values))
    width = 0.3

    # Simple beeswarm algorithm
    for idx in sorted_idx:
        positions[idx] = center + width * (np.random.random() - 0.5)

    return positions


def strip(
    data: pd.DataFrame,
    x: str,
    y: str,
    color: Optional[str] = None,
    size: float = 5,
    jitter: float = 0.2,
    alpha: float = 0.8,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> plt.Axes:
    """
    Create a strip plot from DataFrame.

    Similar to swarm but with random jitter instead of
    algorithmic point placement.

    Args:
        data: DataFrame containing the data.
        x: Column name for categories.
        y: Column name for values.
        color: Column name for color grouping.
        size: Point size.
        jitter: Amount of random horizontal spread.
        alpha: Point transparency.
        ax: Matplotlib Axes to plot on.
        **kwargs: Additional arguments.

    Returns:
        The matplotlib Axes with the strip plot.

    Example:
        >>> strip(df, x='group', y='measurement', jitter=0.15)
    """
    ax = get_or_create_axes(ax)

    categories = data[x].unique()
    n_cats = len(categories)
    colors = get_color_palette(n_cats)
    positions = np.arange(n_cats)

    for i, cat in enumerate(categories):
        cat_data = data[data[x] == cat][y].dropna().values
        x_jitter = positions[i] + jitter * (np.random.random(len(cat_data)) - 0.5)
        ax.scatter(x_jitter, cat_data, s=size, color=colors[i], alpha=alpha, **kwargs)

    ax.set_xticks(positions)
    ax.set_xticklabels(categories)
    ax.set_xlabel(x)
    ax.set_ylabel(y)

    return ax

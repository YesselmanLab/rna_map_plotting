"""
DataFrame-first matrix plots.

This module provides heatmap and correlation matrix visualization.
"""

from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import Normalize

from yplot.plot.base import get_or_create_axes


def heatmap(
    data: Union[pd.DataFrame, np.ndarray],
    x: Optional[str] = None,
    y: Optional[str] = None,
    values: Optional[str] = None,
    cmap: str = "viridis",
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    center: Optional[float] = None,
    annot: bool = False,
    fmt: str = ".2f",
    annot_size: int = 8,
    linewidths: float = 0,
    linecolor: str = "white",
    cbar: bool = True,
    cbar_label: Optional[str] = None,
    square: bool = False,
    xticklabels: Union[bool, list] = True,
    yticklabels: Union[bool, list] = True,
    ax: Optional[plt.Axes] = None,
    **kwargs,
) -> plt.Axes:
    """
    Create a heatmap from DataFrame or 2D array.

    Args:
        data: DataFrame or 2D array. If DataFrame with x, y, values columns,
              will pivot to matrix form.
        x: Column name for x-axis categories (for long-form data).
        y: Column name for y-axis categories (for long-form data).
        values: Column name for cell values (for long-form data).
        cmap: Colormap name.
        vmin: Minimum value for color scale.
        vmax: Maximum value for color scale.
        center: Center value for diverging colormaps.
        annot: If True, annotate cells with values.
        fmt: String format for annotations.
        annot_size: Font size for annotations.
        linewidths: Width of lines between cells.
        linecolor: Color of lines between cells.
        cbar: Whether to show colorbar.
        cbar_label: Label for colorbar.
        square: If True, make cells square.
        xticklabels: Labels for x-axis, or True for column names.
        yticklabels: Labels for y-axis, or True for row names.
        ax: Matplotlib Axes to plot on.
        **kwargs: Additional arguments passed to ax.pcolormesh().

    Returns:
        The matplotlib Axes with the heatmap.

    Example:
        >>> heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        >>> heatmap(df, x='column', y='row', values='value')
    """
    ax = get_or_create_axes(ax)

    matrix, row_labels, col_labels = _prepare_matrix(data, x, y, values)

    # Set up color normalization
    norm = _get_normalization(matrix, vmin, vmax, center)

    # Create heatmap
    mesh = ax.pcolormesh(
        matrix, cmap=cmap, norm=norm,
        edgecolors=linecolor, linewidths=linewidths, **kwargs
    )

    # Configure axes
    _configure_heatmap_axes(
        ax, matrix, row_labels, col_labels,
        xticklabels, yticklabels, square
    )

    # Add annotations
    if annot:
        _add_annotations(ax, matrix, fmt, annot_size)

    # Add colorbar
    if cbar:
        cb = ax.figure.colorbar(mesh, ax=ax)
        if cbar_label:
            cb.set_label(cbar_label)

    return ax


def _prepare_matrix(
    data: Union[pd.DataFrame, np.ndarray],
    x: Optional[str],
    y: Optional[str],
    values: Optional[str],
) -> tuple[np.ndarray, list, list]:
    """Convert data to matrix form with labels."""
    if isinstance(data, np.ndarray):
        return data, list(range(data.shape[0])), list(range(data.shape[1]))

    if x is not None and y is not None and values is not None:
        # Long-form data - pivot to matrix
        pivot = data.pivot(index=y, columns=x, values=values)
        return pivot.values, list(pivot.index), list(pivot.columns)

    # Already matrix-form DataFrame
    return data.values, list(data.index), list(data.columns)


def _get_normalization(
    matrix: np.ndarray,
    vmin: Optional[float],
    vmax: Optional[float],
    center: Optional[float],
) -> Normalize:
    """Get color normalization for heatmap."""
    if center is not None:
        # Diverging colormap centered at a value
        abs_max = max(
            abs(np.nanmin(matrix) - center),
            abs(np.nanmax(matrix) - center)
        )
        return Normalize(vmin=center - abs_max, vmax=center + abs_max)

    data_min = vmin if vmin is not None else np.nanmin(matrix)
    data_max = vmax if vmax is not None else np.nanmax(matrix)
    return Normalize(vmin=data_min, vmax=data_max)


def _configure_heatmap_axes(
    ax: plt.Axes,
    matrix: np.ndarray,
    row_labels: list,
    col_labels: list,
    xticklabels: Union[bool, list],
    yticklabels: Union[bool, list],
    square: bool,
) -> None:
    """Configure axes for heatmap display."""
    n_rows, n_cols = matrix.shape

    # Set tick positions
    ax.set_xticks(np.arange(n_cols) + 0.5)
    ax.set_yticks(np.arange(n_rows) + 0.5)

    # Set tick labels
    if xticklabels is True:
        ax.set_xticklabels(col_labels, rotation=45, ha="right")
    elif xticklabels is False:
        ax.set_xticklabels([])
    else:
        ax.set_xticklabels(xticklabels, rotation=45, ha="right")

    if yticklabels is True:
        ax.set_yticklabels(row_labels)
    elif yticklabels is False:
        ax.set_yticklabels([])
    else:
        ax.set_yticklabels(yticklabels)

    # Invert y-axis so first row is at top
    ax.invert_yaxis()

    if square:
        ax.set_aspect("equal")


def _add_annotations(
    ax: plt.Axes,
    matrix: np.ndarray,
    fmt: str,
    fontsize: int,
) -> None:
    """Add value annotations to heatmap cells."""
    n_rows, n_cols = matrix.shape

    for i in range(n_rows):
        for j in range(n_cols):
            val = matrix[i, j]
            if np.isnan(val):
                continue

            # Choose text color based on background
            text_color = _get_text_color(val, matrix)
            text = format(val, fmt)

            ax.text(
                j + 0.5, i + 0.5, text,
                ha="center", va="center",
                fontsize=fontsize, color=text_color
            )


def _get_text_color(value: float, matrix: np.ndarray) -> str:
    """Get text color for annotation based on background value."""
    vmin = np.nanmin(matrix)
    vmax = np.nanmax(matrix)
    normalized = (value - vmin) / (vmax - vmin) if vmax != vmin else 0.5
    return "white" if normalized > 0.5 else "black"

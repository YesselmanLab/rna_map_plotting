"""
Scatter plot utilities.

This module provides functions for creating scatter plots with
optional regression lines and annotations.
"""

from typing import Any, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from yplot.config import rcParams
from yplot.plots.regression import plot_regression_line


def scatter_plot_w_regression(
    data: Optional[pd.DataFrame] = None,
    ax: Optional[plt.Axes] = None,
    x: Optional[Union[str, np.ndarray]] = None,
    y: Optional[Union[str, np.ndarray]] = None,
    pos: str = "top left",
    size: Optional[float] = None,
    fontsize: Optional[int] = None,
) -> plt.Axes:
    """
    Create a scatter plot with linear regression line.

    Args:
        data: Optional DataFrame containing x and y columns.
        ax: Matplotlib Axes to plot on (creates new if None).
        x: Column name or array for x values.
        y: Column name or array for y values.
        pos: Position for R-squared annotation.
        size: Marker size (uses rcParams default if None).
        fontsize: Font size for annotation.

    Returns:
        The matplotlib Axes with the scatter plot.

    Example:
        >>> scatter_plot_w_regression(df, x='col1', y='col2')
        >>> scatter_plot_w_regression(x=x_array, y=y_array, ax=ax)
    """
    if ax is None:
        _, ax = plt.subplots()

    x_vals, y_vals = _extract_xy(data, x, y)
    x_arr = np.array(x_vals).reshape(-1, 1)
    y_arr = np.array(y_vals)

    marker_size = size if size is not None else rcParams["scatter.marker_size"]
    ax.scatter(x_arr, y_arr, s=marker_size)
    plot_regression_line(x_arr, y_arr, ax, r2_pos=pos, r2_fontsize=fontsize)

    return ax


def _extract_xy(
    data: Optional[pd.DataFrame],
    x: Any,
    y: Any,
) -> tuple:
    """Extract x and y arrays from DataFrame or direct input."""
    if data is not None and isinstance(x, str) and isinstance(y, str):
        return data[x], data[y]
    return x, y

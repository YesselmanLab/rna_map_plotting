"""
Regression line plotting utilities.

This module provides functions for adding regression lines and
R-squared annotations to scatter plots.
"""

from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from yplot.config import rcParams


def plot_regression_line(
    x: np.ndarray,
    y: np.ndarray,
    ax: plt.Axes,
    show_r2: bool = True,
    r2_pos: str = "upper left",
    r2_fontsize: Optional[int] = None,
) -> float:
    """
    Add a linear regression line to a plot.

    Args:
        x: X values (will be reshaped to 2D for sklearn).
        y: Y values.
        ax: The matplotlib Axes to plot on.
        show_r2: Whether to display R-squared value (default: True).
        r2_pos: Position for R-squared text annotation.
        r2_fontsize: Font size for R-squared text.

    Returns:
        The R-squared value of the regression.
    """
    x_2d = x.reshape(-1, 1) if x.ndim == 1 else x

    model = LinearRegression()
    model.fit(x_2d, y)
    r2 = r2_score(y, model.predict(x_2d))

    x_pred = np.linspace(x.min(), x.max(), 1000).reshape(-1, 1)
    ax.plot(
        x_pred,
        model.predict(x_pred),
        color=rcParams["regression.color"],
        linewidth=rcParams["regression.linewidth"],
        linestyle=rcParams["regression.linestyle"],
    )

    if show_r2:
        _add_r2_annotation(ax, r2, r2_pos, r2_fontsize)

    return r2


def _add_r2_annotation(
    ax: plt.Axes,
    r2: float,
    pos: str,
    fontsize: Optional[int],
) -> None:
    """Add R-squared annotation to axes."""
    fontsize = fontsize or rcParams["corner_text.fontsize"]
    font_family = rcParams["font.family"]

    positions = {
        "upper left": (0.03, 0.97, "top", "left"),
        "upper right": (0.97, 0.97, "top", "right"),
        "lower left": (0.03, 0.03, "bottom", "left"),
        "lower right": (0.97, 0.03, "bottom", "right"),
    }

    if pos not in positions:
        pos = "upper left"

    x, y, va, ha = positions[pos]
    ax.text(
        x, y, f"R² = {r2:.2f}",
        transform=ax.transAxes,
        fontsize=fontsize,
        fontname=font_family,
        verticalalignment=va,
        horizontalalignment=ha,
    )

"""
Statistical annotation functions.

This module provides functions for adding significance brackets,
p-values, and statistical annotations to matplotlib plots.
"""

from typing import Optional

import matplotlib.pyplot as plt

from yplot.config import rcParams


def add_significance(
    ax: plt.Axes,
    x1: float,
    x2: float,
    y: float,
    pvalue: float,
    height: float = 0.03,
    fontsize: Optional[int] = None,
    color: str = "black",
    use_stars: bool = True,
    **kwargs,
) -> None:
    """
    Add a significance bracket between two positions.

    Args:
        ax: Matplotlib Axes to annotate.
        x1: Left x position.
        x2: Right x position.
        y: Y position (in data coordinates).
        pvalue: P-value for significance level.
        height: Bracket height as fraction of y-range.
        fontsize: Font size for annotation text.
        color: Color for bracket and text.
        use_stars: If True, use star notation; else show p-value.
        **kwargs: Additional arguments for text.

    Example:
        >>> add_significance(ax, 0, 1, 0.95, pvalue=0.01)
    """
    fontsize = fontsize or rcParams.get("font.size", 8)

    # Get y range and calculate bracket positions
    y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
    bracket_height = height * y_range

    # Draw bracket
    significance_bracket(
        ax, x1, x2, y, bracket_height, color=color
    )

    # Add text
    text = star_notation(pvalue) if use_stars else f"p={pvalue:.3g}"
    mid_x = (x1 + x2) / 2
    ax.text(
        mid_x, y + bracket_height + 0.01 * y_range, text,
        ha="center", va="bottom", fontsize=fontsize,
        color=color, **kwargs
    )


def add_pvalue(
    ax: plt.Axes,
    x: float,
    y: float,
    pvalue: float,
    format_str: str = "p = {:.3g}",
    fontsize: Optional[int] = None,
    color: str = "black",
    **kwargs,
) -> None:
    """
    Add a formatted p-value annotation.

    Args:
        ax: Matplotlib Axes to annotate.
        x: X position (in data coordinates).
        y: Y position (in data coordinates).
        pvalue: P-value to display.
        format_str: Format string for p-value.
        fontsize: Font size for text.
        color: Text color.
        **kwargs: Additional arguments for ax.text().

    Example:
        >>> add_pvalue(ax, 0.5, 0.9, 0.034)
    """
    fontsize = fontsize or rcParams.get("font.size", 8)

    if pvalue < 0.001:
        text = "p < 0.001"
    else:
        text = format_str.format(pvalue)

    ax.text(x, y, text, fontsize=fontsize, color=color, **kwargs)


def significance_bracket(
    ax: plt.Axes,
    x1: float,
    x2: float,
    y: float,
    height: float,
    color: str = "black",
    linewidth: float = 1.0,
) -> None:
    """
    Draw a significance bracket (horizontal line with downward tips).

    Args:
        ax: Matplotlib Axes to draw on.
        x1: Left x position.
        x2: Right x position.
        y: Y position of bracket base.
        height: Height of bracket tips.
        color: Bracket color.
        linewidth: Line width.

    Example:
        >>> significance_bracket(ax, 0, 1, 0.9, 0.05)
    """
    # Horizontal line
    ax.plot([x1, x1, x2, x2], [y, y + height, y + height, y],
            color=color, linewidth=linewidth, clip_on=False)


def star_notation(pvalue: float) -> str:
    """
    Convert p-value to star notation.

    Args:
        pvalue: P-value to convert.

    Returns:
        Star notation string (*, **, ***, or n.s.).

    Example:
        >>> star_notation(0.001)
        '***'
    """
    if pvalue < 0.001:
        return "***"
    elif pvalue < 0.01:
        return "**"
    elif pvalue < 0.05:
        return "*"
    else:
        return "n.s."


def add_significance_bars(
    ax: plt.Axes,
    comparisons: list[tuple[int, int, float]],
    y_start: Optional[float] = None,
    y_step: float = 0.08,
    fontsize: Optional[int] = None,
    color: str = "black",
    use_stars: bool = True,
) -> None:
    """
    Add multiple significance brackets at staggered heights.

    Args:
        ax: Matplotlib Axes to annotate.
        comparisons: List of (x1, x2, pvalue) tuples.
        y_start: Starting y position (auto if None).
        y_step: Vertical step between brackets as fraction of range.
        fontsize: Font size for annotations.
        color: Color for brackets and text.
        use_stars: If True, use star notation.

    Example:
        >>> comparisons = [(0, 1, 0.01), (0, 2, 0.001), (1, 2, 0.05)]
        >>> add_significance_bars(ax, comparisons)
    """
    if y_start is None:
        y_min, y_max = ax.get_ylim()
        y_start = y_max + 0.05 * (y_max - y_min)

    y_range = ax.get_ylim()[1] - ax.get_ylim()[0]
    current_y = y_start

    for x1, x2, pvalue in comparisons:
        add_significance(
            ax, x1, x2, current_y, pvalue,
            fontsize=fontsize, color=color, use_stars=use_stars
        )
        current_y += y_step * y_range


def add_regression_stats(
    ax: plt.Axes,
    r_squared: float,
    pvalue: Optional[float] = None,
    slope: Optional[float] = None,
    intercept: Optional[float] = None,
    loc: str = "upper left",
    fontsize: Optional[int] = None,
    **kwargs,
) -> None:
    """
    Add regression statistics annotation.

    Args:
        ax: Matplotlib Axes to annotate.
        r_squared: R-squared value.
        pvalue: P-value for regression.
        slope: Regression slope.
        intercept: Regression intercept.
        loc: Location string for annotation.
        fontsize: Font size.
        **kwargs: Additional arguments for ax.text().

    Example:
        >>> add_regression_stats(ax, r_squared=0.85, pvalue=0.001)
    """
    fontsize = fontsize or rcParams.get("font.size", 8)

    lines = [f"R² = {r_squared:.3f}"]
    if pvalue is not None:
        lines.append(f"p = {pvalue:.3g}")
    if slope is not None and intercept is not None:
        sign = "+" if intercept >= 0 else ""
        lines.append(f"y = {slope:.3f}x {sign}{intercept:.3f}")

    text = "\n".join(lines)

    # Position based on loc
    x, y, ha, va = _get_position_from_loc(loc)

    ax.text(
        x, y, text, transform=ax.transAxes,
        fontsize=fontsize, ha=ha, va=va,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        **kwargs
    )


def _get_position_from_loc(loc: str) -> tuple[float, float, str, str]:
    """Get x, y, ha, va from location string."""
    positions = {
        "upper left": (0.05, 0.95, "left", "top"),
        "upper right": (0.95, 0.95, "right", "top"),
        "lower left": (0.05, 0.05, "left", "bottom"),
        "lower right": (0.95, 0.05, "right", "bottom"),
        "center": (0.5, 0.5, "center", "center"),
    }
    return positions.get(loc, positions["upper left"])

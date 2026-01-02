"""
Visual annotation elements.

This module provides functions for adding arrows, scale bars,
callouts, and text boxes to matplotlib plots.
"""

from typing import Optional

import matplotlib.pyplot as plt

from yplot.config import rcParams


def add_arrow(
    ax: plt.Axes,
    x_start: float,
    y_start: float,
    x_end: float,
    y_end: float,
    text: Optional[str] = None,
    text_offset: tuple[float, float] = (0, 0.02),
    color: str = "black",
    linewidth: float = 1.0,
    head_width: float = 0.05,
    head_length: float = 0.03,
    fontsize: Optional[int] = None,
    arrowstyle: str = "->",
    **kwargs,
) -> None:
    """
    Add an arrow annotation to the plot.

    Args:
        ax: Matplotlib Axes to annotate.
        x_start: Starting x position.
        y_start: Starting y position.
        x_end: Ending x position (arrow tip).
        y_end: Ending y position (arrow tip).
        text: Optional text label for arrow.
        text_offset: Offset for text from arrow start.
        color: Arrow color.
        linewidth: Arrow line width.
        head_width: Arrow head width.
        head_length: Arrow head length.
        fontsize: Font size for text.
        arrowstyle: Style of arrow ('->', '-|>', etc.).
        **kwargs: Additional arguments.

    Example:
        >>> add_arrow(ax, 0.2, 0.8, 0.4, 0.6, text="Important point")
    """
    fontsize = fontsize or rcParams.get("font.size", 8)

    ax.annotate(
        "",
        xy=(x_end, y_end),
        xytext=(x_start, y_start),
        arrowprops=dict(
            arrowstyle=arrowstyle,
            color=color,
            lw=linewidth,
        ),
        **kwargs
    )

    if text:
        ax.text(
            x_start + text_offset[0],
            y_start + text_offset[1],
            text,
            fontsize=fontsize,
            color=color,
            ha="center",
        )


def add_scale_bar(
    ax: plt.Axes,
    length: float,
    label: Optional[str] = None,
    loc: str = "lower right",
    pad: float = 0.05,
    color: str = "black",
    linewidth: float = 2.0,
    fontsize: Optional[int] = None,
    unit: str = "",
    **kwargs,
) -> None:
    """
    Add a scale bar to the plot.

    Args:
        ax: Matplotlib Axes to annotate.
        length: Length of scale bar in data units.
        label: Label text (if None, uses length + unit).
        loc: Location ('lower right', 'lower left', etc.).
        pad: Padding from axes edge as fraction.
        color: Scale bar color.
        linewidth: Scale bar line width.
        fontsize: Font size for label.
        unit: Unit string to append to length.
        **kwargs: Additional arguments.

    Example:
        >>> add_scale_bar(ax, 100, unit="nm", loc="lower right")
    """
    fontsize = fontsize or rcParams.get("font.size", 8)

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    y_range = ylim[1] - ylim[0]

    # Calculate position based on loc
    x, y = _get_scale_bar_position(loc, xlim, ylim, pad, length)

    # Draw scale bar
    ax.plot([x, x + length], [y, y], color=color, linewidth=linewidth,
            solid_capstyle="butt", clip_on=False)

    # Add end caps
    cap_height = 0.02 * y_range
    ax.plot([x, x], [y - cap_height/2, y + cap_height/2],
            color=color, linewidth=linewidth, clip_on=False)
    ax.plot([x + length, x + length], [y - cap_height/2, y + cap_height/2],
            color=color, linewidth=linewidth, clip_on=False)

    # Add label
    if label is None:
        label = f"{length} {unit}".strip()

    ax.text(
        x + length/2, y - 0.03 * y_range, label,
        ha="center", va="top", fontsize=fontsize, color=color
    )


def _get_scale_bar_position(
    loc: str,
    xlim: tuple[float, float],
    ylim: tuple[float, float],
    pad: float,
    length: float,
) -> tuple[float, float]:
    """Calculate scale bar position from location string."""
    x_range = xlim[1] - xlim[0]
    y_range = ylim[1] - ylim[0]

    positions = {
        "lower right": (xlim[1] - pad * x_range - length, ylim[0] + pad * y_range),
        "lower left": (xlim[0] + pad * x_range, ylim[0] + pad * y_range),
        "upper right": (xlim[1] - pad * x_range - length, ylim[1] - pad * y_range),
        "upper left": (xlim[0] + pad * x_range, ylim[1] - pad * y_range),
    }
    return positions.get(loc, positions["lower right"])


def add_callout(
    ax: plt.Axes,
    x: float,
    y: float,
    text: str,
    text_x: float,
    text_y: float,
    color: str = "black",
    fontsize: Optional[int] = None,
    arrowstyle: str = "->",
    boxstyle: str = "round,pad=0.3",
    facecolor: str = "white",
    edgecolor: Optional[str] = None,
    alpha: float = 0.9,
    **kwargs,
) -> None:
    """
    Add a callout annotation pointing to a specific location.

    Args:
        ax: Matplotlib Axes to annotate.
        x: X position to point at.
        y: Y position to point at.
        text: Callout text.
        text_x: X position for text box.
        text_y: Y position for text box.
        color: Text and arrow color.
        fontsize: Font size.
        arrowstyle: Style of arrow.
        boxstyle: Style of text box.
        facecolor: Text box background color.
        edgecolor: Text box edge color (defaults to color).
        alpha: Text box transparency.
        **kwargs: Additional arguments for annotate.

    Example:
        >>> add_callout(ax, 0.5, 0.8, "Peak value", 0.7, 0.9)
    """
    fontsize = fontsize or rcParams.get("font.size", 8)
    edgecolor = edgecolor or color

    ax.annotate(
        text,
        xy=(x, y),
        xytext=(text_x, text_y),
        fontsize=fontsize,
        color=color,
        arrowprops=dict(
            arrowstyle=arrowstyle,
            color=color,
            connectionstyle="arc3,rad=0.2",
        ),
        bbox=dict(
            boxstyle=boxstyle,
            facecolor=facecolor,
            edgecolor=edgecolor,
            alpha=alpha,
        ),
        **kwargs
    )


def add_text_box(
    ax: plt.Axes,
    x: float,
    y: float,
    text: str,
    fontsize: Optional[int] = None,
    color: str = "black",
    facecolor: str = "white",
    edgecolor: str = "black",
    alpha: float = 0.9,
    boxstyle: str = "round,pad=0.3",
    ha: str = "left",
    va: str = "top",
    transform: Optional[str] = "axes",
    **kwargs,
) -> None:
    """
    Add a text box annotation.

    Args:
        ax: Matplotlib Axes to annotate.
        x: X position.
        y: Y position.
        text: Text content.
        fontsize: Font size.
        color: Text color.
        facecolor: Box background color.
        edgecolor: Box edge color.
        alpha: Box transparency.
        boxstyle: Style of box.
        ha: Horizontal alignment.
        va: Vertical alignment.
        transform: Coordinate system ('axes', 'data', 'figure').
        **kwargs: Additional arguments.

    Example:
        >>> add_text_box(ax, 0.05, 0.95, "n = 100", transform="axes")
    """
    fontsize = fontsize or rcParams.get("font.size", 8)

    if transform == "axes":
        trans = ax.transAxes
    elif transform == "figure":
        trans = ax.figure.transFigure
    else:
        trans = ax.transData

    ax.text(
        x, y, text,
        fontsize=fontsize,
        color=color,
        ha=ha, va=va,
        transform=trans,
        bbox=dict(
            boxstyle=boxstyle,
            facecolor=facecolor,
            edgecolor=edgecolor,
            alpha=alpha,
        ),
        **kwargs
    )


def add_region_highlight(
    ax: plt.Axes,
    x_start: float,
    x_end: float,
    y_start: Optional[float] = None,
    y_end: Optional[float] = None,
    color: str = "yellow",
    alpha: float = 0.3,
    label: Optional[str] = None,
    **kwargs,
) -> None:
    """
    Highlight a rectangular region on the plot.

    Args:
        ax: Matplotlib Axes to annotate.
        x_start: Left edge of region.
        x_end: Right edge of region.
        y_start: Bottom edge (default: axes bottom).
        y_end: Top edge (default: axes top).
        color: Highlight color.
        alpha: Highlight transparency.
        label: Optional label for legend.
        **kwargs: Additional arguments.

    Example:
        >>> add_region_highlight(ax, 10, 20, color="yellow", alpha=0.2)
    """
    if y_start is None:
        y_start = ax.get_ylim()[0]
    if y_end is None:
        y_end = ax.get_ylim()[1]

    ax.axvspan(x_start, x_end, y_start, y_end,
               color=color, alpha=alpha, label=label, **kwargs)

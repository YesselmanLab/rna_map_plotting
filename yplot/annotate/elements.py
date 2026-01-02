"""
Visual annotation elements.

This module provides functions for adding arrows, scale bars,
callouts, and text boxes to matplotlib plots.
"""

from typing import Optional, Union

import matplotlib.pyplot as plt
from matplotlib.transforms import ScaledTranslation

from yplot.config import rcParams

# Position definitions: (x, y, x_offset_pts, y_offset_pts, va, ha)
# x, y are anchor points in axes coordinates (0-1)
# x_offset_pts, y_offset_pts are offsets in points (1 point = 1/72 inch)
TEXT_POSITIONS: dict[str, tuple[float, float, float, float, str, str]] = {
    # Corners (inside axes)
    "top left": (0, 1, 4, -4, "top", "left"),
    "top right": (1, 1, -4, -4, "top", "right"),
    "bottom left": (0, 0, 4, 4, "bottom", "left"),
    "bottom right": (1, 0, -4, 4, "bottom", "right"),
    # Edges (centered on edge, inside axes)
    "top": (0.5, 1, 0, -4, "top", "center"),
    "bottom": (0.5, 0, 0, 4, "bottom", "center"),
    "left": (0, 0.5, 4, 0, "center", "left"),
    "right": (1, 0.5, -4, 0, "center", "right"),
    # Center
    "center": (0.5, 0.5, 0, 0, "center", "center"),
    # Outside axes
    "above": (0.5, 1, 0, 4, "bottom", "center"),
    "below": (0.5, 0, 0, -12, "top", "center"),
}

# Short aliases for common positions
TEXT_POSITION_ALIASES: dict[str, str] = {
    "tl": "top left",
    "tr": "top right",
    "bl": "bottom left",
    "br": "bottom right",
}


def text(
    ax: plt.Axes,
    text: str,
    pos: Union[str, tuple[float, float]] = "top left",
    fontsize: Optional[float] = None,
    offset: Optional[float] = None,
    box: bool = False,
    box_facecolor: str = "white",
    box_edgecolor: str = "black",
    box_alpha: float = 0.9,
    box_style: str = "round,pad=0.3",
    **kwargs,
) -> plt.Text:
    """
    Add text at a named position relative to the axes.

    Text is positioned at a fixed point offset from the axes edge,
    independent of axes size.

    Args:
        ax: Matplotlib Axes to add text to.
        text: Text string to display.
        pos: Position name ('top left', 'center', etc.), alias ('tl', 'tr'),
            or tuple of (x, y) in axes coordinates.
        fontsize: Font size (defaults to rcParams).
        offset: Offset from edge in points (1 point = 1/72 inch).
            Overrides default offset. Default is 4 points.
        box: If True, draw a box around the text.
        box_facecolor: Background color for box.
        box_edgecolor: Edge color for box.
        box_alpha: Transparency for box.
        box_style: Style of box ('round,pad=0.3', 'square', etc.).
        **kwargs: Additional arguments passed to ax.text (color, fontweight, etc.).

    Returns:
        The matplotlib Text object.

    Available positions:
        - Corners: 'top left' (tl), 'top right' (tr), 'bottom left' (bl), 'bottom right' (br)
        - Edges: 'top', 'bottom', 'left', 'right'
        - Center: 'center'
        - Outside: 'above', 'below'

    Example:
        >>> text(ax, "n = 100", pos="top left")
        >>> text(ax, "p < 0.05", pos="tr", fontsize=8)
        >>> text(ax, "R² = 0.95", pos="bottom right", fontweight="bold")
        >>> text(ax, "Important", pos="center", box=True)
        >>> text(ax, "Custom", pos=(0.5, 0.8))
        >>> text(ax, "More offset", pos="top left", offset=10)
    """
    fontsize = fontsize or rcParams.get("font.size", 8)
    fontfamily = kwargs.pop("fontfamily", None) or kwargs.pop("fontname", None) or rcParams.get("font.family", "Arial")
    fig = ax.get_figure()

    # Resolve position
    if isinstance(pos, str):
        # Check for alias
        pos_name = TEXT_POSITION_ALIASES.get(pos, pos)
        if pos_name not in TEXT_POSITIONS:
            valid = list(TEXT_POSITIONS.keys()) + list(TEXT_POSITION_ALIASES.keys())
            raise ValueError(
                f"Unknown position '{pos}'. Valid positions: {valid}"
            )
        x, y, x_off, y_off, va, ha = TEXT_POSITIONS[pos_name]

        # Apply custom offset if specified
        if offset is not None:
            x_off, y_off = _calculate_offset(pos_name, offset)

        # Create transform with point-based offset
        # ScaledTranslation takes offset in inches, so convert points to inches
        offset_transform = ScaledTranslation(
            x_off / 72, y_off / 72, fig.dpi_scale_trans
        )
        transform = ax.transAxes + offset_transform
    else:
        # Custom (x, y) tuple - use axes coordinates directly
        x, y = pos
        va = kwargs.pop("va", "center")
        ha = kwargs.pop("ha", "center")
        transform = ax.transAxes

    # Build text kwargs
    text_kwargs = {
        "transform": transform,
        "fontsize": fontsize,
        "fontfamily": fontfamily,
        "verticalalignment": va,
        "horizontalalignment": ha,
    }
    text_kwargs.update(kwargs)

    # Add box if requested
    if box:
        text_kwargs["bbox"] = dict(
            boxstyle=box_style,
            facecolor=box_facecolor,
            edgecolor=box_edgecolor,
            alpha=box_alpha,
        )

    return ax.text(x, y, text, **text_kwargs)


def _calculate_offset(pos_name: str, offset: float) -> tuple[float, float]:
    """Calculate x, y offsets in points for a given position."""
    # Determine direction of offset based on position
    if "left" in pos_name:
        x_off = offset
    elif "right" in pos_name:
        x_off = -offset
    else:
        x_off = 0

    if "top" in pos_name:
        y_off = -offset
    elif "bottom" in pos_name:
        y_off = offset
    elif pos_name == "above":
        y_off = offset
    elif pos_name == "below":
        y_off = -offset
    else:
        y_off = 0

    return x_off, y_off


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

"""
Legend creation utilities.

This module provides functions for creating and positioning legends
on matplotlib axes.
"""

from typing import Optional

import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.legend import Legend

from yplot.config import rcParams


def add_legend(
    ax: plt.Axes,
    labels: list[str],
    loc: str = "upper right",
    fontsize: Optional[int] = None,
    style: str = "line",
    marker: str = "o",
    markersize: float = 5,
    linewidth: float = 0.75,
    handleheight: Optional[float] = None,
    handlelength: Optional[float] = None,
) -> Legend:
    """
    Add a styled legend to an axes.

    Args:
        ax: Matplotlib Axes to add legend to.
        labels: List of legend labels.
        loc: Legend location string.
        fontsize: Font size for legend text.
        style: Legend symbol style:
            - "line": line only (default)
            - "marker": marker only (e.g., circle)
            - "line+marker" or "-o": line with marker
        marker: Marker type when using "marker" or "line+marker" style.
            Common options: "o" (circle), "s" (square), "^" (triangle),
            "D" (diamond), "v" (down triangle), "*" (star)
        markersize: Size of marker.
        linewidth: Width of line.
        handleheight: Height of legend handle (for vertical alignment).
        handlelength: Length of legend handle.

    Returns:
        The created Legend object.

    Example:
        >>> add_legend(ax, ["Series 1", "Series 2"])
        >>> add_legend(ax, ["A", "B"], style="marker", marker="o")
        >>> add_legend(ax, ["A", "B"], style="line+marker", marker="s")
    """
    fontsize = fontsize or rcParams["legend.fontsize"]
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    # Determine line and marker properties based on style
    if style == "line":
        handles = [
            mlines.Line2D([], [], color=color, lw=linewidth, label=label)
            for label, color in zip(labels, colors)
        ]
    elif style == "marker":
        # Use scatter to create handles - better text alignment
        handles = [
            ax.scatter([], [], color=color, s=markersize**2, marker=marker, label=label)
            for label, color in zip(labels, colors)
        ]
    elif style in ("line+marker", "-o"):
        handles = [
            mlines.Line2D([], [], color=color, lw=linewidth, marker=marker,
                         markersize=markersize, label=label)
            for label, color in zip(labels, colors)
        ]
    else:
        raise ValueError(f"Unknown style '{style}'. Use 'line', 'marker', or 'line+marker'")

    font_props = {"family": rcParams["font.family"], "size": fontsize}

    # Set handle dimensions
    _handleheight = handleheight if handleheight is not None else rcParams["legend.handleheight"]
    _handlelength = handlelength if handlelength is not None else rcParams["legend.handlelength"]

    # For marker style, use smaller handlelength
    if style == "marker" and handlelength is None:
        _handlelength = 0.8

    legend = ax.legend(
        handles=handles,
        frameon=rcParams["legend.frameon"],
        loc=loc,
        handlelength=_handlelength,
        handleheight=_handleheight,
        handletextpad=rcParams["legend.handletextpad"],
        borderaxespad=-0.10,
        prop=font_props,
        labelspacing=rcParams["legend.labelspacing"],
        scatterpoints=1,  # Show only 1 point for scatter handles
    )

    return legend


def add_legend_above_subplot(
    ax: plt.Axes,
    labels: list[str],
    x_offset: float = 0.0,
    y_offset: float = 0.03,
    fontsize: Optional[int] = None,
) -> Legend:
    """
    Position a legend above the subplot, anchored to top-right corner.

    Places the legend at a fixed distance above the subplot top edge.
    The legend is anchored to the top-right corner of the axes, with
    text expanding to the left as more labels are added.

    Args:
        ax: Matplotlib Axes to add legend to.
        labels: List of legend labels.
        x_offset: Horizontal offset from right edge (negative moves left).
        y_offset: Vertical offset above top edge.
        fontsize: Font size for legend text. Defaults to rcParams['legend.fontsize'].

    Returns:
        The created Legend object.
    """
    handles, _ = ax.get_legend_handles_labels()
    fontsize = fontsize or rcParams["legend.fontsize"]
    font_props = {"family": rcParams["font.family"], "size": fontsize}
    x_position = 1.0 + x_offset
    y_position = 1.0 + y_offset

    return ax.legend(
        handles,
        labels,
        frameon=False,
        loc="upper right",  # Anchor point is top-right of legend
        bbox_to_anchor=(x_position, y_position),
        bbox_transform=ax.transAxes,
        borderaxespad=0,
        borderpad=0,  # No padding inside legend border
        labelspacing=0,  # No vertical spacing between entries
        handletextpad=0.4,  # Small gap between handle and text
        columnspacing=0.8,  # Gap between columns
        ncol=len(labels),
        prop=font_props,
    )



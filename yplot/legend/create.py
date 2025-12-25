"""
Legend creation utilities.

This module provides functions for creating and positioning legends
on matplotlib axes.
"""

from typing import Optional

import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from matplotlib.legend import Legend

from yplot.config import rcParams


def add_legend(
    ax: plt.Axes,
    labels: list[str],
    loc: str = "upper right",
    fontsize: Optional[int] = None,
) -> Legend:
    """
    Add a styled legend to an axes.

    Args:
        ax: Matplotlib Axes to add legend to.
        labels: List of legend labels.
        loc: Legend location string.
        fontsize: Font size for legend text.

    Returns:
        The created Legend object.

    Example:
        >>> add_legend(ax, ["Series 1", "Series 2"])
    """
    fontsize = fontsize or rcParams["legend.fontsize"]
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    handles = [
        mlines.Line2D([], [], color=color, lw=0.75, label=label)
        for label, color in zip(labels, colors)
    ]

    font_props = {"family": "Arial Unicode MS", "size": fontsize}

    legend = ax.legend(
        handles=handles,
        frameon=rcParams["legend.frameon"],
        loc=loc,
        handlelength=rcParams["legend.handlelength"],
        handleheight=rcParams["legend.handleheight"],
        handletextpad=rcParams["legend.handletextpad"],
        borderaxespad=-0.10,
        prop=font_props,
        labelspacing=rcParams["legend.labelspacing"],
    )

    return legend


def add_legend_above_subplot(
    ax: plt.Axes,
    labels: list[str],
    x_offset_axes: float = 0.63,
    y_offset_axes: float = 0.03,
    use_figure_coords: bool = False,
) -> Legend:
    """
    Position a legend above the subplot.

    Places the legend at a fixed distance above the subplot top edge.
    Uses axes coordinates by default for consistent positioning.

    Args:
        ax: Matplotlib Axes to add legend to.
        labels: List of legend labels.
        x_offset_axes: Horizontal position (0=left, 1=right).
        y_offset_axes: Vertical offset above top edge.
        use_figure_coords: If True, use figure coordinates.

    Returns:
        The created Legend object.
    """
    handles, _ = ax.get_legend_handles_labels()
    font_props = {"family": "Arial Unicode MS", "size": 8}
    y_position = 1.0 + y_offset_axes

    if use_figure_coords:
        return _create_legend_figure_coords(
            ax, handles, labels, x_offset_axes, y_position, font_props
        )
    return _create_legend_axes_coords(
        ax, handles, labels, x_offset_axes, y_position, font_props
    )


def _create_legend_axes_coords(
    ax: plt.Axes,
    handles: list,
    labels: list[str],
    x_offset: float,
    y_position: float,
    font_props: dict,
) -> Legend:
    """Create legend using axes coordinates."""
    return ax.legend(
        handles,
        labels,
        frameon=False,
        loc="upper left",
        bbox_to_anchor=(x_offset, y_position),
        bbox_transform=ax.transAxes,
        borderaxespad=0,
        ncol=len(labels),
        handletextpad=0.6,
        columnspacing=1.0,
        prop=font_props,
    )


def _create_legend_figure_coords(
    ax: plt.Axes,
    handles: list,
    labels: list[str],
    x_offset: float,
    y_position: float,
    font_props: dict,
) -> Legend:
    """Create legend using figure coordinates."""
    pos = ax.get_position()
    fig_x = pos.x0 + x_offset * pos.width
    fig_y = pos.y0 + y_position * pos.height

    return ax.legend(
        handles,
        labels,
        frameon=False,
        loc="upper left",
        bbox_to_anchor=(fig_x, fig_y),
        bbox_transform=ax.figure.transFigure,
        borderaxespad=0,
        ncol=len(labels),
        handletextpad=0.6,
        columnspacing=1.0,
        prop=font_props,
    )

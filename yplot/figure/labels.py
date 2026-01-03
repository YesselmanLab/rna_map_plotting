"""
Figure and axes labeling utilities.

This module provides functions for adding labels and text annotations
to figures and axes.
"""

from typing import Optional

import matplotlib.pyplot as plt

from yplot.config import rcParams

Coordinate = tuple[float, float, float, float]


def add_subplot_labels(
    fig: plt.Figure,
    coords_list: list[Coordinate],
    start: str = "A",
    left_offset: Optional[float] = None,
    top_offset: Optional[float] = None,
    fontsize: Optional[int] = None,
) -> None:
    """
    Add labels (A, B, C, ...) to subplot corners.

    Args:
        fig: Matplotlib Figure object.
        coords_list: List of (left, bottom, width, height) coordinates.
        start: Starting letter (default: "A").
        left_offset: Horizontal offset from subplot left edge.
        top_offset: Vertical offset above subplot top edge.
        fontsize: Font size for labels.

    Example:
        >>> fig, axes = create_figure_with_layout(layout)
        >>> add_subplot_labels(fig, layout.get_final_coordinates())
    """
    left_offset = left_offset or rcParams["subplot.label_left_offset"]
    top_offset = top_offset or rcParams["subplot.label_top_offset"]
    fontsize = fontsize or rcParams["subplot.label_fontsize"]
 
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    start_idx = letters.index(start)

    for i, coords in enumerate(coords_list):
        left, bottom, width, height = coords
        x = left - left_offset
        y = bottom + height + top_offset

        fig.text(
            x, y, letters[start_idx + i],
            fontsize=fontsize,
            weight="bold",
            fontname=rcParams["font.family"],
            va="top",
            ha="left",
        )


def add_ax_corner_text(
    ax: plt.Axes,
    text: str,
    pos: str = "upper left",
    fontsize: Optional[int] = None,
) -> None:
    """
    Add text to a corner of an axes.

    Args:
        ax: Matplotlib Axes object.
        text: Text to display.
        pos: Corner position ("upper left", "upper right",
             "lower left", "lower right").
        fontsize: Font size for text.
    """
    fontsize = fontsize or rcParams["corner_text.fontsize"]
    font_family = rcParams["font.family"]

    positions = {
        "upper left": (0.03, 0.97, "top", "left"),
        "upper right": (0.97, 0.97, "top", "right"),
        "lower left": (0.03, 0.03, "bottom", "left"),
        "lower right": (0.97, 0.03, "bottom", "right"),
        # Aliases
        "bottom left": (0.03, 0.03, "bottom", "left"),
        "bottom right": (0.97, 0.03, "bottom", "right"),
    }

    if pos not in positions:
        raise ValueError(f"Unknown position: {pos}")

    x, y, va, ha = positions[pos]
    ax.text(
        x, y, text,
        transform=ax.transAxes,
        fontsize=fontsize,
        fontname=font_family,
        verticalalignment=va,
        horizontalalignment=ha,
    )

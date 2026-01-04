"""
Figure creation utilities.

This module provides functions for creating matplotlib figures
using yplot's layout system.
"""

from typing import Union

import matplotlib.pyplot as plt

from yplot.layout import SubplotLayout
from yplot.layout.grid_layout import AxisType, GridLayout


def create_figure_with_layout(
    layout: SubplotLayout,
    **kwargs,
) -> tuple[plt.Figure, list[plt.Axes]]:
    """
    Create a matplotlib figure using a SubplotLayout configuration.

    Args:
        layout: SubplotLayout object defining the figure layout.
        **kwargs: Additional keyword arguments passed to plt.figure().

    Returns:
        Tuple of (figure, list of axes).

    Example:
        >>> layout = SubplotLayout(config={'fig_size': [10, 8], ...})
        >>> fig, axes = create_figure_with_layout(layout)
    """
    coords = layout.get_final_coordinates()
    fig = plt.figure(figsize=layout.fig_size_inches, **kwargs)

    axes = []
    for coord in coords:
        ax = fig.add_axes(coord)
        axes.append(ax)

    return fig, axes


def create_figure_with_true_size(
    width: float,
    height: float,
    verify: bool = False,
    dpi: int = 100,
) -> tuple[plt.Figure, plt.Axes]:
    """
    Create a figure where axes exactly match specified dimensions.

    Removes all margins and padding so the axes panel size equals
    the specified width and height in inches.

    Args:
        width: Desired axes width in inches.
        height: Desired axes height in inches.
        verify: If True, print actual axes size for verification.
        dpi: Figure DPI (default: 100).

    Returns:
        Tuple of (figure, axes).

    Example:
        >>> fig, ax = create_figure_with_true_size(4, 3)
        # Creates axes exactly 4x3 inches
    """
    fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    if verify:
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        print(f"Axes panel size: {bbox.width:.2f} x {bbox.height:.2f} inches")

    return fig, ax


def create_figure_with_grid(
    layout: GridLayout,
    apply_axis_types: bool = True,
    **kwargs,
) -> tuple[plt.Figure, list[plt.Axes]]:
    """
    Create a matplotlib figure using a GridLayout configuration.

    Args:
        layout: GridLayout object defining the figure layout.
        apply_axis_types: If True, configure axes based on axis_type
                         (hide ticks/spines for IMAGE type).
        **kwargs: Additional keyword arguments passed to plt.figure().

    Returns:
        Tuple of (figure, list of axes).

    Example:
        >>> spec = GridSpec.uniform(3, 3, 2.5, 2.0)
        >>> layout = GridLayout(spec)
        >>> layout.add_cell(0, 0, colspan=3)
        >>> fig, axes = create_figure_with_grid(layout)

        # With shared axes:
        >>> layout.add_cell(0, 0, name="top")
        >>> layout.add_cell(1, 0, sharex="top")  # Share x-axis with "top"
    """
    coords = layout.get_final_coordinates()
    axis_types = layout.get_axis_types()
    share_info = layout.get_share_info()
    fig = plt.figure(figsize=layout.fig_size_inches, **kwargs)

    axes = []
    for i, (coord, axis_type) in enumerate(zip(coords, axis_types)):
        sharex_idx, sharey_idx = share_info[i]

        # Get axes to share with (if specified and already created)
        sharex_ax = axes[sharex_idx] if sharex_idx is not None else None
        sharey_ax = axes[sharey_idx] if sharey_idx is not None else None

        ax = fig.add_axes(coord, sharex=sharex_ax, sharey=sharey_ax)
        if apply_axis_types and axis_type == AxisType.IMAGE:
            _configure_axis_for_image(ax)
        axes.append(ax)

    return fig, axes


def _configure_axis_for_image(ax: plt.Axes) -> None:
    """Configure axis for image display (no ticks/spines)."""
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

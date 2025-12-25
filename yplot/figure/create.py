"""
Figure creation utilities.

This module provides functions for creating matplotlib figures
using yplot's layout system.
"""


import matplotlib.pyplot as plt

from yplot.layout import SubplotLayout


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

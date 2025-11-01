import matplotlib.lines as mlines
import matplotlib.pyplot as plt


def add_legend(ax, labels, loc="upper right", fontsize=8):
    handles = []
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    for label, color in zip(labels, colors):
        patch = mlines.Line2D([], [], color=color, lw=0.75, label=label)
        handles.append(patch)
    arial_font = {"family": "Arial Unicode MS", "size": fontsize}

    legend = ax.legend(
        handles=handles,
        frameon=False,
        loc=loc,
        handlelength=1.0,
        handleheight=0.5,
        handletextpad=0.30,
        borderaxespad=-0.10,  # as close as possible to axes
        prop=arial_font,
        labelspacing=0.15,  # reduce space between lines in legend
    )

    return legend


def add_legend_above_subplot(
    ax, labels, x_offset_axes=0.63, y_offset_axes=0.03, use_figure_coords=False
):
    """
    Position a legend above the subplot box at a fixed distance, independent of figure size.

    Uses axes coordinates to position the legend at a fixed offset above the subplot.
    The offset is in axes fraction, meaning it scales with the subplot size but is
    consistent across different figure sizes. This is similar to how ax.text() with
    transform=ax.transAxes works for positioning text labels.

    When use_figure_coords=False (default), uses axes coordinates (bbox_transform=ax.transAxes).
    This ensures the legend is always a fixed distance above the subplot, independent
    of the overall figure size.

    When use_figure_coords=True, converts the position to figure coordinates for
    multi-subplot layouts where you want consistent positioning across different subplot sizes.

    Args:
        ax (matplotlib.axes.Axes): The matplotlib Axes object to add the legend to.
        labels (list of str): List of labels to use for the legend items.
        x_offset_axes (float): Horizontal position in axes fraction (0=left, 1=right).
            Default is 0.63 (63% across the axes).
        y_offset_axes (float): Vertical offset above the top of the axes in axes fraction.
            Default is 0.03 (3% of axes height above the top). This is a fixed amount
            independent of figure size.
        use_figure_coords (bool): If True, convert axes-relative position to figure
            coordinates for consistent positioning in multi-subplot layouts.
            Default is False for backward compatibility.

    Returns:
        matplotlib.legend.Legend: The created legend object.

    Example:
        >>> fig, ax = plt.subplots()
        >>> ax.plot([1, 2, 3], [1, 2, 3], label='Line 1')
        >>> ax.plot([1, 2, 3], [2, 3, 4], label='Line 2')
        >>> # Place legend 3% of axes height above the subplot
        >>> add_legend_above_subplot(ax, ["0 mM Mg²⁺", "40 mM Mg²⁺"], y_offset_axes=0.03)
    """
    handles, _ = ax.get_legend_handles_labels()
    arial8 = {"family": "Arial Unicode MS", "size": 8}

    # Position is at (x_offset_axes, 1 + y_offset_axes) in axes coordinates
    # where 1.0 is the top of the axes, so 1 + y_offset_axes places it above
    y_position_axes = 1.0 + y_offset_axes

    if use_figure_coords:
        # Get axes position in figure coordinates
        pos = ax.get_position()
        ax_left = pos.x0
        ax_bottom = pos.y0
        ax_width = pos.width
        ax_height = pos.height

        # Convert axes-relative position to figure coordinates
        fig_x = ax_left + x_offset_axes * ax_width
        fig_y = ax_bottom + y_position_axes * ax_height

        legend = ax.legend(
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
            prop=arial8,
        )
    else:
        # Use axes coordinates - legend is always a fixed distance above the subplot
        # independent of figure size
        legend = ax.legend(
            handles,
            labels,
            frameon=False,
            loc="upper left",
            bbox_to_anchor=(x_offset_axes, y_position_axes),
            bbox_transform=ax.transAxes,
            borderaxespad=0,
            ncol=len(labels),
            handletextpad=0.6,
            columnspacing=1.0,
            prop=arial8,
        )

    return legend

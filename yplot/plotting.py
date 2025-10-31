import matplotlib.pyplot as plt
import matplotlib.axes as axes
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Union, Optional, Sequence
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from yplot.logger import get_logger
from yplot.figure import SubplotLayout, calculate_subplot_coordinates

log = get_logger("plotting")


def extract_xy(data, x, y):
    """
    Extract x and y array-like objects from different input combinations.

    If `data` is a DataFrame and `x` and `y` are strings, fetch the columns from `data`.
    Otherwise, if `x` and `y` are array-like, return them directly.

    Parameters
    ----------
    data : pd.DataFrame or None
        Source dataframe from which to extract columns.
    x : str or array-like
        Column name or array-like representing x values.
    y : str or array-like
        Column name or array-like representing y values.

    Returns
    -------
    x_values, y_values : array-like
        Arrays for x and y variables.
    """
    if data is not None:
        if isinstance(x, str) and isinstance(y, str):
            return data[x], data[y]
    # if data is None or x/y are not str, assume arraylike
    return x, y


def add_subplot_labels(
    fig, coords_list, start="A", left_offset=0.0572, top_offset=0.02, fontsize=12
):
    """
    Add subplot labels (A, B, C, ...) to the top-left corner of each subplot.

    Args:
        fig: matplotlib Figure object.
        coords_list: list of (left, bottom, width, height) in figure fraction coordinates.
        fig_size: (width, height) in inches.
        start: starting letter.
    """
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    pos = letters.index(start)
    for i, coords in enumerate(coords_list):
        left, bottom, width, height = coords
        # Place label at a fixed offset from the top-left corner of the subplot
        # Use figure fraction coordinates for robust placement
        x = left - left_offset
        y = bottom + height + top_offset
        fig.text(
            x,
            y,
            letters[pos],
            fontsize=fontsize,
            weight="bold",
            fontname="Arial",
            va="top",
            ha="left",
        )
        pos += 1


def add_ax_corner_text(ax, text, pos="top left", fontsize=6):
    if pos == "upper left":
        ax.text(
            0.03,
            0.97,
            text,
            transform=ax.transAxes,
            fontsize=fontsize,
            fontname="Arial",
            verticalalignment="top",
            horizontalalignment="left",
        )
    elif pos == "upper right":
        ax.text(
            0.97,
            0.97,
            text,
            transform=ax.transAxes,
            fontsize=fontsize,
            fontname="Arial",
            verticalalignment="top",
            horizontalalignment="right",
        )
    elif pos == "bottom left":
        ax.text(
            0.03,
            0.03,
            text,
            transform=ax.transAxes,
            fontsize=fontsize,
            fontname="Arial",
            verticalalignment="bottom",
            horizontalalignment="left",
        )
    elif pos == "bottom right":
        ax.text(
            0.97,
            0.03,
            text,
            transform=ax.transAxes,
            fontsize=fontsize,
            fontname="Arial",
            verticalalignment="bottom",
            horizontalalignment="right",
        )


def plot_regression_line(x, y, ax, pos="upper left", fontsize=6):
    model = LinearRegression()
    model.fit(x, y)
    r2 = r2_score(y, model.predict(x))
    x_pred = np.linspace(x.min(), x.max(), 1000).reshape(-1, 1)
    ax.plot(x_pred, model.predict(x_pred), color="black", linewidth=1, linestyle="--")
    add_ax_corner_text(ax, f"R² = {r2:.2f}", pos=pos, fontsize=fontsize)
    return r2


def scatter_plot_w_regression(
    data=None, ax=None, x=None, y=None, pos="upper left", size=6, fontsize=6
):
    # Prepare the data
    x, y = extract_xy(data, x, y)
    x = x.reshape(-1, 1)
    if ax is None:
        _, ax = plt.subplots()
    ax.scatter(x, y, s=size)
    plot_regression_line(x, y, ax, pos=pos, fontsize=fontsize)


def lollipop_plot(
    x: Sequence,
    y1: Sequence,
    y2: Optional[Sequence] = None,
    *,
    ax: Optional[plt.Axes] = None,
    line_color: str = "black",
    marker_size: float = 40,
    line_width: float = 1.0,
) -> plt.Axes:
    """
    Create a single or paired lollipop plot.

    Parameters
    ----------
    x : sequence
        Categories or numeric positions for the lollipops.
    y1 : sequence
        First set of values to plot.
    y2 : sequence, optional
        Second set of values for paired lollipop plot.
    ax : matplotlib.axes.Axes, optional
        Axis to draw the plot on. Creates one if None.
    color1, color2 : str, default matplotlib defaults
        Colors for the data points.
    line_color : str, default "black"
        Color of the connecting lines.
    marker_size : float, default 40
        Size of scatter markers.
    line_width : float, default 1.0
        Width of the connecting lines.

    Returns
    -------
    matplotlib.axes.Axes
        The axis containing the plot.
    """
    if ax is None:
        _, ax = plt.subplots()

    for xi, yi1, yi2 in zip(x, y1, y2):
        ax.vlines(xi, min(yi1, yi2), max(yi1, yi2), color=line_color, lw=line_width)
    ax.scatter(x, y1, s=marker_size, zorder=3)
    ax.scatter(x, y2, s=marker_size, zorder=3)
    ax.set_xticks(x)
    return ax


def create_figure_with_layout(layout, **kwargs):
    """
    Create a matplotlib figure using a SubplotLayout configuration.

    This is the main function for creating figures with the new layout system.

    Parameters:
    -----------
    layout : SubplotLayout, dict, str, or Path
        Layout configuration. Can be:
        - SubplotLayout object
        - Dictionary with layout configuration
        - String path to YAML file
        - Path object to YAML file
    **kwargs
        Additional keyword arguments passed to plt.figure()

    Returns:
    --------
    tuple
        (fig, axes) where fig is matplotlib.figure.Figure and axes is list of matplotlib.axes.Axes

    Examples:
    ---------
    # Using SubplotLayout object
    layout = SubplotLayout(fig_size_inches=(10, 8), rows=2, cols=3)
    fig, axes = create_figure_with_layout(layout)

    # From dictionary
    config = {'fig_size': [10, 8], 'rows': 2, 'cols': 3, 'row_heights': [3.0, 2.0]}
    fig, axes = create_figure_with_layout(config)

    # From YAML file
    fig, axes = create_figure_with_layout('my_layout.yaml')
    """
    # Convert to SubplotLayout object if needed
    if not isinstance(layout, SubplotLayout):
        if isinstance(layout, (str, Path)):
            layout = SubplotLayout(yaml_file=layout)
        elif isinstance(layout, dict):
            layout = SubplotLayout(config=layout)
        else:
            raise TypeError(
                "layout must be a SubplotLayout object, dictionary, or YAML file path"
            )

    # Get coordinates from layout
    coords = calculate_subplot_coordinates(layout)

    # Create figure
    fig = plt.figure(figsize=layout.fig_size_inches, **kwargs)

    # Create axes for each subplot
    axes = []
    for i, (left, bottom, width, height) in enumerate(coords):
        ax = fig.add_axes([left, bottom, width, height])
        axes.append(ax)

    return fig, axes


def load_and_fit_image_to_subplot(image_path, ax):
    """
    Load an image from file and stretch it to fit in a subplot.

    Parameters:
    -----------
    image_path : str
        Path to the image file
    subplot_coords : tuple
        Subplot coordinates as (left, bottom, width, height) in figure-relative units
    fig : matplotlib.figure.Figure
        The figure object
    ax : matplotlib.axes.Axes
        The axes object where the image will be placed

    Returns:
    --------
    matplotlib.image.AxesImage
        The image object that was added to the subplot
    """

    # Load the image
    try:
        img = mpimg.imread(image_path)
    except Exception as e:
        raise ValueError(f"Could not load image from {image_path}: {e}")

    # Clear the axes
    ax.clear()

    # Display the image stretched to fit the subplot
    img_plot = ax.imshow(img)

    # Remove axes ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    return img_plot

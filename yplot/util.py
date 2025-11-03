"""Utility functions for yplot"""

import os
import yaml
from pathlib import Path
from typing import List, Union, Optional
from matplotlib import pyplot as plt
import matplotlib.patches as patches

from yplot.logger import get_logger
from yplot.style import publication_style_ax

log = get_logger("util")


def colors_for_sequence(seq: str) -> List[str]:
    """
    Returns a list of colors corresponding to the input DNA/RNA sequence.

    This function maps each character in the input DNA/RNA sequence to a specific color:
    - 'A' -> 'red'
    - 'C' -> 'blue'
    - 'G' -> 'orange'
    - 'T' or 'U' -> 'green'
    - '&' -> 'gray'

    Args:
        seq (str): A string representing a RNA/DNA sequence.

    Returns:
        List[str]: A list of color strings corresponding to each character in the
        sequence.

    Raises:
        TypeError: If the input is not a string.
        ValueError: If the sequence contains invalid characters.
    """
    color_mapping = {
        "A": "red",
        "C": "blue",
        "G": "orange",
        "T": "green",
        "U": "green",
        "&": "gray",
    }

    colors = []
    for e in seq.upper():  # Convert to uppercase
        try:
            color = color_mapping[e]
            colors.append(color)
        except KeyError as exc:
            log.error(
                "Invalid character '{}' in sequence. Sequence must contain only "
                "'A', 'C', 'G', 'U', 'T', and '&'.".format(e)
            )
            raise ValueError("Invalid character '{}' in sequence.".format(e)) from exc

    log.debug("Input Sequence: {}".format(seq))
    log.debug("Output Colors: {}".format(colors))
    return colors


def draw_box_around_subplot(
    fig, coords, linewidth=2, edgecolor="red", facecolor="none"
):
    """
    Draw a box around a subplot in a figure.

    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The figure to draw the box on
    coords : tuple
        Subplot coordinates (left, bottom, width, height)
    linewidth : float, optional
        Width of the box line (default: 2)
    edgecolor : str, optional
        Color of the box edge (default: "red")
    facecolor : str, optional
        Color of the box face (default: "none")
    """
    bbox = patches.Rectangle(
        (
            coords[0],
            coords[1],
        ),  # (left, bottom) in figure coordinates
        coords[2],  # width in figure coordinates
        coords[3],  # height in figure coordinates
        linewidth=linewidth,
        edgecolor=edgecolor,
        facecolor=facecolor,
        transform=fig.transFigure,
    )
    fig.patches.append(bbox)


def draw_box_around_figure(fig, linewidth=2, edgecolor="black", facecolor="none"):
    """
    Draw a box around the bounds of the entire figure.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to draw the bounding box on.
    linewidth : float, optional
        Line width of the bounding box (default: 2)
    edgecolor : str, optional
        Color of the bounding box edge (default: "black")
    facecolor : str, optional
        Color to fill the box with (default: "none", i.e., transparent)
    """
    # The full figure in figure coordinates is (0, 0, 1, 1)
    bbox = patches.Rectangle(
        (0, 0),
        1,
        1,
        linewidth=linewidth,
        edgecolor=edgecolor,
        facecolor=facecolor,
        transform=fig.transFigure,
        zorder=100,
    )
    fig.patches.append(bbox)


def draw_boxes_around_subplots(fig, coords_list):
    """
    Draw a box around each set of subplot coordinates in coords_list,
    using a different color for each box.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to draw the boxes on.
    coords_list : list of tuple
        List of (left, bottom, width, height) tuples in figure coordinates.
    """
    color_cycle = (
        plt.rcParams["axes.prop_cycle"]
        .by_key()
        .get(
            "color",
            [
                "red",
                "blue",
                "green",
                "orange",
                "purple",
                "brown",
                "pink",
                "gray",
                "olive",
                "cyan",
            ],
        )
    )

    for i, coords in enumerate(coords_list):
        color = color_cycle[i % len(color_cycle)]
        draw_box_around_subplot(
            fig, coords, linewidth=2, edgecolor=color, facecolor="none"
        )
    return fig


def get_data_path():
    """Get the path to the data directory"""
    return Path(__file__).parent / "data"


def load_figure_layout(preset_name=None):
    """
    Load a figure layout configuration from YAML file.

    Parameters
    ----------
    preset_name : str, optional
        Name of the preset layout to load (e.g., '1x4_portrait', '2x2_square').
        If None, returns all available presets.

    Returns
    -------
    dict
        Configuration dictionary with keys: fig_size, layout, subplot_size, spacing
        If preset_name is None, returns dict of all presets.

    Examples
    --------
    >>> config = load_figure_layout('1x4_portrait')
    >>> fig_size = tuple(config['fig_size'])
    >>> layout = tuple(config['layout'])
    >>> subplot_size = tuple(config['subplot_size'])
    >>> spacing = config['spacing']

    >>> # Get all available presets
    >>> all_presets = load_figure_layout()
    >>> print(all_presets.keys())
    """
    layouts_file = get_data_path() / "figure_layouts.yaml"

    if not layouts_file.exists():
        raise FileNotFoundError(f"Figure layouts file not found: {layouts_file}")

    with open(layouts_file, "r") as f:
        all_layouts = yaml.safe_load(f)

    if preset_name is None:
        return all_layouts

    if preset_name not in all_layouts:
        available = ", ".join(all_layouts.keys())
        raise ValueError(
            f"Layout preset '{preset_name}' not found. "
            f"Available presets: {available}"
        )

    return all_layouts[preset_name]


def list_figure_layouts():
    """
    List all available figure layout presets.

    Returns
    -------
    list
        List of available preset names
    """
    all_layouts = load_figure_layout()
    return list(all_layouts.keys())


def create_figure_with_true_size(width, height, verify=False):
    """
    Create a figure and axes with the specified true (panel-only) size in inches.

    To ensure the "true" (interior, panel-only) axes size is exactly the specified
    width x height inches, the figure size is set to match and all margins/paddings
    are removed.

    Args:
        width (float): Desired axes panel width in inches.
        height (float): Desired axes panel height in inches.
        verify (bool): If True, print the actual axes panel size for verification.
                      Default is True.

    Returns:
        tuple: (fig, ax) matplotlib figure and axes objects.
    """
    fig, ax = plt.subplots(figsize=(width, height))
    # Remove any space/margins to ensure axes size matches figure size
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    if verify:
        # Check the resulting axes size to verify
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        ax_width_in, ax_height_in = bbox.width, bbox.height
        print(f"Ax panel size: {ax_width_in:.2f} x {ax_height_in:.2f} inches")

    return fig, ax

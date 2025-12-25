"""
Debug and visualization utilities for figure layouts.

This module provides functions for visualizing subplot layouts
and debugging figure configurations.
"""

import os
from pathlib import Path
from typing import Union

import matplotlib.patches as patches
import matplotlib.pyplot as plt

from yplot.layout import SubplotLayout
from yplot.style import publication_style_ax

Coordinate = tuple[float, float, float, float]

SUBPLOT_COLORS = [
    "#ffcccc", "#ccffcc", "#ccccff", "#ffffcc",
    "#ffccff", "#ccffff", "#ffdddd", "#ddffdd",
]


def render_example_figure(layout: SubplotLayout) -> plt.Figure:
    """
    Render a preview figure showing subplot layout.

    Creates a figure with colored subplots to visualize the layout
    configuration without actual data.

    Args:
        layout: SubplotLayout object to visualize.

    Returns:
        Matplotlib Figure showing the layout.

    Raises:
        ValueError: If layout is not a SubplotLayout instance.
    """
    if not isinstance(layout, SubplotLayout):
        raise ValueError("layout must be a SubplotLayout object")

    coords = layout.get_final_coordinates()
    is_image_list = _build_image_list(layout)

    fig = plt.figure(figsize=layout.fig_size_inches, dpi=100)

    for idx, coord in enumerate(coords):
        ax = fig.add_axes(coord)
        is_image = is_image_list[idx] if idx < len(is_image_list) else False
        _render_subplot(ax, idx, is_image)

    return fig


def _build_image_list(layout: SubplotLayout) -> list[bool]:
    """Build list indicating which subplots are image placeholders."""
    is_image_list = []
    row_keys = sorted(k for k in layout.subplot_info.keys() if k.startswith("row_"))

    for row_key in row_keys:
        row_data = layout.subplot_info[row_key]
        num_cols = row_data.get("cols", 1)
        image_spec = row_data.get("image", False)

        if image_spec:
            row_images = [i in image_spec for i in range(num_cols)]
        else:
            row_images = [False] * num_cols

        is_image_list.extend(row_images)

    return is_image_list


def _render_subplot(ax: plt.Axes, idx: int, is_image: bool) -> None:
    """Render a single subplot in preview mode."""
    color = SUBPLOT_COLORS[idx % len(SUBPLOT_COLORS)]
    ax.set_facecolor(color)

    if is_image:
        _render_image_placeholder(ax, idx)
    else:
        _render_axes_placeholder(ax, idx)


def _render_image_placeholder(ax: plt.Axes, idx: int) -> None:
    """Render placeholder for image subplot."""
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.text(0.5, 0.5, f"Image {idx}", ha="center", va="center",
            fontsize=10, fontweight="bold")


def _render_axes_placeholder(ax: plt.Axes, idx: int) -> None:
    """Render placeholder for regular subplot."""
    ax.text(0.5, 0.5, f"Subplot {idx}", ha="center", va="center",
            fontsize=10, fontweight="bold")
    for spine in ax.spines.values():
        spine.set_edgecolor("black")
        spine.set_linewidth(0.5)
    ax.set_xlabel("X Label", labelpad=2)
    ax.set_ylabel("Y Label", labelpad=2)
    publication_style_ax(ax)


def save_example_figure(
    fig: plt.Figure,
    title: str,
    filename: str,
    output_dir: Union[str, Path] = "docs/figures",
    dpi: int = 150,
    bbox_inches: str = "tight",
) -> str:
    """
    Save a figure with title and formatting.

    Args:
        fig: Figure to save.
        title: Title to add to figure.
        filename: Output filename.
        output_dir: Output directory path.
        dpi: Output DPI.
        bbox_inches: Bounding box setting.

    Returns:
        Path to saved file.
    """
    fig.suptitle(title, fontsize=14, fontweight="bold", y=0.95)
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
    print(f"Saved: {filepath}")
    return filepath


def create_example_figure(
    layout: SubplotLayout,
    title: str,
    filename: str,
    output_dir: Union[str, Path] = "docs/figures",
) -> str:
    """
    Create and save an example figure showing layout.

    Args:
        layout: SubplotLayout to visualize.
        title: Figure title.
        filename: Output filename.
        output_dir: Output directory.

    Returns:
        Path to saved file.
    """
    fig = render_example_figure(layout)
    filepath = save_example_figure(fig, title, filename, output_dir)
    plt.close(fig)
    return filepath


def draw_box_around_figure(
    fig: plt.Figure,
    linewidth: float = 2,
    edgecolor: str = "black",
    facecolor: str = "none",
) -> None:
    """
    Draw a bounding box around the entire figure.

    Args:
        fig: Figure to draw box on.
        linewidth: Line width of box.
        edgecolor: Edge color of box.
        facecolor: Fill color of box.
    """
    bbox = patches.Rectangle(
        (0, 0), 1, 1,
        linewidth=linewidth,
        edgecolor=edgecolor,
        facecolor=facecolor,
        transform=fig.transFigure,
        zorder=100,
    )
    fig.patches.append(bbox)


def draw_box_around_subplot(
    fig: plt.Figure,
    coords: Coordinate,
    linewidth: float = 2,
    edgecolor: str = "red",
    facecolor: str = "none",
) -> None:
    """
    Draw a box around a subplot.

    Args:
        fig: Figure containing the subplot.
        coords: Subplot coordinates (left, bottom, width, height).
        linewidth: Line width of box.
        edgecolor: Edge color of box.
        facecolor: Fill color of box.
    """
    bbox = patches.Rectangle(
        (coords[0], coords[1]),
        coords[2], coords[3],
        linewidth=linewidth,
        edgecolor=edgecolor,
        facecolor=facecolor,
        transform=fig.transFigure,
    )
    fig.patches.append(bbox)


def draw_boxes_around_subplots(
    fig: plt.Figure,
    coords_list: list[Coordinate],
) -> plt.Figure:
    """
    Draw boxes around multiple subplots with different colors.

    Args:
        fig: Figure containing the subplots.
        coords_list: List of subplot coordinates.

    Returns:
        The figure with boxes added.
    """
    color_cycle = plt.rcParams["axes.prop_cycle"].by_key().get(
        "color",
        ["red", "blue", "green", "orange", "purple", "brown", "pink"],
    )

    for i, coords in enumerate(coords_list):
        color = color_cycle[i % len(color_cycle)]
        draw_box_around_subplot(fig, coords, edgecolor=color)

    return fig

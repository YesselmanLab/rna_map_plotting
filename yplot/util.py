"""Utility functions for yplot"""

import os
import yaml
from pathlib import Path
from typing import List, Union, Optional
from matplotlib import pyplot as plt
import matplotlib.patches as patches

from yplot.logger import get_logger

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
        zorder=100
    )
    fig.patches.append(bbox)


def draw_boxes_around_coords_list(fig, coords_list):
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


def create_custom_layout(fig_size, layout, subplot_size, spacing):
    """
    Create a custom layout configuration dictionary.

    Parameters
    ----------
    fig_size : tuple
        Figure size as (width, height) in inches
    layout : tuple
        Layout grid as (rows, cols)
    subplot_size : tuple
        Size of each subplot as (width, height) in inches
    spacing : dict
        Spacing configuration with keys:
        - hspace: horizontal spacing in inches
        - wspace: vertical spacing in inches
        - margins: dict with keys left, right, top, bottom

    Returns
    -------
    dict
        Configuration dictionary compatible with figure layout format
    """
    return {
        "fig_size": list(fig_size),
        "layout": list(layout),
        "subplot_size": list(subplot_size),
        "spacing": spacing,
    }


def render_example_figure(coords, fig_size_inches, grid_layout=None, section_info=None):
    """
    Render an example figure with subplot coordinates.
    
    This function creates a matplotlib figure with the given coordinates but does not save it.
    Use this when you want to display the figure or save it manually.
    
    Parameters:
    -----------
    coords : list
        List of (left, bottom, width, height) coordinate tuples
    fig_size_inches : tuple
        Figure size as (width, height) in inches
    grid_layout : tuple, optional
        Grid layout as (rows, cols) for display purposes
    section_info : dict, optional
        Additional information about sections or subplot groupings
    
    Returns:
    --------
    matplotlib.figure.Figure
        The rendered figure object
    
    Examples:
    ---------
    # Render a figure
    coords = calculate_subplot_coordinates(...)
    fig = render_example_figure(coords, (7, 5))
    
    # Display the figure
    plt.show()
    
    # Or save it manually
    fig.savefig('my_figure.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    """
    fig = plt.figure(figsize=fig_size_inches, dpi=100)
    
    # Color palette for different subplot sizes or sections
    colors = ['#ffcccc', '#ccffcc', '#ccccff', '#ffffcc', '#ffccff', '#ccffff', '#ffdddd', '#ddffdd']
    
    for idx, (left, bottom, width, height) in enumerate(coords):
        ax = fig.add_axes([left, bottom, width, height])
        
        # Set background color based on section or index
        if section_info and 'section' in section_info:
            color_idx = section_info['section'] % len(colors)
        else:
            color_idx = idx % len(colors)
        
        ax.set_facecolor(colors[color_idx])
        
        # Add text showing subplot info
        if grid_layout:
            rows, cols = grid_layout
            row = idx // cols
            col = idx % cols
            ax.text(0.5, 0.5, f'R{row}C{col}\n{idx}', 
                    ha='center', va='center', fontsize=10, fontweight='bold')
        else:
            ax.text(0.5, 0.5, f'Subplot {idx}', 
                    ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Add a subtle border
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(0.5)
        
        # Remove ticks for cleaner look
        ax.set_xticks([])
        ax.set_yticks([])
    
    return fig


def save_example_figure(fig, title, filename, output_dir='test_figures', dpi=150, bbox_inches='tight'):
    """
    Save an example figure to a file.
    
    This function saves a matplotlib figure to a file with optional title and formatting.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The figure object to save
    title : str
        Title for the figure (will be added as suptitle)
    filename : str
        Filename to save the figure
    output_dir : str, optional
        Directory to save the figure in (default: 'test_figures')
    dpi : int, optional
        DPI for the saved figure (default: 150)
    bbox_inches : str, optional
        Bbox_inches parameter for saving (default: 'tight')
    
    Returns:
    --------
    str
        Path to the saved figure file
    
    Examples:
    ---------
    # Save a figure
    fig = render_example_figure(coords, (7, 5))
    filepath = save_example_figure(fig, "My Layout", "example.png")
    plt.close(fig)
    
    # Save with custom directory and DPI
    filepath = save_example_figure(
        fig, 
        "My Layout", 
        "example.png", 
        output_dir='my_figures',
        dpi=300
    )
    """
    # Add title to figure
    fig.suptitle(title, fontsize=14, fontweight='bold', y=0.95)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    # Save the figure
    fig.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)
    
    print(f"✓ Saved: {filepath}")
    return filepath


def create_example_figure(coords, title, filename, fig_size_inches, grid_layout=None, section_info=None, output_dir='test_figures'):
    """
    Create and save an example figure with subplot coordinates.
    
    This is a convenience function that combines render_example_figure and save_example_figure.
    Use this for quick figure creation and saving.
    
    Parameters:
    -----------
    coords : list
        List of (left, bottom, width, height) coordinate tuples
    title : str
        Title for the figure
    filename : str
        Filename to save the figure
    fig_size_inches : tuple
        Figure size as (width, height) in inches
    grid_layout : tuple, optional
        Grid layout as (rows, cols) for display purposes
    section_info : dict, optional
        Additional information about sections or subplot groupings
    output_dir : str, optional
        Directory to save the figure in (default: 'test_figures')
    
    Returns:
    --------
    str
        Path to the saved figure file
    
    Examples:
    ---------
    # Create and save a simple example figure
    coords = calculate_subplot_coordinates(...)
    filepath = create_example_figure(
        coords, 
        "My Layout", 
        "example.png", 
        (7, 5)
    )
    
    # Create figure with section information
    filepath = create_example_figure(
        coords,
        "Merged Layout",
        "merged.png", 
        (7, 6),
        section_info={'section': 0, 'merged_pairs': [(0, 1)]}
    )
    """
    # Render the figure
    fig = render_example_figure(coords, fig_size_inches, grid_layout, section_info)
    
    # Save the figure
    filepath = save_example_figure(fig, title, filename, output_dir)
    
    # Close the figure to free memory
    plt.close(fig)
    
    return filepath

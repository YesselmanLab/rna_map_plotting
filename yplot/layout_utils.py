"""
Utility functions for subplot layout calculations.

This module contains helper functions that were extracted from the main
SubplotLayout class to keep the core functionality focused and clean.
"""

import warnings
from typing import Union, Dict, List, Tuple, Optional


def convert_coordinates_to_inches(coordinates, fig_size_inches):
    """
    Convert coordinate lists from figure-relative units (0-1) to actual inch measurements.

    This function takes subplot coordinates in figure-relative units (0-1) and converts
    them to actual inch measurements based on the figure size. This is useful when you
    need to know the actual physical dimensions of subplots for printing, layout planning,
    or other applications that require inch-based measurements.

    Parameters:
    -----------
    coordinates : tuple or list of tuples
        Subplot coordinates as (left, bottom, width, height) in figure-relative units (0-1).
        Can be a single tuple or list of tuples.
    fig_size_inches : tuple
        Figure size as (width, height) in inches

    Returns:
    --------
    tuple or list of tuples
        Converted coordinates as (left, bottom, width, height) in inches.
        Returns the same type as input (single tuple or list of tuples).

    Examples:
    ---------
    # Convert a single subplot coordinate
    coord = (0.1, 0.2, 0.3, 0.4)  # Relative units
    inch_coord = convert_coordinates_to_inches(coord, fig_size_inches=(10, 8))
    # Result: (1.0, 1.6, 3.0, 3.2) inches

    # Convert multiple subplot coordinates
    coords = [(0.1, 0.1, 0.3, 0.3), (0.6, 0.6, 0.3, 0.3)]
    inch_coords = convert_coordinates_to_inches(coords, fig_size_inches=(12, 10))
    # Result: [(1.2, 1.0, 3.6, 3.0), (7.2, 6.0, 3.6, 3.0)] inches
    """
    fig_width, fig_height = fig_size_inches

    def convert_single_coordinate(coord):
        """Convert a single coordinate tuple from relative to inch units."""
        left_rel, bottom_rel, width_rel, height_rel = coord

        # Convert to inches
        left_inches = left_rel * fig_width
        bottom_inches = bottom_rel * fig_height
        width_inches = width_rel * fig_width
        height_inches = height_rel * fig_height

        return (left_inches, bottom_inches, width_inches, height_inches)

    # Handle single coordinate or list of coordinates
    if isinstance(coordinates, tuple):
        return convert_single_coordinate(coordinates)
    elif isinstance(coordinates, list):
        return [convert_single_coordinate(coord) for coord in coordinates]
    else:
        raise ValueError("coordinates must be a tuple or list of tuples")


def expand_subplot_coordinates(
    coordinates,
    fig_size_inches,
    margins=None,
    spacing=None,
    include_adjacent_spacing=False,
):
    """
    Expand subplot coordinates to include margins and spacing around them.

    This function takes subplot coordinates and expands them to include the margins
    and spacing that would be around them if they were part of a larger figure layout.
    This is useful when you want to insert a figure into a specific subplot position
    and need to know the full area including margins and spacing.

    Parameters:
    -----------
    coordinates : tuple or list of tuples
        Subplot coordinates as (left, bottom, width, height) in figure-relative units (0-1).
        Can be a single tuple or list of tuples.
    fig_size_inches : tuple
        Figure size as (width, height) in inches
    margins : dict, optional
        Margins in inches: {'left': float, 'right': float, 'top': float, 'bottom': float}
        Default: {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75}
    spacing : dict, optional
        Spacing parameters. Can be:
        - Simple: {'hspace': float, 'wspace': float} - uniform spacing
        - Per-row: {'hspace': list, 'wspace': list} - per-row/col spacing
        Default: {'hspace': 0.5, 'wspace': 0.5}
    include_adjacent_spacing : bool, optional
        Whether to include spacing from adjacent subplots. If True, includes half
        the spacing on each side. If False, only includes margins.
        Default: True

    Returns:
    --------
    tuple or list of tuples
        Expanded coordinates as (left, bottom, width, height) in figure-relative units (0-1).
        Returns the same type as input (single tuple or list of tuples).
    """
    # Set default values
    if margins is None:
        margins = {"left": 0.75, "right": 0.75, "top": 0.75, "bottom": 0.75}

    if spacing is None:
        spacing = {"hspace": 0.5, "wspace": 0.5}

    fig_width, fig_height = fig_size_inches

    # Convert margins from inches to relative units
    margin_left_rel = margins["left"] / fig_width
    margin_right_rel = margins["right"] / fig_width
    margin_top_rel = margins["top"] / fig_height
    margin_bottom_rel = margins["bottom"] / fig_height

    # Handle spacing
    hspace = spacing.get("hspace", 0.5)
    wspace = spacing.get("wspace", 0.5)

    # Convert spacing from inches to relative units
    if isinstance(hspace, list):
        # Use average spacing for horizontal
        hspace_rel = sum(hspace) / len(hspace) / fig_width
    else:
        hspace_rel = hspace / fig_width

    if isinstance(wspace, list):
        # Use average spacing for vertical
        wspace_rel = sum(wspace) / len(wspace) / fig_height
    else:
        wspace_rel = wspace / fig_height

    # Calculate expansion amounts
    if include_adjacent_spacing:
        # Include half the spacing on each side
        expand_left = margin_left_rel + hspace_rel / 2
        expand_right = margin_right_rel + hspace_rel / 2
        expand_top = margin_top_rel + wspace_rel / 2
        expand_bottom = margin_bottom_rel + wspace_rel / 2
    else:
        # Only include margins
        expand_left = margin_left_rel
        expand_right = margin_right_rel
        expand_top = margin_top_rel
        expand_bottom = margin_bottom_rel

    def expand_single_coordinate(coord):
        """Expand a single coordinate tuple."""
        left, bottom, width, height = coord

        # Calculate expanded coordinates
        expanded_left = max(0.0, left - expand_left)
        expanded_bottom = max(0.0, bottom - expand_bottom)
        expanded_width = min(1.0 - expanded_left, width + expand_left + expand_right)
        expanded_height = min(
            1.0 - expanded_bottom, height + expand_bottom + expand_top
        )

        # Ensure coordinates are valid
        if expanded_width <= 0 or expanded_height <= 0:
            warnings.warn(
                f"Expanded coordinates result in zero or negative size: "
                f"width={expanded_width:.4f}, height={expanded_height:.4f}. "
                f"Original: {coord}"
            )

        return (expanded_left, expanded_bottom, expanded_width, expanded_height)

    # Handle single coordinate or list of coordinates
    if isinstance(coordinates, tuple):
        return expand_single_coordinate(coordinates)
    elif isinstance(coordinates, list):
        return [expand_single_coordinate(coord) for coord in coordinates]
    else:
        raise ValueError("coordinates must be a tuple or list of tuples")


def calculate_row_spacing(
    fig_size_inches, num_sub_plots, figure_width, margins=None, min_spacing=0.1
):
    """
    Calculate the required spacing between figures in a row given figure size and count.

    This function determines what the horizontal spacing must be between figures in a row
    to fit them all within the given figure size, and warns if it's not possible.

    Parameters:
    -----------
    fig_size_inches : tuple
        Figure size as (width, height) in inches
    num_sub_plots : int
        Number of subplots to fit in the row
    figure_width : float
        Width of each individual figure in inches
    margins : dict, optional
        Margins in inches: {'left': float, 'right': float}
        Default: {'left': 0.75, 'right': 0.75}
    min_spacing : float, optional
        Minimum acceptable spacing between figures in inches (default: 0.1)

    Returns:
    --------
    float
        Required spacing between figures in inches. Returns None if not possible.

    Examples:
    ---------
    # Calculate spacing for 3 figures of width 2.5 inches in a 10-inch wide figure
    spacing = calculate_row_spacing(
        fig_size_inches=(10, 6),
        num_sub_plots=3,
        figure_width=2.5
    )
    # Returns: 0.5 (inches between each figure)
    """
    if num_sub_plots <= 0:
        raise ValueError("num_figures must be positive")

    if figure_width <= 0:
        raise ValueError("figure_width must be positive")

    if min_spacing < 0:
        raise ValueError("min_spacing must be non-negative")

    # Set default margins if not provided
    if margins is None:
        margins = {"left": 0.4, "right": 0.0}

    fig_width = fig_size_inches[0]

    # Calculate total space needed for figures
    total_figure_width = num_sub_plots * figure_width

    # Calculate total space needed for margins
    total_margin_width = margins["left"] + margins["right"]

    # Calculate available space for spacing
    available_space = fig_width - total_figure_width - total_margin_width

    # Check if it's possible to fit the figures
    if available_space < 0:
        warnings.warn(
            f"Cannot fit {num_sub_plots} figures of width {figure_width:.2f} inches "
            f"in a figure of width {fig_width:.2f} inches with margins "
            f"left={margins['left']:.2f}, right={margins['right']:.2f}. "
            f"Total required width: {total_figure_width + total_margin_width:.2f} inches."
        )
        return None

    # Calculate spacing between figures
    if num_sub_plots == 1:
        # Only one figure, no spacing needed
        spacing = 0.0
    else:
        # Divide available space by number of gaps between figures
        num_gaps = num_sub_plots - 1
        spacing = available_space / num_gaps

        # Check if spacing meets minimum requirement (only for multiple figures)
        if spacing < min_spacing:
            warnings.warn(
                f"Calculated spacing {spacing:.3f} inches is less than minimum "
                f"required spacing {min_spacing:.3f} inches. Consider reducing "
                f"figure width, number of figures, or margins."
            )
            return None

    return spacing

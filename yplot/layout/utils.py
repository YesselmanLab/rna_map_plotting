"""
Utility functions for subplot layout calculations.

This module contains helper functions for coordinate conversion,
expansion, and spacing calculations.
"""

import warnings
from typing import Optional, Union

Coordinate = tuple[float, float, float, float]


def convert_to_inches(
    coordinates: Union[Coordinate, list[Coordinate]],
    fig_size_inches: tuple[float, float],
) -> Union[Coordinate, list[Coordinate]]:
    """
    Convert coordinates from figure-relative units (0-1) to inches.

    Args:
        coordinates: Single tuple or list of (left, bottom, width, height)
            tuples in figure-relative units.
        fig_size_inches: Figure size as (width, height) in inches.

    Returns:
        Converted coordinates in inches (same structure as input).

    Example:
        >>> coord = (0.1, 0.2, 0.3, 0.4)
        >>> convert_to_inches(coord, (10, 8))
        (1.0, 1.6, 3.0, 3.2)
    """
    fig_width, fig_height = fig_size_inches

    def convert_single(coord: Coordinate) -> Coordinate:
        left, bottom, width, height = coord
        return (
            left * fig_width,
            bottom * fig_height,
            width * fig_width,
            height * fig_height,
        )

    if isinstance(coordinates, tuple) and len(coordinates) == 4:
        return convert_single(coordinates)
    if isinstance(coordinates, list):
        return [convert_single(c) for c in coordinates]
    raise ValueError("coordinates must be a tuple or list of tuples")


def expand_coordinates(
    coordinates: Union[Coordinate, list[Coordinate]],
    fig_size_inches: tuple[float, float],
    margins: Optional[dict[str, float]] = None,
    spacing: Optional[dict[str, float]] = None,
    include_adjacent_spacing: bool = False,
) -> Union[Coordinate, list[Coordinate]]:
    """
    Expand subplot coordinates to include margins and spacing.

    Args:
        coordinates: Single tuple or list of (left, bottom, width, height).
        fig_size_inches: Figure size as (width, height) in inches.
        margins: Margins in inches with keys: left, right, top, bottom.
        spacing: Spacing with keys: hspace (horizontal), wspace (vertical).
        include_adjacent_spacing: If True, include half spacing on each side.

    Returns:
        Expanded coordinates (same structure as input).
    """
    if margins is None:
        margins = {"left": 0.75, "right": 0.75, "top": 0.75, "bottom": 0.75}
    if spacing is None:
        spacing = {"hspace": 0.5, "wspace": 0.5}

    fig_width, fig_height = fig_size_inches
    expansion = _calculate_expansion(
        margins, spacing, fig_width, fig_height, include_adjacent_spacing
    )

    if isinstance(coordinates, tuple) and len(coordinates) == 4:
        return _expand_single(coordinates, expansion)
    if isinstance(coordinates, list):
        return [_expand_single(c, expansion) for c in coordinates]
    raise ValueError("coordinates must be a tuple or list of tuples")


def _calculate_expansion(
    margins: dict[str, float],
    spacing: dict[str, float],
    fig_width: float,
    fig_height: float,
    include_adjacent: bool,
) -> dict[str, float]:
    """Calculate expansion amounts in relative units."""
    margin_left = margins["left"] / fig_width
    margin_right = margins["right"] / fig_width
    margin_top = margins["top"] / fig_height
    margin_bottom = margins["bottom"] / fig_height

    hspace = spacing.get("hspace", 0.5)
    wspace = spacing.get("wspace", 0.5)
    hspace_rel = (sum(hspace) / len(hspace) if isinstance(hspace, list) else hspace) / fig_width
    wspace_rel = (sum(wspace) / len(wspace) if isinstance(wspace, list) else wspace) / fig_height

    if include_adjacent:
        return {
            "left": margin_left + hspace_rel / 2,
            "right": margin_right + hspace_rel / 2,
            "top": margin_top + wspace_rel / 2,
            "bottom": margin_bottom + wspace_rel / 2,
        }
    return {
        "left": margin_left,
        "right": margin_right,
        "top": margin_top,
        "bottom": margin_bottom,
    }


def _expand_single(coord: Coordinate, expansion: dict[str, float]) -> Coordinate:
    """Expand a single coordinate tuple."""
    left, bottom, width, height = coord
    exp_left = max(0.0, left - expansion["left"])
    exp_bottom = max(0.0, bottom - expansion["bottom"])
    exp_width = min(1.0 - exp_left, width + expansion["left"] + expansion["right"])
    exp_height = min(1.0 - exp_bottom, height + expansion["bottom"] + expansion["top"])

    if exp_width <= 0 or exp_height <= 0:
        warnings.warn(
            f"Expanded coordinates result in invalid size: "
            f"width={exp_width:.4f}, height={exp_height:.4f}", stacklevel=2
        )

    return (exp_left, exp_bottom, exp_width, exp_height)


def calculate_row_spacing(
    fig_size_inches: tuple[float, float],
    num_subplots: int,
    subplot_width: float,
    margins: Optional[dict[str, float]] = None,
    min_spacing: float = 0.1,
) -> Optional[float]:
    """
    Calculate required spacing between subplots in a row.

    Args:
        fig_size_inches: Figure size as (width, height) in inches.
        num_subplots: Number of subplots in the row.
        subplot_width: Width of each subplot in inches.
        margins: Margins with keys: left, right.
        min_spacing: Minimum acceptable spacing (default: 0.1).

    Returns:
        Required spacing in inches, or None if not possible.
    """
    if num_subplots <= 0:
        raise ValueError("num_subplots must be positive")
    if subplot_width <= 0:
        raise ValueError("subplot_width must be positive")
    if min_spacing < 0:
        raise ValueError("min_spacing must be non-negative")

    if margins is None:
        margins = {"left": 0.4, "right": 0.0}

    fig_width = fig_size_inches[0]
    total_subplot_width = num_subplots * subplot_width
    total_margin_width = margins["left"] + margins["right"]
    available_space = fig_width - total_subplot_width - total_margin_width

    if available_space < 0:
        warnings.warn(
            f"Cannot fit {num_subplots} subplots of width {subplot_width:.2f} "
            f"in figure width {fig_width:.2f} with given margins.", stacklevel=2
        )
        return None

    if num_subplots == 1:
        return 0.0

    spacing = available_space / (num_subplots - 1)
    if spacing < min_spacing:
        warnings.warn(
            f"Calculated spacing {spacing:.3f} is less than minimum {min_spacing:.3f}.", stacklevel=2
        )
        return None

    return spacing

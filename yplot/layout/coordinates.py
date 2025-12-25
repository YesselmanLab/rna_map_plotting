"""
Coordinate calculation utilities for subplot layouts.

This module provides functions for calculating subplot positions
within a figure based on row-based configuration.
"""

import warnings
from typing import Any


def calculate_row_coordinates(
    rows: list[dict[str, Any]],
    fig_size_inches: tuple[float, float],
) -> list[tuple[float, float, float, float]]:
    """
    Calculate subplot coordinates from row configuration.

    Args:
        rows: List of row dictionaries with keys:
            - cols: Number of columns
            - width: Subplot width in inches
            - height: Subplot height in inches
            - hspace: Horizontal spacing between columns
            - wspace: Vertical spacing between rows
            - margins: Dict with left, right, top, bottom
        fig_size_inches: Figure size as (width, height) in inches.

    Returns:
        List of (left, bottom, width, height) tuples in figure-relative
        units (0-1) for each subplot, ordered row by row.
    """
    fig_width, fig_height = fig_size_inches
    _validate_layout_fits(rows, fig_height)

    row_bottoms = _calculate_row_bottoms(rows)
    coordinates = []

    for row_idx, row in enumerate(rows):
        col_lefts = _calculate_column_lefts(row)
        row_coords = _generate_row_coordinates(
            row, row_bottoms[row_idx], col_lefts, fig_width, fig_height
        )
        coordinates.extend(row_coords)

    return coordinates


def _validate_layout_fits(rows: list[dict[str, Any]], fig_height: float) -> None:
    """Warn if layout doesn't fit in figure height."""
    total_height = sum(row["height"] for row in rows)
    total_wspace = sum(row["wspace"] for row in rows[:-1])
    total_margins = rows[0]["margins"]["top"] + rows[-1]["margins"]["bottom"]
    required_height = total_height + total_wspace + total_margins

    if required_height > fig_height:
        warnings.warn(
            f"Subplot layout requires {required_height:.2f} inches height "
            f"but figure is {fig_height:.2f} inches. Subplots may overlap.", stacklevel=2
        )


def _calculate_row_bottoms(rows: list[dict[str, Any]]) -> list[float]:
    """Calculate bottom position for each row (from bottom to top)."""
    row_bottoms = []
    current_bottom = rows[-1]["margins"]["bottom"]

    for row_idx in range(len(rows) - 1, -1, -1):
        row_bottoms.insert(0, current_bottom)
        current_bottom += rows[row_idx]["height"]
        if row_idx > 0:
            current_bottom += rows[row_idx - 1]["wspace"]

    return row_bottoms


def _calculate_column_lefts(row: dict[str, Any]) -> list[float]:
    """Calculate left position for each column in a row."""
    col_lefts = []
    current_left = row["margins"]["left"]
    num_cols = row["cols"]
    hspace = row["hspace"]
    width = row["width"]

    for col in range(num_cols):
        col_lefts.append(current_left)
        current_left += width
        if col < num_cols - 1:
            current_left += hspace

    return col_lefts


def _generate_row_coordinates(
    row: dict[str, Any],
    row_bottom: float,
    col_lefts: list[float],
    fig_width: float,
    fig_height: float,
) -> list[tuple[float, float, float, float]]:
    """Generate coordinates for all subplots in a row."""
    coords = []
    for col_left in col_lefts:
        left_rel = col_left / fig_width
        bottom_rel = row_bottom / fig_height
        width_rel = row["width"] / fig_width
        height_rel = row["height"] / fig_height
        coords.append((left_rel, bottom_rel, width_rel, height_rel))
    return coords

"""
Layout system for yplot.

This module provides tools for defining and working with subplot layouts
using a row-based configuration format.
"""

from yplot.layout.coordinates import calculate_row_coordinates
from yplot.layout.subplot_layout import SubplotLayout
from yplot.layout.utils import (
    calculate_row_spacing,
    convert_to_inches,
    expand_coordinates,
)

# Backward compatibility alias
expand_subplot_coordinates = expand_coordinates
convert_coordinates_to_inches = convert_to_inches

__all__ = [
    "SubplotLayout",
    "calculate_row_coordinates",
    "convert_to_inches",
    "expand_coordinates",
    "calculate_row_spacing",
    # Backward compatibility
    "expand_subplot_coordinates",
    "convert_coordinates_to_inches",
]

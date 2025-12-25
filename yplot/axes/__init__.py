"""
Axes utilities for yplot.

This module provides functions for customizing matplotlib axes,
including sequence display, custom ticks, and log scale handling.
"""

from yplot.axes.log_scale import (
    compute_eps_and_transform,
    log_axis_with_zero,
)
from yplot.axes.sequence import (
    apply_x_axis_by_name,
    sequence_and_structure_x_axis,
    sequence_x_axis,
    structure_x_axis,
)
from yplot.axes.ticks import add_custom_ticks, set_tick_params

# Backward compatibility alias
compute_eps_and_xplot = compute_eps_and_transform

__all__ = [
    "sequence_x_axis",
    "structure_x_axis",
    "sequence_and_structure_x_axis",
    "apply_x_axis_by_name",
    "add_custom_ticks",
    "set_tick_params",
    "compute_eps_and_transform",
    "log_axis_with_zero",
    # Backward compatibility
    "compute_eps_and_xplot",
]

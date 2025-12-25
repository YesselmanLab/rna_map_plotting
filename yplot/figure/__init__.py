"""
Figure utilities for yplot.

This module provides functions for creating figures, adding labels,
loading images, and debugging layouts.
"""

from yplot.figure.create import create_figure_with_layout, create_figure_with_true_size
from yplot.figure.debug import (
    create_example_figure,
    draw_box_around_figure,
    draw_box_around_subplot,
    draw_boxes_around_subplots,
    render_example_figure,
    save_example_figure,
)
from yplot.figure.image import load_and_fit_image_to_subplot
from yplot.figure.labels import add_ax_corner_text, add_subplot_labels

__all__ = [
    "create_figure_with_layout",
    "create_figure_with_true_size",
    "add_subplot_labels",
    "add_ax_corner_text",
    "load_and_fit_image_to_subplot",
    "render_example_figure",
    "save_example_figure",
    "create_example_figure",
    "draw_box_around_figure",
    "draw_box_around_subplot",
    "draw_boxes_around_subplots",
]

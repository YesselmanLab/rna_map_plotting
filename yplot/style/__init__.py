"""
Style system for yplot.

This module provides tools for applying consistent styling to matplotlib
figures and axes, with support for presets and custom configurations.
"""

from yplot.style.apply import apply_style_to_figure, publication_style_ax
from yplot.style.presets import PRESETS, get_preset, list_presets, use

__all__ = [
    "publication_style_ax",
    "apply_style_to_figure",
    "use",
    "list_presets",
    "get_preset",
    "PRESETS",
]

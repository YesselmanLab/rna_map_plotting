"""
Annotation tools for scientific figures.

This module provides functions for adding statistical annotations,
significance brackets, arrows, scale bars, and callouts to plots.
"""

from yplot.annotate.elements import (
    add_arrow,
    add_callout,
    add_scale_bar,
    add_text_box,
    text,
)
from yplot.annotate.stats import (
    add_pvalue,
    add_significance,
    significance_bracket,
    star_notation,
)

__all__ = [
    # Statistical annotations
    "add_significance",
    "add_pvalue",
    "significance_bracket",
    "star_notation",
    # Visual elements
    "add_arrow",
    "add_scale_bar",
    "add_callout",
    "add_text_box",
    "text",
]

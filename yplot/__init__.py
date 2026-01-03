"""
yplot - Common plotting tools for DMS-MaPseq data visualization.

This library provides matplotlib-style configuration management and
specialized plotting functions for scientific publications.

Example:
    >>> import yplot
    >>> yplot.use('publication')
    >>> yplot.rcParams['font.size'] = 10
    >>> with yplot.rc_context({'axes.linewidth': 1.5}):
    ...     fig, axes = yplot.create_figure_with_layout(layout)
"""

__author__ = "Joe Yesselman"
__email__ = "jyesselm@unl.edu"
__version__ = "0.2.0"

# Configuration system
# Axes utilities
from yplot.axes import (
    add_custom_ticks,
    compute_eps_and_transform,
    compute_eps_and_xplot,
    log_axis_with_zero,
    sequence_and_structure_x_axis,
    sequence_x_axis,
    structure_x_axis,
)
from yplot.config import rc_context, rcParams

# Figure utilities
from yplot.figure import (
    add_ax_corner_text,
    add_subplot_labels,
    create_example_figure,
    create_figure_with_layout,
    create_figure_with_true_size,
    draw_box_around_figure,
    draw_box_around_subplot,
    draw_boxes_around_subplots,
    load_and_fit_image_to_subplot,
    render_example_figure,
    save_example_figure,
)

# Layout system
# Backward compatibility aliases
from yplot.layout import (
    SubplotLayout,
    calculate_row_spacing,
    convert_coordinates_to_inches,
    convert_to_inches,
    expand_coordinates,
    expand_subplot_coordinates,
)

# Legend utilities
from yplot.legend import add_legend, add_legend_above_subplot

# Plot functions
from yplot.plots import (
    lollipop_plot,
    plot_pop_avg,
    plot_pop_avg_all,
    plot_pop_avg_diff_from_rows,
    plot_pop_avg_from_row,
    plot_pop_avg_traces_all,
    plot_regression_line,
    scatter_plot_w_regression,
)

# Style system
from yplot.style import publication_style_ax, use

# Utility functions
from yplot.utils import colors_for_sequence, get_logger, setup_applevel_logger

# DataFrame-first plotting API
from yplot import plot

# Annotations
from yplot.annotate import (
    add_significance,
    add_pvalue,
    significance_bracket,
    star_notation,
    add_arrow,
    add_scale_bar,
    add_callout,
    add_text_box,
    text,
)

__all__ = [
    # Version info
    "__author__",
    "__email__",
    "__version__",
    # Config
    "rcParams",
    "rc_context",
    "use",
    # Style
    "publication_style_ax",
    # Layout
    "SubplotLayout",
    "expand_coordinates",
    "convert_to_inches",
    "calculate_row_spacing",
    # Figure
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
    # Plots
    "scatter_plot_w_regression",
    "lollipop_plot",
    "plot_regression_line",
    "plot_pop_avg",
    "plot_pop_avg_from_row",
    "plot_pop_avg_diff_from_rows",
    "plot_pop_avg_all",
    "plot_pop_avg_traces_all",
    # Axes
    "sequence_x_axis",
    "structure_x_axis",
    "sequence_and_structure_x_axis",
    "add_custom_ticks",
    "compute_eps_and_transform",
    "log_axis_with_zero",
    # Legend
    "add_legend",
    "add_legend_above_subplot",
    # Utils
    "colors_for_sequence",
    "get_logger",
    "setup_applevel_logger",
    # Backward compatibility
    "expand_subplot_coordinates",
    "convert_coordinates_to_inches",
    "compute_eps_and_xplot",
    # DataFrame plotting API
    "plot",
    # Annotations
    "add_significance",
    "add_pvalue",
    "significance_bracket",
    "star_notation",
    "add_arrow",
    "add_scale_bar",
    "add_callout",
    "add_text_box",
    "text",
]

"""
Plot types for yplot.

This module provides various plot functions including scatter plots,
lollipop plots, bar plots, and regression utilities.
"""

from yplot.plots.bar import (
    plot_pop_avg,
    plot_pop_avg_all,
    plot_pop_avg_diff_from_rows,
    plot_pop_avg_from_row,
    plot_pop_avg_traces_all,
)
from yplot.plots.lollipop import lollipop_plot
from yplot.plots.regression import plot_regression_line
from yplot.plots.scatter import scatter_plot_w_regression

__all__ = [
    "scatter_plot_w_regression",
    "lollipop_plot",
    "plot_regression_line",
    "plot_pop_avg",
    "plot_pop_avg_from_row",
    "plot_pop_avg_diff_from_rows",
    "plot_pop_avg_all",
    "plot_pop_avg_traces_all",
]

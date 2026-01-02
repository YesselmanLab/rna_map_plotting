"""
DataFrame-first plotting API for yplot.

This module provides a seaborn-like interface where data and column names
are the primary inputs, making plots easy to create from DataFrames.

Example:
    >>> import yplot.plot as yp
    >>> yp.scatter(df, x='concentration', y='response', color='treatment')
    >>> yp.bar(df, x='condition', y='mean', error='std')
"""

from yplot.plot.bar import bar, grouped_bar
from yplot.plot.distribution import box, strip, swarm, violin
from yplot.plot.line import line
from yplot.plot.matrix import heatmap
from yplot.plot.scatter import scatter

__all__ = [
    "scatter",
    "line",
    "bar",
    "grouped_bar",
    "violin",
    "box",
    "swarm",
    "strip",
    "heatmap",
]

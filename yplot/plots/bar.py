"""
Bar plot utilities for population average data.

This module provides functions for creating bar plots to display
reactivity data, particularly for RNA/DNA sequences.
"""

from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from yplot.axes.sequence import apply_x_axis_by_name
from yplot.utils.colors import colors_for_sequence


def plot_pop_avg(
    sequence: str,
    structure: str,
    reactivities: list[float],
    ax: Optional[plt.Axes] = None,
    axis: str = "sequence_structure",
) -> plt.Axes:
    """
    Plot population average reactivities for an RNA sequence.

    Each nucleotide is colored by identity, with the x-axis showing
    sequence and/or structure information.

    Args:
        sequence: The RNA sequence.
        structure: The secondary structure string.
        reactivities: Reactivity values for each nucleotide.
        ax: Matplotlib Axes to plot on (creates new if None).
        axis: X-axis type: "sequence_structure", "sequence", or "structure".

    Returns:
        The matplotlib Axes containing the bar plot.

    Example:
        >>> plot_pop_avg("ACGU", "(..)", [0.1, 0.2, 0.3, 0.4])
    """
    if ax is None:
        _, ax = plt.subplots()

    sequence = sequence.replace("U", "T")
    colors = colors_for_sequence(sequence)
    ax.bar(range(len(reactivities)), reactivities, color=colors)
    apply_x_axis_by_name(ax, sequence, structure, axis)

    return ax


def plot_pop_avg_from_row(
    row: dict,
    ax: Optional[plt.Axes] = None,
    data_col: str = "data",
) -> plt.Axes:
    """
    Plot population average from a data row.

    Args:
        row: Dictionary-like object with 'sequence', 'structure', and data.
        ax: Matplotlib Axes to plot on.
        data_col: Column name containing reactivity data.

    Returns:
        The matplotlib Axes containing the bar plot.
    """
    return plot_pop_avg(
        row["sequence"],
        row["structure"],
        row[data_col],
        ax=ax,
    )


def plot_pop_avg_diff_from_rows(
    row1: dict,
    row2: dict,
    data_col: str = "data",
    axes: Optional[Union[list[plt.Axes], np.ndarray]] = None,
    **kwargs,
) -> plt.Figure:
    """
    Plot population average difference between two conditions.

    Creates three panels: row1 data, row2 data, and their difference.

    Args:
        row1: First data row.
        row2: Second data row.
        data_col: Column name containing reactivity data.
        axes: Array of 3 axes to plot on.
        **kwargs: Additional arguments for plt.subplots().

    Returns:
        The matplotlib Figure containing the plots.
    """
    if axes is None:
        fig, axes = plt.subplots(3, 1, **kwargs)
    else:
        fig = axes[0].get_figure()

    plot_pop_avg_from_row(row1, ax=axes[0], data_col=data_col)
    plot_pop_avg_from_row(row2, ax=axes[1], data_col=data_col)

    diff_row = {
        "sequence": row1["sequence"],
        "structure": row1["structure"],
        data_col: np.array(row1[data_col]) - np.array(row2[data_col]),
    }
    plot_pop_avg_from_row(diff_row, ax=axes[2], data_col=data_col)

    return fig


def plot_pop_avg_all(
    df: pd.DataFrame,
    data_col: str = "data",
    axes: Optional[Union[list[plt.Axes], np.ndarray]] = None,
    **kwargs,
) -> plt.Figure:
    """
    Plot population average for each row in a DataFrame.

    Args:
        df: DataFrame with sequence, structure, and data columns.
        data_col: Column name containing reactivity data.
        axes: Array of axes to plot on (one per row).
        **kwargs: Additional arguments for plt.subplots().

    Returns:
        The matplotlib Figure containing all plots.
    """
    n = len(df)
    if axes is None:
        fig, axes = plt.subplots(n, 1, **kwargs)
    else:
        fig = axes[0].get_figure()

    if n == 1 and not isinstance(axes, (list, np.ndarray)):
        axes = [axes]

    for j, (_, row) in enumerate(df.iterrows()):
        plot_pop_avg_from_row(row, ax=axes[j], data_col=data_col)
        if "rna_name" in row:
            axes[j].set_title(row["rna_name"])

    return fig


def plot_pop_avg_traces_all(
    df: pd.DataFrame,
    data_col: str = "data",
    label_col: str = "rna_name",
    ax: Optional[plt.Axes] = None,
) -> plt.Axes:
    """
    Plot overlaid population average traces for all rows.

    Args:
        df: DataFrame with data and label columns.
        data_col: Column containing trace data.
        label_col: Column containing trace labels.
        ax: Matplotlib Axes to plot on.

    Returns:
        The matplotlib Axes containing the traces.
    """
    if ax is None:
        _, ax = plt.subplots()

    for _, row in df.iterrows():
        ax.plot(row[data_col], label=row[label_col])

    return ax

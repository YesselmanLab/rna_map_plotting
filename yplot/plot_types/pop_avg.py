import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Optional, Union

from yplot.util import colors_for_sequence
from yplot.axes import sequence_and_structure_x_axis, sequence_x_axis, structure_x_axis


def apply_x_axis_by_name(ax: plt.Axes, sequence: str, structure: str, axis_type: str):
    """
    Apply an x-axis labeling strategy by name.

    Args:
        ax (plt.Axes): The matplotlib Axes to set x-ticks/labels on.
        sequence (str): Sequence string (e.g. "ACGU").
        structure (str): Structure string (e.g. "(..(").
        axis_type (str): One of "sequence_structure", "sequence", "structure".

    Returns:
        plt.Axes: The modified matplotlib Axes.
    """
    if axis_type == "sequence_structure":
        return sequence_and_structure_x_axis(ax, sequence, structure)
    elif axis_type == "sequence":
        return sequence_x_axis(ax, sequence)
    elif axis_type == "structure":
        return structure_x_axis(ax, structure)
    else:
        raise ValueError(f"Unknown axis_type: {axis_type}")


def plot_pop_avg(
    sequence: str,
    structure: str,
    reactivities: List[float],
    ax: Optional[plt.Axes] = None,
    axis: str = "sequence_structure",
) -> plt.Axes:
    """
    Plot the population average reactivities for a given RNA sequence on the provided matplotlib Axes.

    Each nucleotide in the sequence is colored according to its identity, and the x-axis is labeled
    with both the sequence and the corresponding secondary structure.

    Args:
        seq (str): The RNA sequence.
        ss (str): The secondary structure string corresponding to the sequence.
        reactivities (List[float]): Reactivity values for each nucleotide in the sequence.
        ax (plt.Axes, optional): The matplotlib Axes object to plot on. If None, a new one is created.

    Returns:
        plt.Axes: The matplotlib Axes object containing the population average reactivity bar plot.

    Example:
        >>> fig, ax = plt.subplots()
        >>> plot_pop_avg("ACGU", "(..)", [0.1, 0.2, 0.3, 0.4], ax)
        >>> plt.show()
    """
    if ax is None:
        _, ax = plt.subplots()
    sequence = sequence.replace("U", "T")  # should be RNA
    colors = colors_for_sequence(sequence)
    ax.bar(range(0, len(reactivities)), reactivities, color=colors)
    apply_x_axis_by_name(ax, sequence, structure, axis)
    return ax


def plot_pop_avg_from_row(
    row, ax: Optional[plt.Axes] = None, data_col: str = "data"
) -> plt.Axes:
    """
    Plots the population average from a given row of data.

    Args:
        row: A dictionary-like object representing a row of data.
        data_col: The name of the column containing the data to plot. Default is "data".
        ax: The matplotlib Axes object to plot on. If not provided, a new one is created.

    Returns:
        The matplotlib Axes object containing the plot.

    Raises:
        None.

    Example:
        >>> row = {"sequence": "ACGU", "structure": "(((.)))", "data": [0.1, 0.2, 0.3, 0.4]}
        >>> plot_pop_avg_from_row(row)
    """
    return plot_pop_avg(row["sequence"], row["structure"], row[data_col], ax=ax)


def plot_pop_avg_diff_from_rows(
    row1,
    row2,
    data_col="data",
    axes: Optional[Union[List[plt.Axes], np.ndarray]] = None,
    **kwargs,
) -> plt.Figure:
    """
    Plots the population average difference between two rows.

    Args:
        row1 (dict): The first row containing the data.
        row2 (dict): The second row containing the data.
        data_col (str, optional): The column name for the data. Defaults to "data".
        axes (list or np.ndarray of plt.Axes, optional): Array or list of axes to plot the 3 panels on.
        **kwargs: Additional keyword arguments to be passed to plt.subplots() (only if axes is None).

    Returns:
        matplotlib.figure.Figure: The generated figure.

    Raises:
        None

    Example:
        row1 = {"sequence": "ACGU", "structure": "((((", "data": [1, 2, 3, 4]}
        row2 = {"sequence": "ACGU", "structure": "((((", "data": [5, 6, 7, 8]}
        fig = plot_pop_avg_diff_from_rows(row1, row2)
        plt.show()
    """
    if axes is None:
        fig, axes = plt.subplots(3, 1, **kwargs)
    else:
        fig = axes[0].get_figure()  # Try to get a figure from passed axes

    plot_pop_avg_from_row(row1, ax=axes[0], data_col=data_col)
    plot_pop_avg_from_row(row2, ax=axes[1], data_col=data_col)
    diff = {
        "sequence": row1["sequence"],
        "structure": row1["structure"],
        data_col: np.array(row1[data_col]) - np.array(row2[data_col]),
    }
    plot_pop_avg_from_row(diff, ax=axes[2], data_col=data_col)
    return fig


def plot_pop_avg_all(
    df: pd.DataFrame,
    data_col: str = "data",
    axes: Optional[Union[List[plt.Axes], np.ndarray]] = None,
    **kwargs,
) -> plt.Figure:
    """
    Plots the population average for each row in the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be plotted.
        data_col (str, optional): The column name in the DataFrame that contains the data to be plotted.
            Defaults to "data".
        axes (list or np.ndarray of plt.Axes, optional): The axes for plotting each row.
        **kwargs: Additional keyword arguments to be passed to the `subplots` function if axes not given.

    Returns:
        plt.Figure: The matplotlib Figure object containing the plot.

    Raises:
        None

    Example:
        df = pd.DataFrame({
            "sequence": ["ACGU", "UGCA", "CGAU"],
            "data": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
            "rna_name": ["RNA1", "RNA2", "RNA3"]
        })
        fig = plot_pop_avg_all(df, data_col="data")
        plt.show()
    """
    n = len(df)
    if axes is None:
        fig, axes = plt.subplots(n, 1, **kwargs)
    else:
        fig = axes[0].get_figure()
    # For 1-row, axes may not be a list/array
    if n == 1 and not isinstance(axes, (list, np.ndarray)):
        axes = [axes]
    for j, (_, row) in enumerate(df.iterrows()):
        plot_pop_avg_from_row(row, ax=axes[j], data_col=data_col)
        if "rna_name" in row:
            axes[j].set_title(row["rna_name"])
    # Optionally could highlight last row or something more
    return fig


def plot_pop_avg_traces_all(
    df: pd.DataFrame,
    data_col="data",
    label_col="rna_name",
    ax: Optional[plt.Axes] = None,
):
    """
    Plots population average traces for all RNA names in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data to be plotted.
        data_col (str, optional): The column name in the DataFrame that contains the data to be plotted.
            Defaults to "data".
        label_col (str, optional): The column name in the DataFrame that contains the labels to be plotted.
            Defaults to "rna_name".
        ax (matplotlib.axes.Axes, optional): The axes to plot on. If None, a new one is created.

    Returns:
        matplotlib.axes.Axes: The generated axes object.

    """
    if ax is None:
        fig, ax = plt.subplots(1, 1)
    for i, row in df.iterrows():
        ax.plot(row[data_col], label=row[label_col])
    return ax

import matplotlib.pyplot as plt
import matplotlib.axes as axes
import numpy as np
import pandas as pd
from typing import List, Union, Optional

from rna_map_plotting.logger import get_logger

log = get_logger(__name__)


def colors_for_sequence(seq: str) -> list:
    """
    Returns a list of colors corresponding to the input DNA/RNA sequence.

    This function maps each character in the input DNA/RNA sequence to a specific color:
    - 'A' -> 'red'
    - 'C' -> 'blue'
    - 'G' -> 'orange'
    - 'T' -> 'green'
    - 'U' -> 'green'

    Args:
        seq (str): A string representing a RNA/DNA sequence. The sequence is
                   expected to contain only the characters 'A', 'C', 'G', 'U', and 'T'.

    Returns:
        list: A list of strings where each element is a color corresponding
              to a character in the DNA sequence.

    Raises:
        ValueError: If the sequence contains characters other than 'A', 'C',
                    'G', 'U' and 'T'.

    Example:
        >>> colors_for_sequence("ACGT")
        ['red', 'blue', 'orange', 'green']

    """
    color_mapping = {"A": "red", "C": "blue", "G": "orange", "T": "green", "U": "green"}
    colors = []
    for e in seq:
        try:
            color = color_mapping[e]
            colors.append(color)
        except KeyError as exc:
            log.error(
                f"Invalid character {e} in sequence. Sequence must contain only 'A', 'C', 'G', 'U', and 'T'."
            )
            raise ValueError(f"Invalid character {e} in sequence.") from exc

    log.debug(f"Input Sequence: {seq}")
    log.debug(f"Output Colors: {colors}")
    return colors


def plot_pop_avg(
    seq: str, ss: str, reactivities: List[float], ax: Optional[plt.Axes] = None
) -> plt.Axes:
    """
    Plots the population average reactivities for a given RNA sequence.

    Args:
        seq (str): The RNA sequence.
        ss (str): The secondary structure of the RNA sequence.
        reactivities (List[float]): The list of reactivities corresponding to each nucleotide in the sequence.
        ax (Optional[plt.Axes]): The matplotlib Axes object to plot on. If not provided, a new figure and Axes will be created.

    Returns:
        plt.Axes: The matplotlib Axes object containing the plot.

    """
    colors = colors_for_sequence(seq)
    x = list(range(len(seq)))
    if ax is None:
        fig, ax = plt.subplots(1, figsize=(20, 4))
    ax.bar(range(0, len(reactivities)), reactivities, color=colors)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{s}\n{nt}" for s, nt in zip(seq, ss)])
    return ax


def plot_pop_avg_from_row(row, data_col: str = "data", ax=None) -> plt.Axes:
    """
    Plots the population average from a given row of data.

    Args:
        row: A dictionary-like object representing a row of data.
        data_col: The name of the column containing the data to plot. Default is "data".
        ax: The matplotlib Axes object to plot on. If not provided, a new figure and axes will be created.

    Returns:
        The matplotlib Axes object containing the plot.

    Raises:
        None.

    Example:
        >>> row = {"sequence": "ACGU", "structure": "(((.)))", "data": [0.1, 0.2, 0.3, 0.4]}
        >>> plot_pop_avg_from_row(row)
    """
    return plot_pop_avg(row["sequence"], row["structure"], row[data_col], ax)


def plot_pop_avg_diff_from_rows(row1, row2, data_col="data", **kwargs) -> plt.Figure:
    """
    Plots the population average difference between two rows.

    Args:
        row1 (dict): The first row containing the data.
        row2 (dict): The second row containing the data.
        data_col (str, optional): The column name for the data. Defaults to "data".
        **kwargs: Additional keyword arguments to be passed to plt.subplots().

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
    fig, axes = plt.subplots(3, 1, **kwargs)
    plot_pop_avg_from_row(row1, data_col, axes[0])
    plot_pop_avg_from_row(row2, data_col, axes[1])
    diff = {
        "sequence": row1["sequence"],
        "structure": row1["structure"],
        data_col: np.array(row1[data_col]) - np.array(row2[data_col]),
    }
    plot_pop_avg_from_row(diff, data_col, axes[2])
    return fig


def plot_pop_avg_all(df: pd.DataFrame, data_col: str = "data", **kwargs) -> plt.Figure:
    """
    Plots the population average for each row in the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to be plotted.
        data_col (str, optional): The column name in the DataFrame that contains the data to be plotted.
            Defaults to "data".
        **kwargs: Additional keyword arguments to be passed to the `subplots` function.

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
    fig, axes = plt.subplots(len(df), 1, **kwargs)
    j = 0
    for i, row in df.iterrows():
        colors = colors_for_sequence(row["sequence"])
        axes[j].bar(range(0, len(row[data_col])), row[data_col], color=colors)
        axes[j].set_title(row["rna_name"])
        j += 1
    plot_pop_avg_from_row(df.iloc[-1], ax=axes[-1])
    return fig


def plot_pop_avg_traces_all(df: pd.DataFrame, **kwargs):
    """
    Plots population average traces for all RNA names in the given DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the data to be plotted.
        **kwargs: Additional keyword arguments to be passed to the plt.subplots() function.

    Returns:
        matplotlib.figure.Figure: The generated figure object.

    """
    fig, ax = plt.subplots(1, 1, **kwargs)
    for i, row in df.iterrows():
        plt.plot(row["data"], label=row["rna_name"])
    fig.legend(loc="upper left")
    return fig

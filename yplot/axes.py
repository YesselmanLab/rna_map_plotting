import matplotlib.pyplot as plt
import numpy as np
from typing import List, Union, Tuple, Optional, Sequence
from matplotlib.ticker import FixedLocator, LogLocator, FuncFormatter


def sequence_and_structure_x_axis(
    ax: plt.Axes, sequence: str, structure: str, x_delta: int = 1
) -> List[str]:
    """
    Set the x-axis of the given matplotlib Axes to display both the sequence and secondary
    structure.

    The x-axis tick labels will show each nucleotide in the sequence, with the corresponding
    secondary structure character below it (separated by a newline).

    Args:
        ax (plt.Axes): The matplotlib Axes object to modify.
        sequence (str): The RNA or DNA sequence string.
        structure (str): The secondary structure string (e.g., dot-bracket notation),
            same length as sequence.

    Returns:
        plt.Axes: The modified matplotlib Axes object with updated x-axis tick labels.

    Example:
        >>> fig, ax = plt.subplots()
        >>> sequence_and_structure_x_axis(ax, "ACGU", "(((.")
        >>> plt.show()
    """
    x = list(range(len(sequence)))
    ax.set_xticks(x)
    ax.set_xticklabels([f"{s}\n{nt}" for s, nt in zip(sequence, structure)])
    ax.set_xlim([-x_delta, len(sequence) + x_delta])
    return ax


def sequence_x_axis(ax: plt.Axes, sequence: str, x_delta: int = 1) -> List[str]:
    """
    Set the x-axis of the given matplotlib Axes to display the sequence.

    The x-axis tick labels will show each nucleotide in the sequence.
    """
    ax.set_xticks(range(0, len(sequence)))
    ax.set_xticklabels(sequence)
    ax.set_xlim([-x_delta, len(sequence) + x_delta])
    return ax


def structure_x_axis(ax: plt.Axes, structure: str, x_delta: int = 1) -> List[str]:
    """
    Set the x-axis of the given matplotlib Axes to display the structure.

    The x-axis tick labels will show each nucleotide in the structure.
    """
    ax.set_xticks(range(0, len(structure)))
    ax.set_xticklabels(structure)
    ax.set_xlim([-x_delta, len(structure) + x_delta])
    return ax


def add_custom_ticks(
    ax: plt.Axes, axis: str, min_val: float, max_val: float, num_ticks: int
) -> plt.Axes:
    """
    Add custom ticks to either the x or y axis of a matplotlib Axes object.

    Creates evenly spaced ticks between min_val and max_val (inclusive).

    Args:
        ax (plt.Axes): The matplotlib Axes object to modify.
        axis (str): Which axis to modify ('x' or 'y').
        min_val (float): Minimum value for the ticks.
        max_val (float): Maximum value for the ticks.
        num_ticks (int): Number of ticks to create (including endpoints).

    Returns:
        plt.Axes: The modified matplotlib Axes object.

    Example:
        >>> fig, ax = plt.subplots()
        >>> add_custom_ticks(ax, 'x', 0.0, 0.5, 6)  # Creates ticks: 0.0, 0.1, 0.2, 0.3, 0.4, 0.5
        >>> plt.show()
    """
    if num_ticks < 2:
        raise ValueError("num_ticks must be at least 2")

    # Generate evenly spaced ticks
    ticks = np.linspace(min_val, max_val, num_ticks, endpoint=True)
    print(ticks)

    # Set ticks on the specified axis
    if axis.lower() == "x":
        ax.set_xticks(ticks)
    elif axis.lower() == "y":
        ax.set_yticks(ticks)
    else:
        raise ValueError("axis must be 'x' or 'y'")

    return ax


def compute_eps_and_xplot(
    x: np.ndarray, epsilon_factor: float = 0.1
) -> Tuple[float, np.ndarray, np.ndarray]:
    pos = x[x > 0]
    if pos.size == 0:
        raise ValueError("All x values are zero; cannot use log scale.")
    eps = epsilon_factor * float(np.min(pos))
    x_plot = x.copy()
    x_plot[x_plot <= 0] = eps
    return eps, pos, x_plot


def log_axis_with_zero(
    ax,
    eps: float,
    pos: np.ndarray,
    decade_ticks: Optional[Sequence[float]] = None,
    left_pad: float = 1.5,
    right_pad: float = 1.5,
) -> None:
    ax.set_xscale("log")

    if decade_ticks is None:
        lo_pow = int(np.floor(np.log10(max(eps, float(np.min(pos)) * 0.8))))
        hi_pow = int(np.ceil(np.log10(float(np.max(pos)) * 1.2)))
        decade_ticks = [10.0**p for p in range(lo_pow, hi_pow + 1)]

    tick_positions = [eps] + [
        t for t in decade_ticks if eps <= t <= float(np.max(pos)) * 1.05
    ]
    ax.xaxis.set_major_locator(FixedLocator(tick_positions))

    def _fmt_tick(val, _pos=None):
        return "0" if np.isclose(val, eps) else f"{val:g}"

    ax.xaxis.set_major_formatter(FuncFormatter(_fmt_tick))
    # ax.xaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10)))
    ax.set_xlim(eps / left_pad, float(np.max(pos)) * right_pad)

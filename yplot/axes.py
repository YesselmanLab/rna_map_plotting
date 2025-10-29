import matplotlib.pyplot as plt
from typing import List


def sequence_and_structure_x_axis(
    ax: plt.Axes, sequence: str, structure: str
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
    return ax


def sequence_x_axis(ax: plt.Axes, sequence: str) -> List[str]:
    """
    Set the x-axis of the given matplotlib Axes to display the sequence.

    The x-axis tick labels will show each nucleotide in the sequence.
    """
    ax.set_xticks(range(0, len(sequence)))
    ax.set_xticklabels(sequence)
    return ax


def structure_x_axis(ax: plt.Axes, structure: str) -> List[str]:
    """
    Set the x-axis of the given matplotlib Axes to display the structure.

    The x-axis tick labels will show each nucleotide in the structure.
    """
    ax.set_xticks(range(0, len(structure)))
    ax.set_xticklabels(structure)
    return ax

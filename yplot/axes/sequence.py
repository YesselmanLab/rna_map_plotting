"""
Sequence and structure axis formatting for molecular data.

This module provides functions to display RNA/DNA sequences and
secondary structures on matplotlib axes.
"""


import matplotlib.pyplot as plt


def sequence_x_axis(
    ax: plt.Axes,
    sequence: str,
    x_delta: int = 1,
) -> plt.Axes:
    """
    Set x-axis to display nucleotide sequence.

    Args:
        ax: The matplotlib Axes object to modify.
        sequence: The RNA or DNA sequence string.
        x_delta: Padding around sequence bounds (default: 1).

    Returns:
        The modified matplotlib Axes object.

    Example:
        >>> fig, ax = plt.subplots()
        >>> sequence_x_axis(ax, "ACGU")
    """
    ax.set_xticks(range(len(sequence)))
    ax.set_xticklabels(list(sequence))
    ax.set_xlim(-x_delta, len(sequence) - 1 + x_delta)
    return ax


def structure_x_axis(
    ax: plt.Axes,
    structure: str,
    x_delta: int = 1,
) -> plt.Axes:
    """
    Set x-axis to display secondary structure notation.

    Args:
        ax: The matplotlib Axes object to modify.
        structure: The secondary structure string (dot-bracket notation).
        x_delta: Padding around structure bounds (default: 1).

    Returns:
        The modified matplotlib Axes object.

    Example:
        >>> fig, ax = plt.subplots()
        >>> structure_x_axis(ax, "(((.)))")
    """
    ax.set_xticks(range(len(structure)))
    ax.set_xticklabels(list(structure))
    ax.set_xlim(-x_delta, len(structure) - 1 + x_delta)
    return ax


def sequence_and_structure_x_axis(
    ax: plt.Axes,
    sequence: str,
    structure: str,
    x_delta: int = 1,
) -> plt.Axes:
    """
    Set x-axis to display both sequence and structure.

    Each tick label shows the nucleotide with structure character below.

    Args:
        ax: The matplotlib Axes object to modify.
        sequence: The RNA or DNA sequence string.
        structure: The secondary structure string (same length as sequence).
        x_delta: Padding around bounds (default: 1).

    Returns:
        The modified matplotlib Axes object.

    Example:
        >>> fig, ax = plt.subplots()
        >>> sequence_and_structure_x_axis(ax, "ACGU", "(((.")
    """
    labels = [f"{seq}\n{struct}" for seq, struct in zip(sequence, structure)]
    ax.set_xticks(range(len(sequence)))
    ax.set_xticklabels(labels)
    ax.set_xlim(-x_delta, len(sequence) - 1 + x_delta)
    return ax


def apply_x_axis_by_name(
    ax: plt.Axes,
    sequence: str,
    structure: str,
    axis_type: str,
) -> plt.Axes:
    """
    Apply x-axis labeling strategy by name.

    Args:
        ax: The matplotlib Axes to modify.
        sequence: Sequence string.
        structure: Structure string.
        axis_type: One of "sequence_structure", "sequence", "structure".

    Returns:
        The modified matplotlib Axes.

    Raises:
        ValueError: If axis_type is not recognized.
    """
    axis_functions = {
        "sequence_structure": lambda: sequence_and_structure_x_axis(
            ax, sequence, structure
        ),
        "sequence": lambda: sequence_x_axis(ax, sequence),
        "structure": lambda: structure_x_axis(ax, structure),
    }

    if axis_type not in axis_functions:
        raise ValueError(f"Unknown axis_type: {axis_type}")

    return axis_functions[axis_type]()

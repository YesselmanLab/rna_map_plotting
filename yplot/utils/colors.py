"""
Color utilities for sequence visualization.

This module provides color mappings for RNA/DNA nucleotides.
"""


COLOR_MAPPING = {
    "A": "red",
    "C": "blue",
    "G": "orange",
    "T": "green",
    "U": "green",
    "&": "gray",
}


def colors_for_sequence(seq: str) -> list[str]:
    """
    Get colors for each nucleotide in a sequence.

    Maps each nucleotide character to a specific color:
        - A: red
        - C: blue
        - G: orange
        - T/U: green
        - &: gray

    Args:
        seq: RNA or DNA sequence string.

    Returns:
        List of color strings corresponding to each nucleotide.

    Raises:
        ValueError: If sequence contains invalid characters.

    Example:
        >>> colors_for_sequence("ACGU")
        ['red', 'blue', 'orange', 'green']
    """
    colors = []
    for char in seq.upper():
        if char not in COLOR_MAPPING:
            raise ValueError(
                f"Invalid character '{char}' in sequence. "
                f"Valid characters: {list(COLOR_MAPPING.keys())}"
            )
        colors.append(COLOR_MAPPING[char])

    return colors

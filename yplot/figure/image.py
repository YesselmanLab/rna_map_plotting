"""
Image loading utilities for figures.

This module provides functions for loading and displaying images
within matplotlib subplots.
"""

from pathlib import Path
from typing import Union

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.image import AxesImage


def load_and_fit_image_to_subplot(
    image_path: Union[str, Path],
    ax: plt.Axes,
) -> AxesImage:
    """
    Load and display an image stretched to fit a subplot.

    Args:
        image_path: Path to the image file.
        ax: Matplotlib Axes where the image will be displayed.

    Returns:
        The AxesImage object.

    Raises:
        ValueError: If image cannot be loaded.

    Example:
        >>> fig, ax = plt.subplots()
        >>> load_and_fit_image_to_subplot("figure.png", ax)
    """
    try:
        img = mpimg.imread(str(image_path))
    except Exception as e:
        raise ValueError(f"Could not load image from {image_path}: {e}") from e

    ax.clear()
    img_plot = ax.imshow(img)
    _hide_axes(ax)

    return img_plot


def _hide_axes(ax: plt.Axes) -> None:
    """Remove all axes decorations for image display."""
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    for spine in ax.spines.values():
        spine.set_visible(False)

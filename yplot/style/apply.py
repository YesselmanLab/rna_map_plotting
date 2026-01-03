"""
Style application functions for matplotlib axes.

This module provides functions to apply consistent styling to
matplotlib axes objects using yplot's configuration system.
"""

from typing import Optional

import matplotlib.pyplot as plt

from yplot.config import rcParams


def publication_style_ax(
    ax: plt.Axes,
    fsize: Optional[int] = None,
    ytick_size: Optional[int] = None,
    xtick_size: Optional[int] = None,
) -> None:
    """
    Apply publication-quality styling to a matplotlib Axes.

    Uses values from rcParams unless explicitly overridden.

    Args:
        ax: The matplotlib Axes object to style.
        fsize: Font size for labels/title. Defaults to rcParams['axes.labelsize'].
        ytick_size: Y-axis tick label size. Defaults to rcParams['ytick.labelsize'].
        xtick_size: X-axis tick label size. Defaults to rcParams['xtick.labelsize'].
    """
    fsize = fsize if fsize is not None else rcParams["axes.labelsize"]
    ytick_size = ytick_size if ytick_size is not None else rcParams["ytick.labelsize"]
    xtick_size = xtick_size if xtick_size is not None else rcParams["xtick.labelsize"]

    _apply_spine_style(ax)
    _apply_tick_style(ax)
    _apply_font_style(ax, fsize, xtick_size, ytick_size)


def _apply_spine_style(ax: plt.Axes) -> None:
    """Apply spine styling to axes."""
    linewidth = rcParams["axes.linewidth"]
    for spine in ax.spines.values():
        spine.set_linewidth(linewidth)


def _apply_tick_style(ax: plt.Axes) -> None:
    """Apply tick styling to axes."""
    # Apply x-tick styling
    ax.tick_params(
        axis="x",
        width=rcParams["xtick.major.width"],
        length=rcParams["xtick.major.size"],
        pad=rcParams["xtick.major.pad"],
    )
    # Apply y-tick styling
    ax.tick_params(
        axis="y",
        width=rcParams["ytick.major.width"],
        length=rcParams["ytick.major.size"],
        pad=rcParams["ytick.major.pad"],
    )


def _apply_font_style(
    ax: plt.Axes,
    fsize: int,
    xtick_size: int,
    ytick_size: int,
) -> None:
    """Apply font styling to axes labels and ticks."""
    font_family = rcParams["font.family"]

    ax.xaxis.label.set_fontsize(fsize)
    ax.yaxis.label.set_fontsize(fsize)
    ax.title.set_fontsize(fsize)

    ax.xaxis.label.set_fontname(font_family)
    ax.yaxis.label.set_fontname(font_family)
    ax.title.set_fontname(font_family)

    for label in ax.get_xticklabels():
        label.set_fontname(font_family)
        label.set_fontsize(xtick_size)

    for label in ax.get_yticklabels():
        label.set_fontname(font_family)
        label.set_fontsize(ytick_size)


def apply_style_to_figure(fig: plt.Figure) -> None:
    """
    Apply publication styling to all axes in a figure.

    Args:
        fig: The matplotlib Figure to style.
    """
    for ax in fig.get_axes():
        publication_style_ax(ax)

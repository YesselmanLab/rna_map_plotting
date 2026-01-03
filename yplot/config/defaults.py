"""
Default configuration values for yplot.

This module defines all default styling parameters used throughout the library.
These values can be overridden via rcParams or rc_context.
"""

from typing import Any

DEFAULT_PARAMS: dict[str, Any] = {
    # Font properties
    "font.family": "Arial Unicode MS",
    "font.size": 8,
    # Axes properties
    "axes.linewidth": 0.75,
    "axes.labelsize": 8,
    "axes.titlesize": 8,
    "axes.labelpad": 2,
    # X-tick properties
    "xtick.labelsize": 6,
    "xtick.major.width": 0.75,
    "xtick.major.size": 2.0,
    "xtick.major.pad": 1,
    # Y-tick properties
    "ytick.labelsize": 6,
    "ytick.major.width": 0.75,
    "ytick.major.size": 2.0,
    "ytick.major.pad": 1,
    # Line properties
    "lines.linewidth": 1.0,
    "lines.markersize": 6,
    # Scatter properties
    "scatter.marker_size": 20,
    # Lollipop properties
    "lollipop.marker_size": 40,
    "lollipop.line_width": 1.0,
    "lollipop.line_color": "black",
    # Legend properties
    "legend.fontsize": 8,
    "legend.frameon": False,
    "legend.handlelength": 1.0,
    "legend.handleheight": 0.5,
    "legend.handletextpad": 0.30,
    "legend.labelspacing": 0.15,
    # Subplot label properties
    "subplot.label_fontsize": 12,
    "subplot.label_left_offset": 0.0572,
    "subplot.label_top_offset": 0.02,
    # Corner text properties
    "corner_text.fontsize": 6,
    # Regression properties
    "regression.linewidth": 1.0,
    "regression.linestyle": "--",
    "regression.color": "black",
}


def get_default(key: str) -> Any:
    """
    Get a default configuration value.

    Args:
        key: The configuration key to retrieve.

    Returns:
        The default value for the key.

    Raises:
        KeyError: If the key is not found in defaults.
    """
    if key not in DEFAULT_PARAMS:
        raise KeyError(f"Unknown configuration key: {key}")
    return DEFAULT_PARAMS[key]


def list_keys() -> list:
    """
    List all available configuration keys.

    Returns:
        List of all configuration key names.
    """
    return list(DEFAULT_PARAMS.keys())

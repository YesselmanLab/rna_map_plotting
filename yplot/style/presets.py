"""
Style presets for common use cases.

This module provides predefined style configurations for different
output contexts like publications, presentations, and posters.
"""

from typing import Any

from yplot.config import rcParams

PRESETS: dict[str, dict[str, Any]] = {
    "publication": {
        "font.family": "Arial Unicode MS",
        "font.size": 8,
        "axes.linewidth": 0.75,
        "axes.labelsize": 8,
        "axes.titlesize": 8,
        "xtick.labelsize": 6,
        "ytick.labelsize": 6,
        "xtick.major.width": 0.75,
        "ytick.major.width": 0.75,
        "xtick.major.size": 2.0,
        "ytick.major.size": 2.0,
        "lines.linewidth": 1.0,
        "legend.fontsize": 8,
    },
    "presentation": {
        "font.family": "Arial Unicode MS",
        "font.size": 14,
        "axes.linewidth": 1.5,
        "axes.labelsize": 14,
        "axes.titlesize": 16,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "xtick.major.width": 1.5,
        "ytick.major.width": 1.5,
        "xtick.major.size": 4.0,
        "ytick.major.size": 4.0,
        "lines.linewidth": 2.0,
        "legend.fontsize": 12,
    },
    "poster": {
        "font.family": "Arial Unicode MS",
        "font.size": 18,
        "axes.linewidth": 2.0,
        "axes.labelsize": 18,
        "axes.titlesize": 20,
        "xtick.labelsize": 16,
        "ytick.labelsize": 16,
        "xtick.major.width": 2.0,
        "ytick.major.width": 2.0,
        "xtick.major.size": 5.0,
        "ytick.major.size": 5.0,
        "lines.linewidth": 2.5,
        "legend.fontsize": 16,
    },
}


def use(style: str) -> None:
    """
    Apply a predefined style preset.

    Args:
        style: Name of the preset ('publication', 'presentation', 'poster').

    Raises:
        ValueError: If style name is not recognized.

    Example:
        >>> import yplot
        >>> yplot.use('publication')
    """
    if style not in PRESETS:
        available = ", ".join(PRESETS.keys())
        raise ValueError(f"Unknown style '{style}'. Available: {available}")

    preset = PRESETS[style]
    rcParams.update_from_dict(preset)


def list_presets() -> list:
    """
    List available style presets.

    Returns:
        List of preset names.
    """
    return list(PRESETS.keys())


def get_preset(name: str) -> dict[str, Any]:
    """
    Get the configuration dictionary for a preset.

    Args:
        name: Name of the preset.

    Returns:
        Dictionary of configuration values.

    Raises:
        ValueError: If preset name is not recognized.
    """
    if name not in PRESETS:
        available = ", ".join(PRESETS.keys())
        raise ValueError(f"Unknown preset '{name}'. Available: {available}")
    return PRESETS[name].copy()

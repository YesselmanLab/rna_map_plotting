"""
Base classes and utilities for DataFrame-first plotting.

This module provides common functionality for extracting data from
DataFrames and handling the seaborn-like API pattern.
"""

from dataclasses import dataclass, field
from typing import Any, Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


@dataclass
class PlotData:
    """Container for extracted plot data with optional grouping."""

    x: np.ndarray
    y: np.ndarray
    color: Optional[np.ndarray] = None
    size: Optional[np.ndarray] = None
    error: Optional[np.ndarray] = None
    error_low: Optional[np.ndarray] = None
    error_high: Optional[np.ndarray] = None
    group: Optional[np.ndarray] = None
    labels: dict[str, list] = field(default_factory=dict)


def extract_data(
    data: Optional[pd.DataFrame],
    x: Optional[Union[str, np.ndarray]] = None,
    y: Optional[Union[str, np.ndarray]] = None,
    color: Optional[Union[str, np.ndarray]] = None,
    size: Optional[Union[str, np.ndarray]] = None,
    error: Optional[Union[str, np.ndarray]] = None,
    error_low: Optional[Union[str, np.ndarray]] = None,
    error_high: Optional[Union[str, np.ndarray]] = None,
    group: Optional[Union[str, np.ndarray]] = None,
) -> PlotData:
    """
    Extract plotting data from DataFrame or arrays.

    Args:
        data: DataFrame containing the data columns.
        x: Column name or array for x values.
        y: Column name or array for y values.
        color: Column name or array for color grouping.
        size: Column name or array for marker size.
        error: Column name or array for symmetric error bars.
        error_low: Column name or array for lower error bounds.
        error_high: Column name or array for upper error bounds.
        group: Column name or array for line/series grouping.

    Returns:
        PlotData object with extracted arrays and labels.
    """
    labels = {}

    x_arr = _extract_column(data, x, "x", labels)
    y_arr = _extract_column(data, y, "y", labels)
    color_arr = _extract_column(data, color, "color", labels)
    size_arr = _extract_column(data, size, "size", labels)
    error_arr = _extract_column(data, error, "error", labels)
    error_low_arr = _extract_column(data, error_low, "error_low", labels)
    error_high_arr = _extract_column(data, error_high, "error_high", labels)
    group_arr = _extract_column(data, group, "group", labels)

    return PlotData(
        x=x_arr,
        y=y_arr,
        color=color_arr,
        size=size_arr,
        error=error_arr,
        error_low=error_low_arr,
        error_high=error_high_arr,
        group=group_arr,
        labels=labels,
    )


def _extract_column(
    data: Optional[pd.DataFrame],
    col: Optional[Union[str, np.ndarray]],
    key: str,
    labels: dict,
) -> Optional[np.ndarray]:
    """Extract a single column from DataFrame or return array directly."""
    if col is None:
        return None
    if data is not None and isinstance(col, str):
        labels[key] = col
        return np.array(data[col])
    return np.array(col) if col is not None else None


def get_or_create_axes(ax: Optional[plt.Axes] = None) -> plt.Axes:
    """Get existing axes or create new ones."""
    if ax is None:
        _, ax = plt.subplots()
    return ax


def get_color_palette(n_colors: int) -> list[str]:
    """Get color palette from rcParams or matplotlib default."""
    cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    return [cycle[i % len(cycle)] for i in range(n_colors)]


def group_by_category(
    data: PlotData,
    category_col: str = "color",
) -> dict[Any, PlotData]:
    """
    Split PlotData by a categorical variable.

    Args:
        data: PlotData to split.
        category_col: Which field to group by ('color' or 'group').

    Returns:
        Dictionary mapping category values to PlotData subsets.
    """
    cat_arr = getattr(data, category_col)
    if cat_arr is None:
        return {None: data}

    unique_cats = np.unique(cat_arr)
    result = {}

    for cat in unique_cats:
        mask = cat_arr == cat
        result[cat] = PlotData(
            x=data.x[mask],
            y=data.y[mask],
            color=data.color[mask] if data.color is not None else None,
            size=data.size[mask] if data.size is not None else None,
            error=data.error[mask] if data.error is not None else None,
            error_low=data.error_low[mask] if data.error_low is not None else None,
            error_high=data.error_high[mask] if data.error_high is not None else None,
            group=data.group[mask] if data.group is not None else None,
            labels=data.labels,
        )

    return result


def apply_labels(ax: plt.Axes, data: PlotData) -> None:
    """Apply axis labels from PlotData labels dict."""
    if "x" in data.labels:
        ax.set_xlabel(data.labels["x"])
    if "y" in data.labels:
        ax.set_ylabel(data.labels["y"])

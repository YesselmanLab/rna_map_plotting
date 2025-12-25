"""
SubplotLayout class for row-based subplot configuration.

This module provides the main interface for defining and working
with subplot layouts using a simple row-based configuration format.
"""

from pathlib import Path
from typing import Any, Optional, Union

import yaml

from yplot.layout.coordinates import calculate_row_coordinates
from yplot.layout.utils import expand_coordinates

Coordinate = tuple[float, float, float, float]


class SubplotLayout:
    """
    Row-based subplot layout configuration.

    Supports configuration via dictionary or YAML file with row-based
    definitions for flexible subplot arrangements.

    Args:
        config: Configuration dictionary with fig_size and row definitions.
        yaml_file: Path to YAML configuration file.

    Example:
        >>> layout_dict = {
        ...     "fig_size": (7, 8.0),
        ...     "margins": {"left": 0.40, "right": 0.0, "top": 0.0, "bottom": 0.30},
        ...     "row_1": {
        ...         "size": (2.9, 2.5),
        ...         "spacing": {"hspace": 0.70, "wspace": 0.40},
        ...         "cols": 2,
        ...     },
        ... }
        >>> layout = SubplotLayout(config=layout_dict)
    """

    def __init__(
        self,
        config: Optional[dict[str, Any]] = None,
        yaml_file: Optional[Union[str, Path]] = None,
    ) -> None:
        """Initialize from configuration dictionary or YAML file."""
        config = self._load_config(config, yaml_file)
        self._validate_config(config)

        self.fig_size_inches: tuple[float, float] = tuple(config["fig_size"])
        self.subplot_info: dict[str, Any] = config
        self.rows: int = self._count_rows(config)
        self.margins: Optional[dict[str, float]] = config.get("margins")

    def _load_config(
        self,
        config: Optional[dict[str, Any]],
        yaml_file: Optional[Union[str, Path]],
    ) -> dict[str, Any]:
        """Load configuration from dict or YAML file."""
        if yaml_file is not None:
            yaml_path = Path(yaml_file)
            if not yaml_path.exists():
                raise FileNotFoundError(f"YAML file not found: {yaml_path}")
            with open(yaml_path) as f:
                return yaml.safe_load(f)

        if config is None:
            raise ValueError("Must provide either config or yaml_file")
        return config

    def _validate_config(self, config: dict[str, Any]) -> None:
        """Validate configuration has required fields."""
        if "fig_size" not in config:
            raise ValueError("Configuration must contain 'fig_size' key")
        if self._count_rows(config) == 0:
            raise ValueError("Configuration must contain at least one 'row_X' key")

    def _count_rows(self, config: dict[str, Any]) -> int:
        """Count number of row definitions in config."""
        return len([k for k in config.keys() if k.startswith("row_")])

    def get_coordinates(self) -> list[Coordinate]:
        """
        Calculate subplot coordinates based on configuration.

        Returns:
            List of (left, bottom, width, height) tuples in figure-relative
            units (0-1) for each subplot, ordered row by row.
        """
        rows = self._parse_rows()
        return calculate_row_coordinates(rows, self.fig_size_inches)

    def _parse_rows(self) -> list[dict[str, Any]]:
        """Parse row configurations into standardized format."""
        default_margins = self.margins or {
            "left": 0.0, "right": 0.0, "top": 0.0, "bottom": 0.0
        }
        row_keys = sorted(k for k in self.subplot_info.keys() if k.startswith("row_"))
        rows = []

        for row_key in row_keys:
            row_data = self.subplot_info[row_key]
            self._validate_row(row_key, row_data)
            rows.append(self._normalize_row(row_data, default_margins))

        return rows

    def _validate_row(self, row_key: str, row_data: dict[str, Any]) -> None:
        """Validate a row has required fields."""
        if "cols" not in row_data or "size" not in row_data:
            raise ValueError(f"{row_key} must contain 'cols' and 'size' fields")
        size = row_data["size"]
        if not isinstance(size, (tuple, list)) or len(size) != 2:
            raise ValueError(f"{row_key} 'size' must be (width, height)")

    def _normalize_row(
        self,
        row_data: dict[str, Any],
        default_margins: dict[str, float],
    ) -> dict[str, Any]:
        """Normalize row data to standard format."""
        spacing = row_data.get("spacing", {})
        if isinstance(spacing, dict):
            hspace = spacing.get("hspace", 0.3)
            wspace = spacing.get("wspace", 0.3)
        else:
            hspace = row_data.get("hspace", 0.3)
            wspace = row_data.get("wspace", 0.3)

        return {
            "cols": row_data["cols"],
            "width": row_data["size"][0],
            "height": row_data["size"][1],
            "hspace": hspace,
            "wspace": wspace,
            "margins": row_data.get("margins", default_margins),
        }

    def get_final_coordinates(self) -> list[Coordinate]:
        """
        Get coordinates with expansion applied for image subplots.

        Returns:
            List of (left, bottom, width, height) tuples with final coordinates.
        """
        coords = self.get_coordinates()
        return self._apply_image_expansion(coords)

    def _apply_image_expansion(self, coords: list[Coordinate]) -> list[Coordinate]:
        """Apply expansion to image subplot coordinates."""
        final_coords = []
        row_keys = sorted(k for k in self.subplot_info.keys() if k.startswith("row_"))
        coord_idx = 0

        for row_key in row_keys:
            row_data = self.subplot_info[row_key]
            num_cols = row_data.get("cols", 1)
            image_cols = self._get_image_columns(row_data, num_cols)

            for i in range(num_cols):
                if coord_idx >= len(coords):
                    break
                if image_cols[i]:
                    expanded = self._expand_image_coord(coords[coord_idx], row_data)
                    final_coords.append(expanded)
                else:
                    final_coords.append(coords[coord_idx])
                coord_idx += 1

        return final_coords

    def _get_image_columns(
        self, row_data: dict[str, Any], num_cols: int
    ) -> list[bool]:
        """Determine which columns are image subplots."""
        image_spec = row_data.get("image", False)
        if not image_spec:
            return [False] * num_cols
        return [i in image_spec for i in range(num_cols)]

    def _expand_image_coord(
        self, coord: Coordinate, row_data: dict[str, Any]
    ) -> Coordinate:
        """Expand a single image coordinate."""
        spacing = row_data.get("spacing", {"hspace": 0.5, "wspace": 0.5})
        margins = row_data.get("margins", self.margins)
        return expand_coordinates(
            coord,
            self.fig_size_inches,
            margins=margins,
            spacing=spacing,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to a dictionary."""
        return self.subplot_info

    def to_yaml(self, yaml_file: Union[str, Path]) -> None:
        """
        Save configuration to YAML file.

        Args:
            yaml_file: Path to save the YAML configuration.
        """
        yaml_path = Path(yaml_file)
        yaml_path.parent.mkdir(parents=True, exist_ok=True)
        with open(yaml_path, "w") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, indent=2)

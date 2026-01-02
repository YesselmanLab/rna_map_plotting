"""
SubplotLayout class for row-based subplot configuration.

This module provides the main interface for defining and working
with subplot layouts using a simple row-based configuration format.
"""

import warnings
from pathlib import Path
from typing import Any, Optional, Union

import re

import yaml

# Valid keys at the top level of the config
VALID_TOP_LEVEL_KEYS = {"fig_size", "margins"}

# Valid keys within a row definition
VALID_ROW_KEYS = {"cols", "size", "spacing", "margins", "image", "hspace", "wspace"}

from yplot.layout.coordinates import calculate_row_coordinates
from yplot.layout.utils import expand_coordinates

Coordinate = tuple[float, float, float, float]

# Pattern to match range syntax: rows_1-10, row_1-5, rows_3:7
RANGE_PATTERN = re.compile(r'^rows?_(\d+)[-:](\d+)$')


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
                loaded = yaml.safe_load(f)
                return self._expand_range_keys(loaded)

        if config is None:
            raise ValueError("Must provide either config or yaml_file")
        return self._expand_range_keys(config)

    def _expand_range_keys(self, config: dict[str, Any]) -> dict[str, Any]:
        """
        Expand range syntax keys into individual row keys.

        Supports patterns like:
        - rows_1-10: expands to row_1 through row_10
        - row_1-5: expands to row_1 through row_5
        - rows_3:7: expands to row_3 through row_7

        Args:
            config: Configuration dictionary that may contain range keys.

        Returns:
            Configuration with range keys expanded to individual row_X keys.
        """
        expanded = {}
        # Track which range keys produced which row keys for error messages
        row_sources: dict[str, str] = {}

        for key, value in config.items():
            match = RANGE_PATTERN.match(key)
            if match:
                start, end = int(match.group(1)), int(match.group(2))
                if start > end:
                    raise ValueError(
                        f"Invalid range '{key}': start ({start}) > end ({end})"
                    )
                for i in range(start, end + 1):
                    row_key = f"row_{i}"
                    if row_key in expanded:
                        source = row_sources.get(row_key, row_key)
                        raise ValueError(
                            f"Duplicate row definition: '{row_key}' "
                            f"(from '{key}' conflicts with '{source}')"
                        )
                    # Deep copy the value to avoid shared references
                    expanded[row_key] = dict(value) if isinstance(value, dict) else value
                    row_sources[row_key] = key
            else:
                # Check if this is a row_X key that conflicts with an expanded range
                if key.startswith("row_") and key in expanded:
                    source = row_sources.get(key, key)
                    raise ValueError(
                        f"Duplicate row definition: '{key}' "
                        f"(conflicts with range '{source}')"
                    )
                expanded[key] = value
                if key.startswith("row_"):
                    row_sources[key] = key
        return expanded

    def _validate_config(self, config: dict[str, Any]) -> None:
        """Validate configuration has required fields."""
        if "fig_size" not in config:
            raise ValueError("Configuration must contain 'fig_size' key")
        if self._count_rows(config) == 0:
            raise ValueError("Configuration must contain at least one 'row_X' key")
        self._warn_unknown_keys(config)

    def _warn_unknown_keys(self, config: dict[str, Any]) -> None:
        """Warn about unrecognized keys in the configuration."""
        # Check top-level keys
        for key in config.keys():
            if key.startswith("row_"):
                # Validate row-level keys
                row_data = config[key]
                if isinstance(row_data, dict):
                    self._warn_unknown_row_keys(key, row_data)
            elif key not in VALID_TOP_LEVEL_KEYS:
                suggestion = self._suggest_key(key, VALID_TOP_LEVEL_KEYS)
                msg = f"Unknown config key '{key}' will be ignored"
                if suggestion:
                    msg += f". Did you mean '{suggestion}'?"
                warnings.warn(msg, UserWarning, stacklevel=4)

    def _warn_unknown_row_keys(self, row_key: str, row_data: dict[str, Any]) -> None:
        """Warn about unrecognized keys in a row definition."""
        for key in row_data.keys():
            if key not in VALID_ROW_KEYS:
                suggestion = self._suggest_key(key, VALID_ROW_KEYS)
                msg = f"Unknown key '{key}' in {row_key} will be ignored"
                if suggestion:
                    msg += f". Did you mean '{suggestion}'?"
                warnings.warn(msg, UserWarning, stacklevel=5)

    def _suggest_key(self, key: str, valid_keys: set[str]) -> Optional[str]:
        """Suggest a valid key based on similarity to the provided key."""
        key_lower = key.lower()
        for valid in valid_keys:
            # Check for common typos: missing 's', extra 's', similar spelling
            if (
                key_lower == valid.rstrip("s")  # margin -> margins
                or key_lower == valid + "s"  # spacings -> spacing
                or key_lower in valid  # col -> cols
                or valid in key_lower  # columns -> cols
            ):
                return valid
        return None

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

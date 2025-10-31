"""
Streamlined subplot layout configuration system.

This module provides a clean, focused interface for creating subplot layouts
using row-based configurations.
"""

import yaml
from pathlib import Path
from typing import Union, Dict, List, Tuple, Optional
import warnings


class SubplotLayout:
    """
    Streamlined subplot layout configuration class.

    Supports row-based configuration with dictionary format.

    Parameters:
    -----------
    config : dict
        Configuration dictionary with fig_size and row definitions.

    Examples:
    ---------
    # Row-based configuration
    layout_dict = {
        "fig_size": (7, 8.0),
        "row_1": {
            "size": (2.9, 2.5),
            "spacing": {"hspace": 0.70, "wspace": 0.40},
            "margins": {"left": 0.40, "right": 0.0, "top": 0.0, "bottom": 0.30},
            "cols": 2,
            "image": [0, 1],
        },
        "row_2": {
            "size": (2.9, 1.2),
            "spacing": {"hspace": 0.70, "wspace": 0.40},
            "margins": {"left": 0.40, "right": 0.0, "top": 0.0, "bottom": 0.30},
            "cols": 2,
        },
    }
    layout = SubplotLayout(config=layout_dict)
    """

    def __init__(
        self,
        config: Optional[Dict] = None,
        yaml_file: Optional[Union[str, Path]] = None,
    ):
        """Initialize from configuration dictionary or YAML file."""
        if yaml_file is not None:
            yaml_path = Path(yaml_file)
            if not yaml_path.exists():
                raise FileNotFoundError(f"YAML file not found: {yaml_path}")
            with open(yaml_path, "r") as f:
                config = yaml.safe_load(f)

        if config is None:
            raise ValueError("Must provide either config or yaml_file")

        # Validate fig_size
        if "fig_size" not in config:
            raise ValueError("Configuration must contain 'fig_size' key")

        self.fig_size_inches = tuple(config["fig_size"])
        self.subplot_info = config
        self.rows = len([k for k in config.keys() if k.startswith("row_")])

        if self.rows == 0:
            raise ValueError("Configuration must contain at least one 'row_X' key")

    def get_coordinates(self) -> List[Tuple[float, float, float, float]]:
        """
        Calculate subplot coordinates based on the configuration.

        Returns:
        --------
        list
            List of tuples, each containing (left, bottom, width, height) coordinates
            in figure-relative units (0-1) for each subplot, ordered row by row.
        """
        return self._calculate_row_based_coordinates()

    def _calculate_row_based_coordinates(
        self,
    ) -> List[Tuple[float, float, float, float]]:
        """Calculate coordinates using row-based configuration."""
        fig_width, fig_height = self.fig_size_inches

        # Parse row information
        rows = []
        row_keys = sorted([k for k in self.subplot_info.keys() if k.startswith("row_")])

        if not row_keys:
            raise ValueError("subplot_info must contain at least one 'row_X' key")

        for row_key in row_keys:
            row_data = self.subplot_info[row_key]

            # Validate required fields
            if "cols" not in row_data or "size" not in row_data:
                raise ValueError(f"{row_key} must contain 'cols' and 'size' fields")

            # Extract row information
            cols = row_data["cols"]
            size = row_data["size"]

            # Handle spacing - can be dict or individual values
            spacing = row_data.get("spacing", {})
            if isinstance(spacing, dict):
                hspace = spacing.get("hspace", 0.3)
                wspace = spacing.get("wspace", 0.3)
            else:
                # Backward compatibility
                hspace = row_data.get("hspace", 0.3)
                wspace = row_data.get("wspace", 0.3)

            margins = row_data.get(
                "margins", {"left": 0.00, "right": 0.00, "top": 0.00, "bottom": 0.00}
            )

            if not isinstance(size, (tuple, list)) or len(size) != 2:
                raise ValueError(
                    f"{row_key} 'size' must be a tuple/list of (width, height)"
                )

            rows.append(
                {
                    "cols": cols,
                    "width": size[0],
                    "height": size[1],
                    "hspace": hspace,
                    "wspace": wspace,
                    "margins": margins,
                }
            )

        # Calculate total space needed
        total_height = sum(row["height"] for row in rows)
        total_wspace = sum(
            row["wspace"] for row in rows[:-1]
        )  # No wspace after last row
        total_margins_height = rows[0]["margins"]["top"] + rows[-1]["margins"]["bottom"]

        required_height = total_height + total_wspace + total_margins_height

        # Warn if layout doesn't fit
        if required_height > fig_height:
            warnings.warn(
                f"Subplot layout requires {required_height:.2f} inches height "
                f"but figure is {fig_height:.2f} inches. Subplots may overlap."
            )

        # Calculate coordinates
        coordinates = []

        # Calculate cumulative positions for rows (from bottom to top)
        row_bottoms = []
        current_bottom = rows[-1]["margins"]["bottom"]  # Start from bottom row margin

        for row_idx in range(len(rows) - 1, -1, -1):  # Start from bottom row
            row_bottoms.insert(0, current_bottom)  # Insert at beginning
            current_bottom += rows[row_idx]["height"]
            if row_idx > 0:  # Add spacing if not the top row
                current_bottom += rows[row_idx - 1]["wspace"]

        # Generate coordinates for each subplot
        for row_idx, row in enumerate(rows):
            num_cols_in_row = row["cols"]
            row_height = row["height"]
            subplot_width = row["width"]
            hspace = row["hspace"]

            # Calculate column positions for this row
            col_lefts = []
            current_left = row["margins"]["left"]

            for col in range(num_cols_in_row):
                col_lefts.append(current_left)
                current_left += subplot_width
                if col < num_cols_in_row - 1:  # Add spacing if not the last column
                    current_left += hspace

            # Generate coordinates for subplots in this row
            for col in range(num_cols_in_row):
                left_inches = col_lefts[col]
                bottom_inches = row_bottoms[row_idx]
                width_inches = subplot_width
                height_inches = row_height

                # Convert to figure-relative coordinates (0-1)
                left_rel = left_inches / fig_width
                bottom_rel = bottom_inches / fig_height
                width_rel = width_inches / fig_width
                height_rel = height_inches / fig_height

                coordinates.append((left_rel, bottom_rel, width_rel, height_rel))

        return coordinates

    def get_final_coordinates(self) -> List[Tuple[float, float, float, float]]:
        """
        Get coordinates with expansion applied for image subplots.

        Returns:
        --------
        list
            List of tuples with final coordinates (left, bottom, width, height).
        """
        from yplot.layout_utils import expand_subplot_coordinates

        coords = self.get_coordinates()
        final_coords = []

        row_keys = sorted([k for k in self.subplot_info.keys() if k.startswith("row_")])
        coord_idx = 0

        for row_key in row_keys:
            row_data = self.subplot_info[row_key]
            image_flag = row_data.get("image", False)
            num_cols = row_data.get("cols", 1)

            # Handle different image flag formats
            if isinstance(image_flag, bool):
                # Boolean: all columns in row are images
                is_image_list = [image_flag] * num_cols
            elif isinstance(image_flag, list):
                # List: specific columns are images
                is_image_list = [i in image_flag for i in range(num_cols)]
            else:
                # Default: no images
                is_image_list = [False] * num_cols

            for i in range(num_cols):
                if is_image_list[i] and coord_idx < len(coords):
                    # Expand this coordinate
                    # Get spacing from the row data
                    spacing = row_data.get("spacing", {})
                    if isinstance(spacing, dict):
                        hspace = spacing.get("hspace", 0.5)
                        wspace = spacing.get("wspace", 0.5)
                    else:
                        hspace = row_data.get("hspace", 0.5)
                        wspace = row_data.get("wspace", 0.5)

                    expanded = expand_subplot_coordinates(
                        coords[coord_idx],
                        self.fig_size_inches,
                        margins=row_data.get("margins"),
                        spacing={"hspace": hspace, "wspace": wspace},
                    )
                    final_coords.append(expanded)
                else:
                    final_coords.append(coords[coord_idx])
                coord_idx += 1

        return final_coords

    def to_dict(self) -> Dict:
        """Convert configuration to a dictionary."""
        return self.subplot_info

    def to_yaml(self, yaml_file: Union[str, Path]):
        """Save configuration to YAML file."""
        yaml_path = Path(yaml_file)
        yaml_path.parent.mkdir(parents=True, exist_ok=True)

        with open(yaml_path, "w") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, indent=2)

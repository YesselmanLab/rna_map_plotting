"""
Streamlined subplot layout configuration system.

This module provides a clean, focused interface for creating subplot layouts
with support for both standard grid layouts and row-based configurations.
"""

import yaml
from pathlib import Path
from typing import Union, Dict, List, Tuple, Optional
import warnings


class SubplotLayout:
    """
    Streamlined subplot layout configuration class.

    Supports two configuration formats:
    1. Standard grid: fig_size, rows, cols, row_heights, col_widths, etc.
    2. Row-based: fig_size + row_1, row_2, etc. (for complex layouts)

    Parameters:
    -----------
    config : dict, optional
        Configuration dictionary. Can use either standard or row-based format.
    fig_size_inches : tuple, optional
        Figure size as (width, height) in inches (for direct initialization)
    rows : int, optional
        Number of rows in the subplot grid (for direct initialization)
    cols : int, optional
        Number of columns in the subplot grid (for direct initialization)
    **kwargs
        Additional parameters for direct initialization

    Examples:
    ---------
    # Row-based configuration (preferred for complex layouts)
    layout_dict = {
        "fig_size": (7, 2),
        "row_1": {
            "size": (1.3, 1.3),
            "hspace": 0.45,
            "wspace": 0.50,
            "margins": {"left": 0.40, "right": 0.0, "top": 0.0, "bottom": 0.50},
            "cols": 4
        }
    }
    layout = SubplotLayout(config=layout_dict)

    # Standard grid configuration
    layout = SubplotLayout(
        fig_size_inches=(10, 8),
        rows=2,
        cols=3,
        row_heights=[3.0, 2.0],
        col_widths=[2.5, 2.5, 2.5]
    )
    """

    def __init__(
        self,
        config: Optional[Dict] = None,
        fig_size_inches: Optional[Tuple[float, float]] = None,
        rows: Optional[int] = None,
        cols: Optional[int] = None,
        **kwargs,
    ):
        # Initialize with defaults
        self.fig_size_inches = None
        self.rows = None
        self.cols = None
        self.row_heights = []
        self.col_widths = []
        self.wspace = []
        self.hspace = []
        self.margins = {"left": 0.75, "right": 0.75, "top": 0.75, "bottom": 0.75}
        self.subplot_info = None
        self.is_row_based = False

        # Handle different initialization methods
        if config is not None:
            self._load_from_config(config)
        elif fig_size_inches is not None and rows is not None and cols is not None:
            self._load_from_parameters(fig_size_inches, rows, cols, **kwargs)
        else:
            raise ValueError(
                "Must provide either config dict or fig_size_inches+rows+cols"
            )

    def _load_from_config(self, config: Dict):
        """Load configuration from dictionary."""
        # Check if this is a row-based configuration
        row_keys = [k for k in config.keys() if k.startswith("row_")]
        has_traditional_keys = "rows" in config or "cols" in config

        if row_keys and not has_traditional_keys:
            # Row-based configuration
            self.is_row_based = True
            self.fig_size_inches = tuple(
                config.get("fig_size", config.get("fig_size_inches", (7, 4)))
            )
            self.subplot_info = config
            self.rows = len(row_keys)
            self.cols = None  # Will be determined from row configs
            self.margins = config.get(
                "margins", {"left": 0.00, "right": 0.00, "top": 0.00, "bottom": 0.00}
            )
            return

        # Standard configuration
        self.is_row_based = False
        if "fig_size" in config:
            self.fig_size_inches = tuple(config["fig_size"])
        elif "fig_size_inches" in config:
            self.fig_size_inches = tuple(config["fig_size_inches"])
        else:
            raise ValueError(
                "Configuration must contain 'fig_size' or 'fig_size_inches'"
            )

        self.rows = config.get("rows", 1)
        self.cols = config.get("cols", 1)

        # Set default values
        self.row_heights = config.get("row_heights", [2.0] * self.rows)
        self.col_widths = config.get("col_widths", [2.0] * self.cols)
        self.wspace = config.get(
            "wspace", [0.5] * (self.rows - 1) if self.rows > 1 else []
        )
        self.hspace = config.get(
            "hspace", [0.5] * (self.cols - 1) if self.cols > 1 else []
        )
        self.margins = config.get("margins", self.margins)

    def _load_from_parameters(
        self, fig_size_inches: Tuple[float, float], rows: int, cols: int, **kwargs
    ):
        """Load configuration from direct parameters."""
        self.is_row_based = False
        self.fig_size_inches = tuple(fig_size_inches)
        self.rows = rows
        self.cols = cols

        # Set row heights
        row_heights = kwargs.get("row_heights")
        if row_heights is not None:
            if len(row_heights) != rows:
                raise ValueError(
                    f"row_heights must have {rows} elements, got {len(row_heights)}"
                )
            self.row_heights = row_heights
        else:
            self.row_heights = [2.0] * rows

        # Set column widths
        col_widths = kwargs.get("col_widths")
        if col_widths is not None:
            if len(col_widths) != cols:
                raise ValueError(
                    f"col_widths must have {cols} elements, got {len(col_widths)}"
                )
            self.col_widths = col_widths
        else:
            self.col_widths = [2.0] * cols

        # Set vertical spacing (between rows)
        wspace = kwargs.get("wspace")
        if wspace is not None:
            if rows > 1 and len(wspace) != rows - 1:
                raise ValueError(
                    f"wspace must have {rows - 1} elements, got {len(wspace)}"
                )
            self.wspace = wspace
        else:
            self.wspace = [0.5] * (rows - 1) if rows > 1 else []

        # Set horizontal spacing (between columns)
        hspace = kwargs.get("hspace")
        if hspace is not None:
            if cols > 1 and len(hspace) != cols - 1:
                raise ValueError(
                    f"hspace must have {cols - 1} elements, got {len(hspace)}"
                )
            self.hspace = hspace
        else:
            self.hspace = [0.5] * (cols - 1) if cols > 1 else []

        # Set margins
        margins = kwargs.get("margins")
        if margins is not None:
            self.margins = margins

    def get_coordinates(
        self, cols_per_row: Optional[List[int]] = None
    ) -> List[Tuple[float, float, float, float]]:
        """
        Calculate subplot coordinates based on the configuration.

        Parameters:
        -----------
        cols_per_row : list, optional
            Number of columns in each row. If None, uses uniform grid.
            If provided, allows different numbers of subplots per row.

        Returns:
        --------
        list
            List of tuples, each containing (left, bottom, width, height) coordinates
            in figure-relative units (0-1) for each subplot, ordered row by row.
        """
        if self.is_row_based:
            return self._calculate_row_based_coordinates()
        else:
            return self._calculate_standard_coordinates(cols_per_row)

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

    def _calculate_standard_coordinates(
        self, cols_per_row: Optional[List[int]] = None
    ) -> List[Tuple[float, float, float, float]]:
        """Calculate coordinates using standard grid configuration."""
        fig_width, fig_height = self.fig_size_inches

        # Use uniform grid if cols_per_row not provided
        if cols_per_row is None:
            cols_per_row = [self.cols] * self.rows

        # Validate list lengths
        if len(self.row_heights) != self.rows:
            raise ValueError(
                f"row_heights must have {self.rows} elements, got {len(self.row_heights)}"
            )
        if len(cols_per_row) != self.rows:
            raise ValueError(
                f"cols_per_row must have {self.rows} elements, got {len(cols_per_row)}"
            )
        if self.rows > 1 and len(self.wspace) != self.rows - 1:
            raise ValueError(
                f"wspace must have {self.rows - 1} elements, got {len(self.wspace)}"
            )

        # Calculate total space needed
        total_subplot_height = sum(self.row_heights)
        total_wspace = sum(self.wspace)
        total_margins_height = self.margins["top"] + self.margins["bottom"]

        # For width calculation, we need to consider the maximum number of columns
        max_cols = max(cols_per_row)
        if len(self.col_widths) != max_cols:
            raise ValueError(
                f"col_widths must have {max_cols} elements, got {len(self.col_widths)}"
            )

        # Calculate total width needed (using max columns for validation)
        total_subplot_width = sum(self.col_widths)
        total_hspace = sum(self.hspace) if len(self.hspace) > 0 else 0
        total_margins_width = self.margins["left"] + self.margins["right"]

        required_width = total_subplot_width + total_hspace + total_margins_width
        required_height = total_subplot_height + total_wspace + total_margins_height

        # Warn if layout doesn't fit
        if required_width > fig_width or required_height > fig_height:
            warnings.warn(
                f"Subplot layout requires {required_width:.2f}x{required_height:.2f} inches "
                f"but figure is {fig_width:.2f}x{fig_height:.2f} inches. Subplots may overlap."
            )

        # Calculate coordinates
        coordinates = []

        # Calculate cumulative positions for rows (from bottom to top)
        row_bottoms = []
        current_bottom = self.margins["bottom"]
        for row in range(self.rows - 1, -1, -1):  # Start from bottom row
            row_bottoms.insert(0, current_bottom)  # Insert at beginning
            current_bottom += self.row_heights[row]
            if row > 0:  # Add spacing if not the top row
                current_bottom += self.wspace[row - 1]

        # Generate coordinates for each subplot
        for row in range(self.rows):
            num_cols_in_row = cols_per_row[row]

            # Calculate column positions for this row
            col_lefts = []
            current_left = self.margins["left"]
            for col in range(num_cols_in_row):
                col_lefts.append(current_left)
                current_left += self.col_widths[col]
                if col < num_cols_in_row - 1:  # Add spacing if not the last column
                    current_left += self.hspace[col] if col < len(self.hspace) else 0

            # Generate coordinates for subplots in this row
            for col in range(num_cols_in_row):
                left_inches = col_lefts[col]
                bottom_inches = row_bottoms[row]
                width_inches = self.col_widths[col]
                height_inches = self.row_heights[row]

                # Convert to figure-relative coordinates (0-1)
                left_rel = left_inches / fig_width
                bottom_rel = bottom_inches / fig_height
                width_rel = width_inches / fig_width
                height_rel = height_inches / fig_height

                coordinates.append((left_rel, bottom_rel, width_rel, height_rel))

        return coordinates

    def to_dict(self) -> Dict:
        """Convert configuration to a dictionary."""
        if self.is_row_based:
            return self.subplot_info
        else:
            return {
                "fig_size": list(self.fig_size_inches),
                "rows": self.rows,
                "cols": self.cols,
                "row_heights": self.row_heights,
                "col_widths": self.col_widths,
                "wspace": self.wspace,
                "hspace": self.hspace,
                "margins": self.margins,
            }

    def to_yaml(self, yaml_file: Union[str, Path]):
        """Save configuration to YAML file."""
        yaml_path = Path(yaml_file)
        yaml_path.parent.mkdir(parents=True, exist_ok=True)

        with open(yaml_path, "w") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, indent=2)

    @classmethod
    def from_yaml(cls, yaml_file: Union[str, Path]):
        """Load configuration from YAML file."""
        yaml_path = Path(yaml_file)
        if not yaml_path.exists():
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")

        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)

        return cls(config=config)


# Convenience function for backward compatibility
def calculate_subplot_coordinates(
    layout: SubplotLayout, cols_per_row: Optional[List[int]] = None
) -> List[Tuple[float, float, float, float]]:
    """
    Calculate subplot coordinates from a SubplotLayout configuration.

    This is a convenience wrapper function that calls the get_coordinates method
    on a SubplotLayout object.

    Parameters:
    -----------
    layout : SubplotLayout
        SubplotLayout object containing the configuration
    cols_per_row : list, optional
        Number of columns in each row. If None, uses uniform grid.
        If provided, allows different numbers of subplots per row.

    Returns:
    --------
    list
        List of tuples, each containing (left, bottom, width, height) coordinates
        in figure-relative units (0-1) for each subplot, ordered row by row.
    """
    return layout.get_coordinates(cols_per_row)


# Convenience function for backward compatibility
def generate_subplot_coordinates_from_dict(
    config: Dict,
) -> List[Tuple[float, float, float, float]]:
    """
    Generate subplot coordinates from a dictionary configuration.

    This function provides a clean interface for generating subplot coordinates
    directly from a dictionary without needing to create a SubplotLayout object.

    Parameters:
    -----------
    config : dict
        Configuration dictionary. Can use either the row-based format (row_1, row_2, etc.)
        or the standard format with rows, cols, etc.

    Returns:
    --------
    list
        List of tuples, each containing (left, bottom, width, height) coordinates
        in figure-relative units (0-1) for each subplot
    """
    layout = SubplotLayout(config=config)
    return layout.get_coordinates()

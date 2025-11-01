"""
Streamlined subplot layout configuration system.

This module provides a clean, focused interface for creating subplot layouts
using row-based configurations.
"""

import os
import yaml
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path
from typing import Union, Dict, List, Tuple, Optional
import warnings

from yplot.layout_utils import expand_subplot_coordinates
from yplot.style import publication_style_ax


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
    # Row-based configuration with top-level margins
    layout_dict = {
        "fig_size": (7, 8.0),
        "margins": {"left": 0.40, "right": 0.0, "top": 0.0, "bottom": 0.30},
        "row_1": {
            "size": (2.9, 2.5),
            "spacing": {"hspace": 0.70, "wspace": 0.40},
            "cols": 2,
            "image": [0, 1],
        },
        "row_2": {
            "size": (2.9, 1.2),
            "spacing": {"hspace": 0.70, "wspace": 0.40},
            "cols": 2,
        },
    }
    layout = SubplotLayout(config=layout_dict)

    # Row-specific margins override top-level margins
    layout_dict = {
        "fig_size": (7, 8.0),
        "margins": {"left": 0.40, "right": 0.0, "top": 0.0, "bottom": 0.30},
        "row_1": {
            "size": (2.9, 2.5),
            "spacing": {"hspace": 0.70, "wspace": 0.40},
            "margins": {"left": 0.40, "right": 0.0, "top": 0.0, "bottom": 0.30},
            "cols": 2,
        },
        "row_2": {
            "size": (2.9, 1.2),
            "spacing": {"hspace": 0.70, "wspace": 0.40},
            "cols": 2,  # Uses top-level margins
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

        # Parse top-level margins if provided
        self.margins = config.get("margins", None)

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

        # Default margins to use if not specified at row level
        default_margins = (
            self.margins
            if self.margins is not None
            else {"left": 0.00, "right": 0.00, "top": 0.00, "bottom": 0.00}
        )

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

            # Use row-specific margins if provided, otherwise use default margins
            margins = row_data.get("margins", default_margins)

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

        coords = self.get_coordinates()
        final_coords = []

        row_keys = sorted([k for k in self.subplot_info.keys() if k.startswith("row_")])
        coord_idx = 0

        for row_key in row_keys:
            row_data = self.subplot_info[row_key]
            num_cols = row_data.get("cols", 1)
            if row_data.get("image", False):
                # List: specific columns are images
                is_image_list = [
                    i in row_data.get("image", []) for i in range(num_cols)
                ]
            else:
                # Default: no images
                is_image_list = [False] * num_cols

            for i in range(num_cols):
                if is_image_list[i] and coord_idx < len(coords):
                    # Expand this coordinate
                    # Handle spacing - can be dict or individual values, with defaults
                    spacing = row_data.get("spacing")
                    if spacing is None:
                        # Default spacing if not specified
                        spacing = {"hspace": 0.5, "wspace": 0.5}

                    # Use row-specific margins if provided, otherwise use top-level margins
                    margins = row_data.get("margins", self.margins)

                    expanded = expand_subplot_coordinates(
                        coords[coord_idx],
                        self.fig_size_inches,
                        margins=margins,
                        spacing=spacing,
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


def load_and_fit_image_to_subplot(image_path, ax):
    """
    Load an image from file and stretch it to fit in a subplot.

    Parameters:
    -----------
    image_path : str
        Path to the image file
    subplot_coords : tuple
        Subplot coordinates as (left, bottom, width, height) in figure-relative units
    fig : matplotlib.figure.Figure
        The figure object
    ax : matplotlib.axes.Axes
        The axes object where the image will be placed

    Returns:
    --------
    matplotlib.image.AxesImage
        The image object that was added to the subplot
    """

    # Load the image
    try:
        img = mpimg.imread(image_path)
    except Exception as e:
        raise ValueError(f"Could not load image from {image_path}: {e}")

    # Clear the axes
    ax.clear()

    # Display the image stretched to fit the subplot
    img_plot = ax.imshow(img)

    # Remove axes ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Remove spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    return img_plot


def render_example_figure(layout):
    """
    Render an example figure with subplot coordinates.

    This function creates a matplotlib figure with the given coordinates but does not save it.
    Use this when you want to display the figure or save it manually.

    Parameters:
    -----------
    layout : SubplotLayout
        A SubplotLayout object containing the figure configuration

    Returns:
    --------
    matplotlib.figure.Figure
        The rendered figure object

    Examples:
    ---------
    # Render a figure
    layout = SubplotLayout(config={...})
    fig = render_example_figure(layout)

    # Display the figure
    plt.show()

    # Or save it manually
    fig.savefig('my_figure.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    """

    # Ensure layout is a SubplotLayout object
    if not isinstance(layout, SubplotLayout):
        raise ValueError("layout must be a SubplotLayout object")

    coords = layout.get_final_coordinates()
    fig_size_inches = layout.fig_size_inches

    fig = plt.figure(figsize=fig_size_inches, dpi=100)

    # Color palette for different subplot sizes or sections
    colors = [
        "#ffcccc",
        "#ccffcc",
        "#ccccff",
        "#ffffcc",
        "#ffccff",
        "#ccffff",
        "#ffdddd",
        "#ddffdd",
    ]

    # Track which subplots are images by building a list
    is_image_list = []
    row_keys = sorted([k for k in layout.subplot_info.keys() if k.startswith("row_")])

    for row_key in row_keys:
        row_data = layout.subplot_info[row_key]
        num_cols = row_data.get("cols", 1)
        if row_data.get("image", False):
            # List: specific columns are images
            row_image_list = [i in row_data.get("image", []) for i in range(num_cols)]
        else:
            # Default: no images
            row_image_list = [False] * num_cols
        is_image_list.extend(row_image_list)

    for idx, (left, bottom, width, height) in enumerate(coords):
        ax = fig.add_axes([left, bottom, width, height])

        # Set background color based on index
        color_idx = idx % len(colors)
        ax.set_facecolor(colors[color_idx])

        # Check if this is an image subplot
        is_image = is_image_list[idx] if idx < len(is_image_list) else False

        if is_image:
            # For image subplots, don't show axes
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            for spine in ax.spines.values():
                spine.set_visible(False)
            # Just show the subplot number
            ax.text(
                0.5,
                0.5,
                f"Image {idx}",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
            )
        else:
            # For regular subplots, add text showing subplot info and axes
            ax.text(
                0.5,
                0.5,
                f"Subplot {idx}",
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
            )

            # Add a subtle border
            for spine in ax.spines.values():
                spine.set_edgecolor("black")
                spine.set_linewidth(0.5)

            ax.set_xlabel("X Label", labelpad=2)
            ax.set_ylabel("Y Label", labelpad=2)
            publication_style_ax(ax)

    return fig


def save_example_figure(
    fig, title, filename, output_dir="docs/figures", dpi=150, bbox_inches="tight"
):
    """
    Save an example figure to a file.

    This function saves a matplotlib figure to a file with optional title and formatting.

    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The figure object to save
    title : str
        Title for the figure (will be added as suptitle)
    filename : str
        Filename to save the figure
    output_dir : str, optional
        Directory to save the figure in (default: 'docs/figures')
    dpi : int, optional
        DPI for the saved figure (default: 150)
    bbox_inches : str, optional
        Bbox_inches parameter for saving (default: 'tight')

    Returns:
    --------
    str
        Path to the saved figure file

    Examples:
    ---------
    # Save a figure
    fig = render_example_figure(coords, (7, 5))
    filepath = save_example_figure(fig, "My Layout", "example.png")
    plt.close(fig)

    # Save with custom directory and DPI
    filepath = save_example_figure(
        fig,
        "My Layout",
        "example.png",
        output_dir='my_figures',
        dpi=300
    )
    """
    # Add title to figure
    fig.suptitle(title, fontsize=14, fontweight="bold", y=0.95)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    # Save the figure
    fig.savefig(filepath, dpi=dpi, bbox_inches=bbox_inches)

    print(f"✓ Saved: {filepath}")
    return filepath


def create_example_figure(
    layout,
    title,
    filename,
    output_dir="docs/figures",
):
    """
    Create and save an example figure with subplot coordinates.

    This is a convenience function that combines render_example_figure and save_example_figure.
    Use this for quick figure creation and saving.

    Parameters:
    -----------
    layout : SubplotLayout
        A SubplotLayout object containing the figure configuration
    title : str
        Title for the figure
    filename : str
        Filename to save the figure
    output_dir : str, optional
        Directory to save the figure in (default: 'docs/figures')

    Returns:
    --------
    str
        Path to the saved figure file

    Examples:
    ---------
    # Create and save a simple example figure
    layout = SubplotLayout(config={...})
    filepath = create_example_figure(
        layout,
        "My Layout",
        "example.png"
    )
    """
    # Render the figure
    fig = render_example_figure(layout)

    # Save the figure
    filepath = save_example_figure(fig, title, filename, output_dir)

    # Close the figure to free memory
    plt.close(fig)

    return filepath

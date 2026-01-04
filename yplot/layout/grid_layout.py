"""
Grid-based subplot layout with spanning support.

This module provides a subplot2grid-like interface with exact inch specifications
for cell sizes and gaps between subplots.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Optional, Union

import yaml


class AxisType(Enum):
    """Axis behavior type for grid cells."""

    PLOT = auto()  # Standard axes with ticks/spines
    IMAGE = auto()  # Bare axes for images (no ticks/spines)


DEFAULT_MARGINS = {"left": 0.5, "right": 0.1, "top": 0.1, "bottom": 0.4}


def create_grid(
    rows: int,
    cols: int,
    cell_width: float = 2.5,
    cell_height: float = 2.0,
    hgap: float = 0.3,
    vgap: float = 0.4,
    left: float = 0.5,
    right: float = 0.1,
    top: float = 0.1,
    bottom: float = 0.4,
) -> "GridLayout":
    """
    Create a filled uniform grid layout in one step.

    This is a convenience function that creates a GridSpec and GridLayout
    with all cells filled. For simple uniform grids, this is the easiest way.

    Args:
        rows: Number of rows.
        cols: Number of columns.
        cell_width: Width of each cell in inches.
        cell_height: Height of each cell in inches.
        hgap: Horizontal gap between columns in inches.
        vgap: Vertical gap between rows in inches.
        left: Left margin in inches.
        right: Right margin in inches.
        top: Top margin in inches.
        bottom: Bottom margin in inches.

    Returns:
        GridLayout with all cells filled.

    Example:
        >>> layout = create_grid(2, 3, cell_width=2.5, cell_height=2.0)
        >>> fig, axes = create_figure_with_grid(layout)
        >>> # axes is a list of 6 axes in row-major order
    """
    spec = GridSpec.uniform(
        rows=rows,
        cols=cols,
        cell_width=cell_width,
        cell_height=cell_height,
        hgap=hgap,
        vgap=vgap,
        margins={"left": left, "right": right, "top": top, "bottom": bottom},
    )
    return GridLayout(spec).fill()


@dataclass(frozen=True)
class GridSpec:
    """
    Defines grid structure with exact inch dimensions.

    Attributes:
        col_widths: Width of each column in inches.
        row_heights: Height of each row in inches.
        hgap: Horizontal gap between columns in inches.
        vgap: Vertical gap between rows in inches.
        margins: Dict with left, right, top, bottom margins in inches.

    Example:
        >>> # Uniform 3x3 grid
        >>> spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.5, cell_height=2.0)
        >>> # Non-uniform grid
        >>> spec = GridSpec(
        ...     col_widths=(3.0, 2.0, 1.5),
        ...     row_heights=(2.0, 2.5, 2.0),
        ...     hgap=0.3,
        ...     vgap=0.4,
        ... )
    """

    col_widths: tuple[float, ...]
    row_heights: tuple[float, ...]
    hgap: float = 0.3
    vgap: float = 0.4
    margins: tuple[tuple[str, float], ...] = None  # Converted from dict for hashability

    def __post_init__(self) -> None:
        """Validate and set default margins."""
        if self.margins is None:
            # Use object.__setattr__ since frozen=True
            object.__setattr__(
                self, "margins", tuple(DEFAULT_MARGINS.items())
            )

    @classmethod
    def uniform(
        cls,
        rows: int,
        cols: int,
        cell_width: float,
        cell_height: float,
        hgap: float = 0.3,
        vgap: float = 0.4,
        margins: Optional[dict[str, float]] = None,
    ) -> "GridSpec":
        """
        Create grid with uniform cell sizes.

        Args:
            rows: Number of rows.
            cols: Number of columns.
            cell_width: Width of each cell in inches.
            cell_height: Height of each cell in inches.
            hgap: Horizontal gap between columns in inches.
            vgap: Vertical gap between rows in inches.
            margins: Dict with left, right, top, bottom margins.

        Returns:
            GridSpec with uniform cell dimensions.
        """
        margins_tuple = tuple((margins or DEFAULT_MARGINS).items())
        return cls(
            col_widths=tuple([cell_width] * cols),
            row_heights=tuple([cell_height] * rows),
            hgap=hgap,
            vgap=vgap,
            margins=margins_tuple,
        )

    @classmethod
    def from_figsize(
        cls,
        figsize: tuple[float, float],
        rows: int,
        cols: int,
        hgap: float = 0.3,
        vgap: float = 0.4,
        margins: Optional[dict[str, float]] = None,
        col_ratios: Optional[list[float]] = None,
        row_ratios: Optional[list[float]] = None,
    ) -> "GridSpec":
        """
        Create grid with fixed figure size, calculating cell sizes automatically.

        Args:
            figsize: Total figure (width, height) in inches.
            rows: Number of rows.
            cols: Number of columns.
            hgap: Horizontal gap between columns in inches.
            vgap: Vertical gap between rows in inches.
            margins: Dict with left, right, top, bottom margins.
            col_ratios: Relative column widths (e.g., [1, 2, 1] for 1:2:1 ratio).
                       If None, columns are equal width.
            row_ratios: Relative row heights (e.g., [1, 2] for 1:2 ratio).
                       If None, rows are equal height.

        Returns:
            GridSpec with cell sizes calculated to fit the figure size.

        Example:
            >>> # 7x5 inch figure with 2x3 grid
            >>> spec = GridSpec.from_figsize((7, 5), rows=2, cols=3)
            >>> assert spec.fig_width == 7.0
            >>> assert spec.fig_height == 5.0

            >>> # With non-uniform columns (1:2:1 ratio)
            >>> spec = GridSpec.from_figsize((7, 5), rows=2, cols=3, col_ratios=[1, 2, 1])
        """
        fig_width, fig_height = figsize
        margins_dict = margins or DEFAULT_MARGINS

        # Calculate available space for cells
        available_width = (
            fig_width
            - margins_dict["left"]
            - margins_dict["right"]
            - hgap * (cols - 1)
        )
        available_height = (
            fig_height
            - margins_dict["top"]
            - margins_dict["bottom"]
            - vgap * (rows - 1)
        )

        if available_width <= 0:
            raise ValueError(
                f"Figure width {fig_width} is too small for margins and gaps"
            )
        if available_height <= 0:
            raise ValueError(
                f"Figure height {fig_height} is too small for margins and gaps"
            )

        # Calculate column widths
        if col_ratios is None:
            col_widths = tuple([available_width / cols] * cols)
        else:
            if len(col_ratios) != cols:
                raise ValueError(
                    f"col_ratios length ({len(col_ratios)}) must match cols ({cols})"
                )
            total_ratio = sum(col_ratios)
            col_widths = tuple(r / total_ratio * available_width for r in col_ratios)

        # Calculate row heights
        if row_ratios is None:
            row_heights = tuple([available_height / rows] * rows)
        else:
            if len(row_ratios) != rows:
                raise ValueError(
                    f"row_ratios length ({len(row_ratios)}) must match rows ({rows})"
                )
            total_ratio = sum(row_ratios)
            row_heights = tuple(r / total_ratio * available_height for r in row_ratios)

        margins_tuple = tuple(margins_dict.items())
        return cls(
            col_widths=col_widths,
            row_heights=row_heights,
            hgap=hgap,
            vgap=vgap,
            margins=margins_tuple,
        )

    @classmethod
    def from_width(
        cls,
        fig_width: float,
        rows: int,
        cols: int,
        cell_height: float,
        hgap: float = 0.3,
        vgap: float = 0.4,
        margins: Optional[dict[str, float]] = None,
        col_ratios: Optional[list[float]] = None,
    ) -> "GridSpec":
        """
        Create grid with fixed figure width, calculating column widths automatically.

        Args:
            fig_width: Total figure width in inches.
            rows: Number of rows.
            cols: Number of columns.
            cell_height: Height of each cell in inches.
            hgap: Horizontal gap between columns in inches.
            vgap: Vertical gap between rows in inches.
            margins: Dict with left, right, top, bottom margins.
            col_ratios: Relative column widths. If None, columns are equal.

        Returns:
            GridSpec with column widths calculated to fit the figure width.

        Example:
            >>> spec = GridSpec.from_width(7.0, rows=2, cols=3, cell_height=2.0)
            >>> assert spec.fig_width == 7.0
        """
        margins_dict = margins or DEFAULT_MARGINS

        # Calculate available width for cells
        available_width = (
            fig_width
            - margins_dict["left"]
            - margins_dict["right"]
            - hgap * (cols - 1)
        )

        if available_width <= 0:
            raise ValueError(
                f"Figure width {fig_width} is too small for margins and gaps"
            )

        # Calculate column widths
        if col_ratios is None:
            col_widths = tuple([available_width / cols] * cols)
        else:
            if len(col_ratios) != cols:
                raise ValueError(
                    f"col_ratios length ({len(col_ratios)}) must match cols ({cols})"
                )
            total_ratio = sum(col_ratios)
            col_widths = tuple(r / total_ratio * available_width for r in col_ratios)

        margins_tuple = tuple(margins_dict.items())
        return cls(
            col_widths=col_widths,
            row_heights=tuple([cell_height] * rows),
            hgap=hgap,
            vgap=vgap,
            margins=margins_tuple,
        )

    @classmethod
    def from_height(
        cls,
        fig_height: float,
        rows: int,
        cols: int,
        cell_width: float,
        hgap: float = 0.3,
        vgap: float = 0.4,
        margins: Optional[dict[str, float]] = None,
        row_ratios: Optional[list[float]] = None,
    ) -> "GridSpec":
        """
        Create grid with fixed figure height, calculating row heights automatically.

        Args:
            fig_height: Total figure height in inches.
            rows: Number of rows.
            cols: Number of columns.
            cell_width: Width of each cell in inches.
            hgap: Horizontal gap between columns in inches.
            vgap: Vertical gap between rows in inches.
            margins: Dict with left, right, top, bottom margins.
            row_ratios: Relative row heights. If None, rows are equal.

        Returns:
            GridSpec with row heights calculated to fit the figure height.

        Example:
            >>> spec = GridSpec.from_height(5.0, rows=2, cols=3, cell_width=2.0)
            >>> assert spec.fig_height == 5.0
        """
        margins_dict = margins or DEFAULT_MARGINS

        # Calculate available height for cells
        available_height = (
            fig_height
            - margins_dict["top"]
            - margins_dict["bottom"]
            - vgap * (rows - 1)
        )

        if available_height <= 0:
            raise ValueError(
                f"Figure height {fig_height} is too small for margins and gaps"
            )

        # Calculate row heights
        if row_ratios is None:
            row_heights = tuple([available_height / rows] * rows)
        else:
            if len(row_ratios) != rows:
                raise ValueError(
                    f"row_ratios length ({len(row_ratios)}) must match rows ({rows})"
                )
            total_ratio = sum(row_ratios)
            row_heights = tuple(r / total_ratio * available_height for r in row_ratios)

        margins_tuple = tuple(margins_dict.items())
        return cls(
            col_widths=tuple([cell_width] * cols),
            row_heights=row_heights,
            hgap=hgap,
            vgap=vgap,
            margins=margins_tuple,
        )

    @classmethod
    def fixed_cells(
        cls,
        rows: int,
        cols: int,
        cell_width: float,
        cell_height: float,
        fig_width: Optional[float] = None,
        fig_height: Optional[float] = None,
        hgap: float = 0.3,
        vgap: float = 0.4,
        min_left: float = 0.5,
        min_bottom: float = 0.4,
        min_right: float = 0.1,
        min_top: float = 0.1,
        auto_gaps: bool = False,
    ) -> "GridSpec":
        """
        Create grid with fixed cell sizes and optional fixed figure dimensions.

        Margins are calculated automatically to fill the remaining space.
        If auto_gaps=True, gaps are also calculated to distribute space evenly.

        Args:
            rows: Number of rows.
            cols: Number of columns.
            cell_width: Width of each cell in inches.
            cell_height: Height of each cell in inches.
            fig_width: Total figure width in inches (optional).
            fig_height: Total figure height in inches (optional).
            hgap: Horizontal gap between columns in inches (ignored if auto_gaps=True).
            vgap: Vertical gap between rows in inches (ignored if auto_gaps=True).
            min_left: Minimum left margin in inches.
            min_bottom: Minimum bottom margin in inches.
            min_right: Minimum right margin in inches.
            min_top: Minimum top margin in inches.
            auto_gaps: If True, calculate gaps automatically to distribute
                      remaining space evenly between cells.

        Returns:
            GridSpec with fixed cell sizes and calculated margins/gaps.

        Example:
            >>> # Lock figure to 7 inches wide, cells are 2x2, auto gaps
            >>> spec = GridSpec.fixed_cells(
            ...     rows=2, cols=3,
            ...     cell_width=2.0, cell_height=2.0,
            ...     fig_width=8.0,
            ...     auto_gaps=True
            ... )
            >>> assert spec.fig_width == 8.0
            >>> assert spec.col_widths == (2.0, 2.0, 2.0)
        """
        if auto_gaps:
            # Calculate gaps to distribute remaining space evenly
            if fig_width is not None:
                cells_width = cols * cell_width
                remaining_width = fig_width - cells_width - min_left - min_right
                if remaining_width < 0:
                    raise ValueError(
                        f"Figure width {fig_width} is too small for "
                        f"{cols} cells of width {cell_width}. "
                        f"Need at least {cells_width + min_left + min_right:.2f} inches."
                    )
                # Distribute remaining space: gaps get space, margins stay at minimum
                if cols > 1:
                    hgap = remaining_width / (cols - 1)
                    left = min_left
                    right = min_right
                else:
                    hgap = 0
                    # Single column: extra space goes to margins
                    extra = remaining_width
                    left = min_left + extra * 0.8
                    right = min_right + extra * 0.2
            else:
                left = min_left
                right = min_right

            if fig_height is not None:
                cells_height = rows * cell_height
                remaining_height = fig_height - cells_height - min_top - min_bottom
                if remaining_height < 0:
                    raise ValueError(
                        f"Figure height {fig_height} is too small for "
                        f"{rows} cells of height {cell_height}. "
                        f"Need at least {cells_height + min_top + min_bottom:.2f} inches."
                    )
                # Distribute remaining space to gaps
                if rows > 1:
                    vgap = remaining_height / (rows - 1)
                    top = min_top
                    bottom = min_bottom
                else:
                    vgap = 0
                    # Single row: extra space goes to margins
                    extra = remaining_height
                    bottom = min_bottom + extra * 0.8
                    top = min_top + extra * 0.2
            else:
                top = min_top
                bottom = min_bottom
        else:
            # Fixed gaps, calculate margins
            content_width = cols * cell_width + (cols - 1) * hgap
            content_height = rows * cell_height + (rows - 1) * vgap

            # Calculate margins for width
            if fig_width is not None:
                available_h_margin = fig_width - content_width
                if available_h_margin < min_left + min_right:
                    raise ValueError(
                        f"Figure width {fig_width} is too small for "
                        f"{cols} cells of width {cell_width} with gaps {hgap}. "
                        f"Need at least {content_width + min_left + min_right:.2f} inches."
                    )
                # Distribute extra margin, keeping left larger (for y-axis labels)
                extra = available_h_margin - (min_left + min_right)
                left = min_left + extra * 0.8
                right = min_right + extra * 0.2
            else:
                left = min_left
                right = min_right

            # Calculate margins for height
            if fig_height is not None:
                available_v_margin = fig_height - content_height
                if available_v_margin < min_top + min_bottom:
                    raise ValueError(
                        f"Figure height {fig_height} is too small for "
                        f"{rows} cells of height {cell_height} with gaps {vgap}. "
                        f"Need at least {content_height + min_top + min_bottom:.2f} inches."
                    )
                # Distribute extra margin, keeping bottom larger (for x-axis labels)
                extra = available_v_margin - (min_top + min_bottom)
                bottom = min_bottom + extra * 0.8
                top = min_top + extra * 0.2
            else:
                top = min_top
                bottom = min_bottom

        margins = {"left": left, "right": right, "top": top, "bottom": bottom}
        margins_tuple = tuple(margins.items())

        return cls(
            col_widths=tuple([cell_width] * cols),
            row_heights=tuple([cell_height] * rows),
            hgap=hgap,
            vgap=vgap,
            margins=margins_tuple,
        )

    @property
    def num_rows(self) -> int:
        """Number of rows in the grid."""
        return len(self.row_heights)

    @property
    def num_cols(self) -> int:
        """Number of columns in the grid."""
        return len(self.col_widths)

    @property
    def margins_dict(self) -> dict[str, float]:
        """Get margins as dictionary."""
        return dict(self.margins)

    @property
    def fig_width(self) -> float:
        """Calculate total figure width in inches."""
        margins = self.margins_dict
        content_width = sum(self.col_widths) + self.hgap * (self.num_cols - 1)
        return margins["left"] + content_width + margins["right"]

    @property
    def fig_height(self) -> float:
        """Calculate total figure height in inches."""
        margins = self.margins_dict
        content_height = sum(self.row_heights) + self.vgap * (self.num_rows - 1)
        return margins["top"] + content_height + margins["bottom"]

    @property
    def fig_size_inches(self) -> tuple[float, float]:
        """Return (width, height) tuple for matplotlib."""
        return (self.fig_width, self.fig_height)


@dataclass
class GridCell:
    """
    Represents a subplot placement within the grid.

    Attributes:
        row: Starting row index (0-based, from top).
        col: Starting column index (0-based, from left).
        rowspan: Number of rows to span (default 1).
        colspan: Number of columns to span (default 1).
        axis_type: Type of axis (PLOT or IMAGE).
        name: Optional name for the subplot.
        sharex: Share x-axis with another cell (by name or index).
        sharey: Share y-axis with another cell (by name or index).
    """

    row: int
    col: int
    rowspan: int = 1
    colspan: int = 1
    axis_type: AxisType = AxisType.PLOT
    name: Optional[str] = None
    sharex: Optional[Union[str, int]] = None
    sharey: Optional[Union[str, int]] = None

    def validate(self, spec: GridSpec) -> None:
        """
        Validate cell fits within grid bounds.

        Args:
            spec: GridSpec defining the grid structure.

        Raises:
            ValueError: If cell is out of bounds.
        """
        if self.row < 0 or self.row >= spec.num_rows:
            raise ValueError(
                f"Row {self.row} is out of bounds (0 to {spec.num_rows - 1})"
            )
        if self.col < 0 or self.col >= spec.num_cols:
            raise ValueError(
                f"Column {self.col} is out of bounds (0 to {spec.num_cols - 1})"
            )
        if self.row + self.rowspan > spec.num_rows:
            raise ValueError(
                f"Cell spans rows {self.row} to {self.row + self.rowspan - 1}, "
                f"but grid only has {spec.num_rows} rows"
            )
        if self.col + self.colspan > spec.num_cols:
            raise ValueError(
                f"Cell spans columns {self.col} to {self.col + self.colspan - 1}, "
                f"but grid only has {spec.num_cols} columns"
            )

    def occupied_positions(self) -> set[tuple[int, int]]:
        """Return set of (row, col) positions occupied by this cell."""
        positions = set()
        for r in range(self.row, self.row + self.rowspan):
            for c in range(self.col, self.col + self.colspan):
                positions.add((r, c))
        return positions


class GridLayout:
    """
    Grid-based subplot layout with spanning support.

    Provides subplot2grid-like functionality with exact inch specifications.

    Example:
        >>> spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.5, cell_height=2.0)
        >>> layout = GridLayout(spec)
        >>> layout.add_cell(0, 0, colspan=3)           # Top row spans all columns
        >>> layout.add_cell(1, 0, colspan=2)           # Middle-left spans 2 columns
        >>> layout.add_cell(1, 2, rowspan=2, axis_type=AxisType.IMAGE)  # Right side
        >>> layout.add_cell(2, 0)                      # Bottom-left
        >>> layout.add_cell(2, 1)                      # Bottom-middle
        >>> fig, axes = create_figure_with_grid(layout)
    """

    def __init__(
        self,
        spec: Optional[GridSpec] = None,
        config: Optional[dict[str, Any]] = None,
        yaml_file: Optional[Union[str, Path]] = None,
    ) -> None:
        """
        Initialize from GridSpec, config dict, or YAML file.

        Args:
            spec: GridSpec defining the grid structure.
            config: Configuration dictionary (alternative to spec).
            yaml_file: Path to YAML configuration (alternative to spec).

        Raises:
            ValueError: If no valid configuration source is provided.
        """
        self._cells: list[GridCell] = []
        self._occupied: set[tuple[int, int]] = set()

        if spec is not None:
            self._spec = spec
        elif config is not None:
            self._spec, self._cells = self._parse_config(config)
            self._update_occupied()
        elif yaml_file is not None:
            self._spec, self._cells = self._load_yaml(yaml_file)
            self._update_occupied()
        else:
            raise ValueError("Must provide spec, config, or yaml_file")

    def _parse_config(
        self, config: dict[str, Any]
    ) -> tuple[GridSpec, list[GridCell]]:
        """Parse configuration dictionary into GridSpec and cells."""
        grid_config = config.get("grid", config)

        # Parse grid spec
        spec = self._parse_grid_spec(grid_config)

        # Parse cells if present
        cells = []
        if "cells" in config:
            for cell_config in config["cells"]:
                cells.append(self._parse_cell(cell_config))

        return spec, cells

    def _parse_grid_spec(self, config: dict[str, Any]) -> GridSpec:
        """Parse grid specification from config."""
        # Handle col_widths - can be single value or list
        col_widths = config.get("col_widths")
        if col_widths is None:
            cols = config.get("cols", 1)
            cell_width = config.get("cell_width", 2.5)
            col_widths = tuple([cell_width] * cols)
        elif isinstance(col_widths, (int, float)):
            cols = config.get("cols", 1)
            col_widths = tuple([col_widths] * cols)
        else:
            col_widths = tuple(col_widths)

        # Handle row_heights - can be single value or list
        row_heights = config.get("row_heights")
        if row_heights is None:
            rows = config.get("rows", 1)
            cell_height = config.get("cell_height", 2.0)
            row_heights = tuple([cell_height] * rows)
        elif isinstance(row_heights, (int, float)):
            rows = config.get("rows", 1)
            row_heights = tuple([row_heights] * rows)
        else:
            row_heights = tuple(row_heights)

        margins = config.get("margins", DEFAULT_MARGINS)
        margins_tuple = tuple(margins.items())

        return GridSpec(
            col_widths=col_widths,
            row_heights=row_heights,
            hgap=config.get("hgap", 0.3),
            vgap=config.get("vgap", 0.4),
            margins=margins_tuple,
        )

    def _parse_cell(self, config: dict[str, Any]) -> GridCell:
        """Parse a single cell configuration."""
        pos = config.get("pos", [0, 0])
        axis_type_str = config.get("axis_type", "plot").upper()
        axis_type = AxisType[axis_type_str]

        return GridCell(
            row=pos[0],
            col=pos[1],
            rowspan=config.get("rowspan", 1),
            colspan=config.get("colspan", 1),
            axis_type=axis_type,
            name=config.get("name"),
            sharex=config.get("sharex"),
            sharey=config.get("sharey"),
        )

    def _load_yaml(
        self, yaml_file: Union[str, Path]
    ) -> tuple[GridSpec, list[GridCell]]:
        """Load configuration from YAML file."""
        yaml_path = Path(yaml_file)
        if not yaml_path.exists():
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")

        with open(yaml_path) as f:
            config = yaml.safe_load(f)

        return self._parse_config(config)

    def _update_occupied(self) -> None:
        """Update the set of occupied positions from current cells."""
        self._occupied = set()
        for cell in self._cells:
            self._occupied.update(cell.occupied_positions())

    @property
    def spec(self) -> GridSpec:
        """Get the grid specification."""
        return self._spec

    @property
    def fig_size_inches(self) -> tuple[float, float]:
        """Figure size in inches (for matplotlib compatibility)."""
        return self._spec.fig_size_inches

    @property
    def cells(self) -> list[GridCell]:
        """List of defined cells."""
        return self._cells.copy()

    def fill(
        self,
        axis_type: Union[AxisType, str] = AxisType.PLOT,
    ) -> "GridLayout":
        """
        Fill the entire grid with 1x1 cells.

        Args:
            axis_type: Type of axis for all cells.

        Returns:
            Self for method chaining.

        Example:
            >>> spec = GridSpec.uniform(rows=2, cols=3, cell_width=2.0, cell_height=2.0)
            >>> layout = GridLayout(spec).fill()
            >>> # Creates 6 cells in row-major order
        """
        for row in range(self._spec.num_rows):
            for col in range(self._spec.num_cols):
                if (row, col) not in self._occupied:
                    self.add_cell(row, col, axis_type=axis_type)
        return self

    def fill_row(
        self,
        row: int,
        axis_type: Union[AxisType, str] = AxisType.PLOT,
    ) -> "GridLayout":
        """
        Fill a single row with 1x1 cells.

        Args:
            row: Row index to fill.
            axis_type: Type of axis for cells in this row.

        Returns:
            Self for method chaining.

        Example:
            >>> layout.fill_row(0)  # Fill first row
            >>> layout.fill_row(1, axis_type=AxisType.IMAGE)  # Fill second row with image axes
        """
        for col in range(self._spec.num_cols):
            if (row, col) not in self._occupied:
                self.add_cell(row, col, axis_type=axis_type)
        return self

    def add_cell(
        self,
        row: int,
        col: int,
        rowspan: int = 1,
        colspan: int = 1,
        axis_type: Union[AxisType, str] = AxisType.PLOT,
        name: Optional[str] = None,
        sharex: Optional[Union[str, int]] = None,
        sharey: Optional[Union[str, int]] = None,
    ) -> "GridLayout":
        """
        Add a subplot cell to the layout.

        Args:
            row: Starting row index (0-based, from top).
            col: Starting column index (0-based, from left).
            rowspan: Number of rows to span.
            colspan: Number of columns to span.
            axis_type: Type of axis (AxisType.PLOT, AxisType.IMAGE, or string).
            name: Optional name for the subplot.
            sharex: Share x-axis with another cell (by name or index).
            sharey: Share y-axis with another cell (by name or index).

        Returns:
            Self for method chaining.

        Raises:
            ValueError: If cell overlaps with existing cells or is out of bounds.
        """
        # Convert string axis_type to enum
        if isinstance(axis_type, str):
            axis_type = AxisType[axis_type.upper()]

        cell = GridCell(
            row=row,
            col=col,
            rowspan=rowspan,
            colspan=colspan,
            axis_type=axis_type,
            name=name,
            sharex=sharex,
            sharey=sharey,
        )

        # Validate bounds
        cell.validate(self._spec)

        # Check for overlaps
        new_positions = cell.occupied_positions()
        overlap = self._occupied & new_positions
        if overlap:
            raise ValueError(
                f"Cell at ({row}, {col}) overlaps with existing cells at {overlap}"
            )

        self._cells.append(cell)
        self._occupied.update(new_positions)
        return self

    def get_coordinates(self) -> list[tuple[float, float, float, float]]:
        """
        Calculate subplot coordinates.

        Returns:
            List of (left, bottom, width, height) tuples in figure-relative
            units (0-1) for each cell, in order added.
        """
        fig_width, fig_height = self.fig_size_inches
        margins = self._spec.margins_dict
        coords = []

        for cell in self._cells:
            # Calculate left position
            left = margins["left"]
            for c in range(cell.col):
                left += self._spec.col_widths[c] + self._spec.hgap

            # Calculate width (sum of spanned columns + gaps between them)
            width = sum(self._spec.col_widths[cell.col : cell.col + cell.colspan])
            width += self._spec.hgap * (cell.colspan - 1)

            # Calculate bottom position (from top, so we need to compute differently)
            # Start from top margin, go down through rows
            top_offset = margins["top"]
            for r in range(cell.row):
                top_offset += self._spec.row_heights[r] + self._spec.vgap

            # Height spans multiple rows
            height = sum(self._spec.row_heights[cell.row : cell.row + cell.rowspan])
            height += self._spec.vgap * (cell.rowspan - 1)

            # Bottom = figure_height - top_offset - height
            bottom = fig_height - top_offset - height

            # Convert to relative coordinates (0-1)
            left_rel = left / fig_width
            bottom_rel = bottom / fig_height
            width_rel = width / fig_width
            height_rel = height / fig_height

            coords.append((left_rel, bottom_rel, width_rel, height_rel))

        return coords

    def get_final_coordinates(self) -> list[tuple[float, float, float, float]]:
        """
        Get coordinates with IMAGE cells expanded to fill gap space.

        IMAGE cells expand by half the hgap/vgap on each side since they
        don't need space for axis labels.

        Returns:
            List of (left, bottom, width, height) tuples with IMAGE cells expanded.
        """
        base_coords = self.get_coordinates()
        fig_width, fig_height = self.fig_size_inches

        final_coords = []
        for coord, cell in zip(base_coords, self._cells):
            if cell.axis_type == AxisType.IMAGE:
                coord = self._expand_image_coord(coord, cell, fig_width, fig_height)
            final_coords.append(coord)

        return final_coords

    def _expand_image_coord(
        self,
        coord: tuple[float, float, float, float],
        cell: GridCell,
        fig_width: float,
        fig_height: float,
    ) -> tuple[float, float, float, float]:
        """
        Expand an IMAGE cell to fill adjacent gap space.

        Expands by half hgap to the left and half vgap downward (towards
        where axis labels typically are), but respects figure boundaries.
        """
        left, bottom, width, height = coord

        # Calculate expansion in relative units
        half_hgap = (self._spec.hgap / 2) / fig_width
        half_vgap = (self._spec.vgap / 2) / fig_height

        # Expand left only (towards y-axis labels area)
        new_left = max(0.0, left - half_hgap)
        left_expansion = left - new_left

        # Expand down only (towards x-axis labels area)
        new_bottom = max(0.0, bottom - half_vgap)
        bottom_expansion = bottom - new_bottom

        # Width increases by left expansion only
        new_width = width + left_expansion

        # Height increases by bottom expansion only
        new_height = height + bottom_expansion

        return (new_left, new_bottom, new_width, new_height)

    def get_axis_types(self) -> list[AxisType]:
        """Return axis types for each cell in order."""
        return [cell.axis_type for cell in self._cells]

    def get_cell_index(self, ref: Union[str, int]) -> int:
        """
        Resolve a cell reference to an index.

        Args:
            ref: Cell name (string) or index (int).

        Returns:
            Index of the cell in the cells list.

        Raises:
            ValueError: If cell reference is invalid.
        """
        if isinstance(ref, int):
            if ref < 0 or ref >= len(self._cells):
                raise ValueError(
                    f"Cell index {ref} is out of bounds (0 to {len(self._cells) - 1})"
                )
            return ref
        else:
            for i, cell in enumerate(self._cells):
                if cell.name == ref:
                    return i
            raise ValueError(f"No cell found with name '{ref}'")

    def get_share_info(self) -> list[tuple[Optional[int], Optional[int]]]:
        """
        Get axis sharing information for each cell.

        Returns:
            List of (sharex_index, sharey_index) tuples for each cell.
            None values indicate no sharing for that axis.
        """
        share_info = []
        for cell in self._cells:
            sharex_idx = None
            sharey_idx = None
            if cell.sharex is not None:
                sharex_idx = self.get_cell_index(cell.sharex)
            if cell.sharey is not None:
                sharey_idx = self.get_cell_index(cell.sharey)
            share_info.append((sharex_idx, sharey_idx))
        return share_info

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation."""
        cells_list = []
        for cell in self._cells:
            cell_dict = {
                "pos": [cell.row, cell.col],
                "rowspan": cell.rowspan,
                "colspan": cell.colspan,
                "axis_type": cell.axis_type.name.lower(),
                "name": cell.name,
            }
            if cell.sharex is not None:
                cell_dict["sharex"] = cell.sharex
            if cell.sharey is not None:
                cell_dict["sharey"] = cell.sharey
            cells_list.append(cell_dict)

        return {
            "grid": {
                "col_widths": list(self._spec.col_widths),
                "row_heights": list(self._spec.row_heights),
                "hgap": self._spec.hgap,
                "vgap": self._spec.vgap,
                "margins": self._spec.margins_dict,
            },
            "cells": cells_list,
        }

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

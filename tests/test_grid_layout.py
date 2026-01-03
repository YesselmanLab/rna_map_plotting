"""Tests for yplot.layout.grid_layout module."""

import tempfile
from pathlib import Path

import pytest

from yplot.layout import AxisType, GridCell, GridLayout, GridSpec, create_grid
from yplot.figure import create_figure_with_grid


class TestAxisType:
    """Tests for AxisType enum."""

    def test_axis_type_plot(self):
        """AxisType.PLOT exists."""
        assert AxisType.PLOT is not None

    def test_axis_type_image(self):
        """AxisType.IMAGE exists."""
        assert AxisType.IMAGE is not None


class TestGridSpec:
    """Tests for GridSpec class."""

    def test_uniform_creates_grid(self):
        """GridSpec.uniform creates uniform cell grid."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.5, cell_height=2.0)
        assert spec.num_rows == 3
        assert spec.num_cols == 3
        assert spec.col_widths == (2.5, 2.5, 2.5)
        assert spec.row_heights == (2.0, 2.0, 2.0)

    def test_uniform_with_gaps(self):
        """GridSpec.uniform accepts gap parameters."""
        spec = GridSpec.uniform(
            rows=2, cols=2, cell_width=3.0, cell_height=2.5, hgap=0.5, vgap=0.6
        )
        assert spec.hgap == 0.5
        assert spec.vgap == 0.6

    def test_uniform_with_margins(self):
        """GridSpec.uniform accepts margin parameters."""
        margins = {"left": 1.0, "right": 0.5, "top": 0.2, "bottom": 0.8}
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0, margins=margins)
        assert spec.margins_dict == margins

    def test_non_uniform_col_widths(self):
        """GridSpec with different column widths."""
        spec = GridSpec(
            col_widths=(3.0, 2.0, 1.5),
            row_heights=(2.0, 2.5),
        )
        assert spec.col_widths == (3.0, 2.0, 1.5)
        assert spec.num_cols == 3
        assert spec.num_rows == 2

    def test_fig_width_calculation(self):
        """GridSpec calculates correct figure width."""
        spec = GridSpec.uniform(
            rows=1,
            cols=3,
            cell_width=2.0,
            cell_height=2.0,
            hgap=0.5,
            margins={"left": 0.5, "right": 0.1, "top": 0.1, "bottom": 0.4},
        )
        # width = left + 3*cell + 2*gap + right = 0.5 + 6.0 + 1.0 + 0.1 = 7.6
        assert spec.fig_width == pytest.approx(7.6)

    def test_fig_height_calculation(self):
        """GridSpec calculates correct figure height."""
        spec = GridSpec.uniform(
            rows=3,
            cols=1,
            cell_width=2.0,
            cell_height=2.0,
            vgap=0.4,
            margins={"left": 0.5, "right": 0.1, "top": 0.1, "bottom": 0.5},
        )
        # height = top + 3*cell + 2*gap + bottom = 0.1 + 6.0 + 0.8 + 0.5 = 7.4
        assert spec.fig_height == pytest.approx(7.4)

    def test_fig_size_inches(self):
        """GridSpec.fig_size_inches returns tuple."""
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0)
        size = spec.fig_size_inches
        assert isinstance(size, tuple)
        assert len(size) == 2

    def test_frozen_dataclass(self):
        """GridSpec is immutable (frozen)."""
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0)
        with pytest.raises(AttributeError):
            spec.hgap = 1.0


class TestGridCell:
    """Tests for GridCell class."""

    def test_cell_defaults(self):
        """GridCell has correct default values."""
        cell = GridCell(row=0, col=0)
        assert cell.rowspan == 1
        assert cell.colspan == 1
        assert cell.axis_type == AxisType.PLOT
        assert cell.name is None

    def test_cell_with_span(self):
        """GridCell accepts span parameters."""
        cell = GridCell(row=1, col=0, rowspan=2, colspan=3)
        assert cell.rowspan == 2
        assert cell.colspan == 3

    def test_cell_with_axis_type(self):
        """GridCell accepts axis_type parameter."""
        cell = GridCell(row=0, col=0, axis_type=AxisType.IMAGE)
        assert cell.axis_type == AxisType.IMAGE

    def test_cell_validate_in_bounds(self):
        """GridCell validates within grid bounds."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.0, cell_height=2.0)
        cell = GridCell(row=1, col=1)
        cell.validate(spec)  # Should not raise

    def test_cell_validate_row_out_of_bounds(self):
        """GridCell validation fails for row out of bounds."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.0, cell_height=2.0)
        cell = GridCell(row=5, col=0)
        with pytest.raises(ValueError, match="Row 5 is out of bounds"):
            cell.validate(spec)

    def test_cell_validate_col_out_of_bounds(self):
        """GridCell validation fails for column out of bounds."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.0, cell_height=2.0)
        cell = GridCell(row=0, col=5)
        with pytest.raises(ValueError, match="Column 5 is out of bounds"):
            cell.validate(spec)

    def test_cell_validate_rowspan_exceeds(self):
        """GridCell validation fails when rowspan exceeds grid."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.0, cell_height=2.0)
        cell = GridCell(row=2, col=0, rowspan=2)  # Would span row 2-3, but only 3 rows
        with pytest.raises(ValueError, match="spans rows"):
            cell.validate(spec)

    def test_cell_validate_colspan_exceeds(self):
        """GridCell validation fails when colspan exceeds grid."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.0, cell_height=2.0)
        cell = GridCell(row=0, col=2, colspan=2)  # Would span col 2-3, but only 3 cols
        with pytest.raises(ValueError, match="spans columns"):
            cell.validate(spec)

    def test_occupied_positions_single(self):
        """GridCell.occupied_positions returns single position for 1x1 cell."""
        cell = GridCell(row=1, col=2)
        assert cell.occupied_positions() == {(1, 2)}

    def test_occupied_positions_span(self):
        """GridCell.occupied_positions returns all positions for spanning cell."""
        cell = GridCell(row=0, col=0, rowspan=2, colspan=3)
        expected = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)}
        assert cell.occupied_positions() == expected


class TestGridLayout:
    """Tests for GridLayout class."""

    def test_init_with_spec(self):
        """GridLayout initializes from GridSpec."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        assert layout.fig_size_inches == spec.fig_size_inches

    def test_init_without_args_raises(self):
        """GridLayout raises without spec, config, or yaml_file."""
        with pytest.raises(ValueError, match="Must provide"):
            GridLayout()

    def test_add_cell_returns_self(self):
        """add_cell returns self for chaining."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        result = layout.add_cell(0, 0)
        assert result is layout

    def test_method_chaining(self):
        """GridLayout supports method chaining."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.0, cell_height=2.0)
        layout = (
            GridLayout(spec)
            .add_cell(0, 0, colspan=3)
            .add_cell(1, 0, colspan=2)
            .add_cell(1, 2, rowspan=2)
        )
        assert len(layout.cells) == 3

    def test_add_cell_with_string_axis_type(self):
        """add_cell accepts string axis_type."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0, axis_type="image")
        assert layout.cells[0].axis_type == AxisType.IMAGE

    def test_add_cell_validates_bounds(self):
        """add_cell validates cell is within bounds."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        with pytest.raises(ValueError, match="out of bounds"):
            layout.add_cell(5, 0)

    def test_add_cell_detects_overlap(self):
        """add_cell detects overlapping cells."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0, colspan=2)
        with pytest.raises(ValueError, match="overlaps"):
            layout.add_cell(0, 1)  # Overlaps with first cell

    def test_get_coordinates_single_cell(self):
        """get_coordinates returns correct coords for single cell."""
        spec = GridSpec.uniform(
            rows=2,
            cols=2,
            cell_width=2.0,
            cell_height=2.0,
            hgap=0.0,
            vgap=0.0,
            margins={"left": 0.0, "right": 0.0, "top": 0.0, "bottom": 0.0},
        )
        layout = GridLayout(spec)
        layout.add_cell(0, 0)
        coords = layout.get_coordinates()

        assert len(coords) == 1
        left, bottom, width, height = coords[0]
        # Cell at top-left: left=0, bottom=0.5 (second row), width=0.5, height=0.5
        assert left == pytest.approx(0.0)
        assert bottom == pytest.approx(0.5)  # Top row starts at 0.5
        assert width == pytest.approx(0.5)
        assert height == pytest.approx(0.5)

    def test_get_coordinates_with_span(self):
        """get_coordinates handles spanning cells correctly."""
        spec = GridSpec.uniform(
            rows=3,
            cols=3,
            cell_width=2.0,
            cell_height=2.0,
            hgap=0.0,
            vgap=0.0,
            margins={"left": 0.0, "right": 0.0, "top": 0.0, "bottom": 0.0},
        )
        layout = GridLayout(spec)
        layout.add_cell(0, 0, colspan=3)  # Top row spanning all columns
        coords = layout.get_coordinates()

        left, bottom, width, height = coords[0]
        # Should span full width
        assert width == pytest.approx(1.0)

    def test_get_final_coordinates_plot_unchanged(self):
        """get_final_coordinates returns same as get_coordinates for PLOT cells."""
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0, axis_type=AxisType.PLOT)
        # PLOT cells are not expanded
        assert layout.get_coordinates() == layout.get_final_coordinates()

    def test_get_axis_types(self):
        """get_axis_types returns types in order."""
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0, axis_type=AxisType.PLOT)
        layout.add_cell(0, 1, axis_type=AxisType.IMAGE)
        layout.add_cell(1, 0, axis_type=AxisType.IMAGE)

        types = layout.get_axis_types()
        assert types == [AxisType.PLOT, AxisType.IMAGE, AxisType.IMAGE]

    def test_cells_property_returns_copy(self):
        """cells property returns a copy, not original."""
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0)
        cells = layout.cells
        cells.append(GridCell(1, 1))  # Modify the copy
        assert len(layout.cells) == 1  # Original unchanged


class TestGridLayoutConfig:
    """Tests for GridLayout configuration loading."""

    def test_init_with_config_dict(self):
        """GridLayout initializes from config dict."""
        config = {
            "grid": {
                "rows": 3,
                "cols": 3,
                "col_widths": 2.5,
                "row_heights": 2.0,
                "hgap": 0.3,
                "vgap": 0.4,
            },
            "cells": [
                {"pos": [0, 0], "colspan": 3},
                {"pos": [1, 0], "colspan": 2},
                {"pos": [1, 2], "rowspan": 2, "axis_type": "image"},
            ],
        }
        layout = GridLayout(config=config)
        assert len(layout.cells) == 3
        assert layout.cells[2].axis_type == AxisType.IMAGE

    def test_init_with_yaml(self):
        """GridLayout initializes from YAML file."""
        import yaml

        config = {
            "grid": {
                "rows": 2,
                "cols": 2,
                "col_widths": 2.0,
                "row_heights": 2.0,
            },
            "cells": [{"pos": [0, 0]}],
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(config, f)
            f.flush()
            layout = GridLayout(yaml_file=f.name)
            assert len(layout.cells) == 1

    def test_yaml_file_not_found(self):
        """GridLayout raises for missing YAML file."""
        with pytest.raises(FileNotFoundError):
            GridLayout(yaml_file="/nonexistent/file.yaml")

    def test_to_dict(self):
        """to_dict returns configuration dictionary."""
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0, colspan=2, axis_type=AxisType.IMAGE, name="top")

        result = layout.to_dict()
        assert "grid" in result
        assert "cells" in result
        assert len(result["cells"]) == 1
        assert result["cells"][0]["colspan"] == 2
        assert result["cells"][0]["axis_type"] == "image"
        assert result["cells"][0]["name"] == "top"

    def test_to_yaml(self):
        """to_yaml saves configuration to file."""
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0)

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "layout.yaml"
            layout.to_yaml(path)
            assert path.exists()

            # Verify it can be loaded back
            loaded = GridLayout(yaml_file=path)
            assert len(loaded.cells) == 1


class TestGridLayoutSubplot2GridExample:
    """Test GridLayout replicating matplotlib's subplot2grid example."""

    def test_subplot2grid_example(self):
        """
        Replicate matplotlib subplot2grid example:
        ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
        ax2 = plt.subplot2grid((3, 3), (1, 0), colspan=2)
        ax3 = plt.subplot2grid((3, 3), (1, 2), rowspan=2)
        ax4 = plt.subplot2grid((3, 3), (2, 0))
        ax5 = plt.subplot2grid((3, 3), (2, 1))
        """
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.5, cell_height=2.0)
        layout = (
            GridLayout(spec)
            .add_cell(0, 0, colspan=3, name="ax1")
            .add_cell(1, 0, colspan=2, name="ax2")
            .add_cell(1, 2, rowspan=2, name="ax3")
            .add_cell(2, 0, name="ax4")
            .add_cell(2, 1, name="ax5")
        )

        assert len(layout.cells) == 5
        coords = layout.get_coordinates()
        assert len(coords) == 5

        # All coordinates should be valid (0-1 range)
        for left, bottom, width, height in coords:
            assert 0 <= left < 1
            assert 0 <= bottom < 1
            assert 0 < width <= 1
            assert 0 < height <= 1


class TestCreateFigureWithGrid:
    """Tests for create_figure_with_grid function."""

    def test_creates_figure_and_axes(self):
        """create_figure_with_grid returns figure and axes list."""
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0)
        layout.add_cell(0, 1)

        fig, axes = create_figure_with_grid(layout)
        assert fig is not None
        assert len(axes) == 2

    def test_correct_number_of_axes(self):
        """create_figure_with_grid creates correct number of axes."""
        spec = GridSpec.uniform(rows=3, cols=3, cell_width=2.0, cell_height=2.0)
        layout = (
            GridLayout(spec)
            .add_cell(0, 0, colspan=3)
            .add_cell(1, 0, colspan=2)
            .add_cell(1, 2, rowspan=2)
            .add_cell(2, 0)
            .add_cell(2, 1)
        )

        fig, axes = create_figure_with_grid(layout)
        assert len(axes) == 5

    def test_image_axes_have_no_ticks(self):
        """IMAGE axis type has no ticks."""
        spec = GridSpec.uniform(rows=1, cols=2, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0, axis_type=AxisType.PLOT)
        layout.add_cell(0, 1, axis_type=AxisType.IMAGE)

        fig, axes = create_figure_with_grid(layout)

        # Plot axis should have ticks
        plot_ax = axes[0]
        assert len(plot_ax.get_xticks()) > 0 or len(plot_ax.get_yticks()) > 0

        # Image axis should have no visible ticks
        image_ax = axes[1]
        assert len(image_ax.get_xticks()) == 0
        assert len(image_ax.get_yticks()) == 0

    def test_image_axes_have_no_spines(self):
        """IMAGE axis type has no visible spines."""
        spec = GridSpec.uniform(rows=1, cols=1, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0, axis_type=AxisType.IMAGE)

        fig, axes = create_figure_with_grid(layout)
        ax = axes[0]

        for spine in ax.spines.values():
            assert not spine.get_visible()

    def test_apply_axis_types_false(self):
        """apply_axis_types=False skips axis type configuration."""
        spec = GridSpec.uniform(rows=1, cols=1, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0, axis_type=AxisType.IMAGE)

        fig, axes = create_figure_with_grid(layout, apply_axis_types=False)
        ax = axes[0]

        # Should still have spines visible
        for spine in ax.spines.values():
            assert spine.get_visible()

    def test_figure_size_matches_spec(self):
        """Figure size matches GridSpec calculation."""
        spec = GridSpec.uniform(
            rows=2,
            cols=2,
            cell_width=2.0,
            cell_height=2.0,
            hgap=0.5,
            vgap=0.5,
            margins={"left": 0.5, "right": 0.1, "top": 0.1, "bottom": 0.4},
        )
        layout = GridLayout(spec)
        layout.add_cell(0, 0)

        fig, _ = create_figure_with_grid(layout)
        actual_size = fig.get_size_inches()

        assert actual_size[0] == pytest.approx(spec.fig_width)
        assert actual_size[1] == pytest.approx(spec.fig_height)


class TestGridLayoutFill:
    """Tests for GridLayout fill methods."""

    def test_fill_creates_all_cells(self):
        """fill() creates cells for entire grid."""
        spec = GridSpec.uniform(rows=2, cols=3, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec).fill()
        assert len(layout.cells) == 6

    def test_fill_returns_self(self):
        """fill() returns self for chaining."""
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        result = layout.fill()
        assert result is layout

    def test_fill_skips_occupied(self):
        """fill() skips already occupied cells."""
        spec = GridSpec.uniform(rows=2, cols=3, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0, colspan=2)  # Occupies (0,0) and (0,1)
        layout.fill()
        # Should have: 1 spanning cell + 4 filled cells = 5 total
        assert len(layout.cells) == 5

    def test_fill_with_axis_type(self):
        """fill() accepts axis_type parameter."""
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec).fill(axis_type=AxisType.IMAGE)
        for cell in layout.cells:
            assert cell.axis_type == AxisType.IMAGE

    def test_fill_row_single_row(self):
        """fill_row() fills specified row."""
        spec = GridSpec.uniform(rows=2, cols=3, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.fill_row(0)
        assert len(layout.cells) == 3
        for cell in layout.cells:
            assert cell.row == 0

    def test_fill_row_returns_self(self):
        """fill_row() returns self for chaining."""
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        result = layout.fill_row(0)
        assert result is layout

    def test_fill_row_with_axis_type(self):
        """fill_row() accepts axis_type parameter."""
        spec = GridSpec.uniform(rows=2, cols=2, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.fill_row(0, axis_type=AxisType.PLOT)
        layout.fill_row(1, axis_type=AxisType.IMAGE)

        types = layout.get_axis_types()
        assert types[:2] == [AxisType.PLOT, AxisType.PLOT]
        assert types[2:] == [AxisType.IMAGE, AxisType.IMAGE]

    def test_fill_row_skips_occupied(self):
        """fill_row() skips occupied cells."""
        spec = GridSpec.uniform(rows=2, cols=3, cell_width=2.0, cell_height=2.0)
        layout = GridLayout(spec)
        layout.add_cell(0, 0, colspan=2)
        layout.fill_row(0)
        # Row 0 has spanning cell (0,0)-(0,1) and filled cell (0,2)
        assert len(layout.cells) == 2


class TestCreateGrid:
    """Tests for create_grid convenience function."""

    def test_creates_filled_grid(self):
        """create_grid creates a filled grid layout."""
        layout = create_grid(2, 3)
        assert len(layout.cells) == 6

    def test_cell_dimensions(self):
        """create_grid uses specified cell dimensions."""
        layout = create_grid(2, 2, cell_width=3.0, cell_height=2.5)
        assert layout.spec.col_widths == (3.0, 3.0)
        assert layout.spec.row_heights == (2.5, 2.5)

    def test_gaps(self):
        """create_grid uses specified gaps."""
        layout = create_grid(2, 2, hgap=0.5, vgap=0.6)
        assert layout.spec.hgap == 0.5
        assert layout.spec.vgap == 0.6

    def test_margins(self):
        """create_grid uses specified margins."""
        layout = create_grid(2, 2, left=1.0, right=0.5, top=0.3, bottom=0.8)
        margins = layout.spec.margins_dict
        assert margins["left"] == 1.0
        assert margins["right"] == 0.5
        assert margins["top"] == 0.3
        assert margins["bottom"] == 0.8

    def test_works_with_create_figure(self):
        """create_grid result works with create_figure_with_grid."""
        layout = create_grid(2, 2, cell_width=2.0, cell_height=2.0)
        fig, axes = create_figure_with_grid(layout)
        assert len(axes) == 4

    def test_default_margins(self):
        """create_grid has sensible default margins."""
        layout = create_grid(2, 2)
        margins = layout.spec.margins_dict
        assert margins["left"] == 0.5
        assert margins["right"] == 0.1
        assert margins["top"] == 0.1
        assert margins["bottom"] == 0.4


class TestImageExpansion:
    """Tests for IMAGE cell expansion."""

    def test_image_cells_are_expanded(self):
        """IMAGE cells are larger than PLOT cells due to expansion."""
        spec = GridSpec.uniform(
            rows=1, cols=2,
            cell_width=2.0, cell_height=2.0,
            hgap=0.4, vgap=0.4,
        )
        layout = GridLayout(spec)
        layout.add_cell(0, 0, axis_type=AxisType.PLOT)
        layout.add_cell(0, 1, axis_type=AxisType.IMAGE)

        base_coords = layout.get_coordinates()
        final_coords = layout.get_final_coordinates()

        # PLOT cell should be unchanged
        assert base_coords[0] == final_coords[0]

        # IMAGE cell should be expanded (larger width and height)
        assert final_coords[1][2] > base_coords[1][2]  # width
        assert final_coords[1][3] > base_coords[1][3]  # height

    def test_image_expansion_uses_half_gap(self):
        """IMAGE cells expand by half the gap on each side."""
        spec = GridSpec.uniform(
            rows=1, cols=1,
            cell_width=2.0, cell_height=2.0,
            hgap=0.4, vgap=0.6,
            margins={"left": 1.0, "right": 1.0, "top": 1.0, "bottom": 1.0},
        )
        layout = GridLayout(spec)
        layout.add_cell(0, 0, axis_type=AxisType.IMAGE)

        base = layout.get_coordinates()[0]
        final = layout.get_final_coordinates()[0]

        fig_width, fig_height = layout.fig_size_inches

        # Width should increase by hgap (0.2 on each side = 0.4 total)
        expected_width_increase = 0.4 / fig_width
        actual_width_increase = final[2] - base[2]
        assert actual_width_increase == pytest.approx(expected_width_increase, rel=0.01)

        # Height should increase by vgap (0.3 on each side = 0.6 total)
        expected_height_increase = 0.6 / fig_height
        actual_height_increase = final[3] - base[3]
        assert actual_height_increase == pytest.approx(expected_height_increase, rel=0.01)

    def test_image_expansion_respects_boundaries(self):
        """IMAGE expansion doesn't go past figure edges."""
        spec = GridSpec.uniform(
            rows=1, cols=1,
            cell_width=2.0, cell_height=2.0,
            hgap=0.4, vgap=0.4,
            margins={"left": 0.0, "right": 0.0, "top": 0.0, "bottom": 0.0},
        )
        layout = GridLayout(spec)
        layout.add_cell(0, 0, axis_type=AxisType.IMAGE)

        final = layout.get_final_coordinates()[0]
        left, bottom, width, height = final

        # Should not go past boundaries
        assert left >= 0.0
        assert bottom >= 0.0
        assert left + width <= 1.0
        assert bottom + height <= 1.0

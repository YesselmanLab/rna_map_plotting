"""Tests for yplot.layout module."""

import pytest
import tempfile
from pathlib import Path

from yplot.layout import (
    SubplotLayout,
    calculate_row_spacing,
    convert_to_inches,
    expand_coordinates,
)


class TestSubplotLayout:
    """Tests for SubplotLayout class."""

    def test_init_with_config(self, simple_layout_config):
        """SubplotLayout initializes from config dict."""
        layout = SubplotLayout(config=simple_layout_config)
        assert layout.fig_size_inches == (7, 5)
        assert layout.rows == 1

    def test_init_with_yaml(self, simple_layout_config):
        """SubplotLayout initializes from YAML file."""
        import yaml
        # Convert tuple to list for YAML compatibility
        yaml_config = {
            "fig_size": list(simple_layout_config["fig_size"]),
            "margins": simple_layout_config["margins"],
            "row_1": {
                "size": list(simple_layout_config["row_1"]["size"]),
                "spacing": simple_layout_config["row_1"]["spacing"],
                "cols": simple_layout_config["row_1"]["cols"],
            },
        }
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(yaml_config, f)
            f.flush()
            layout = SubplotLayout(yaml_file=f.name)
            assert layout.fig_size_inches == (7, 5)

    def test_init_without_config_raises(self):
        """SubplotLayout raises without config or yaml_file."""
        with pytest.raises(ValueError, match="Must provide"):
            SubplotLayout()

    def test_init_missing_fig_size_raises(self):
        """SubplotLayout raises when fig_size missing."""
        with pytest.raises(ValueError, match="fig_size"):
            SubplotLayout(config={"row_1": {"cols": 2, "size": (2, 2)}})

    def test_init_missing_rows_raises(self):
        """SubplotLayout raises when no rows defined."""
        with pytest.raises(ValueError, match="row_X"):
            SubplotLayout(config={"fig_size": (7, 5)})

    def test_get_coordinates(self, simple_layout):
        """get_coordinates returns correct number of coords."""
        coords = simple_layout.get_coordinates()
        assert len(coords) == 2  # 2 columns in row_1
        assert all(len(c) == 4 for c in coords)

    def test_get_coordinates_multi_row(self, multi_row_layout_config):
        """get_coordinates handles multiple rows."""
        layout = SubplotLayout(config=multi_row_layout_config)
        coords = layout.get_coordinates()
        assert len(coords) == 4  # 2 cols * 2 rows

    def test_coordinates_are_normalized(self, simple_layout):
        """Coordinates are in figure-relative units (0-1)."""
        coords = simple_layout.get_coordinates()
        for left, bottom, width, height in coords:
            assert 0 <= left <= 1
            assert 0 <= bottom <= 1
            assert 0 < width <= 1
            assert 0 < height <= 1

    def test_get_final_coordinates(self, simple_layout):
        """get_final_coordinates returns coords."""
        coords = simple_layout.get_final_coordinates()
        assert len(coords) == 2

    def test_get_final_coordinates_with_images(self, layout_with_images):
        """get_final_coordinates expands image subplots."""
        layout = SubplotLayout(config=layout_with_images)
        regular = layout.get_coordinates()
        final = layout.get_final_coordinates()
        # First coord should be expanded (image), second should be same
        assert final[0] != regular[0]  # Expanded

    def test_to_dict(self, simple_layout, simple_layout_config):
        """to_dict returns original config."""
        result = simple_layout.to_dict()
        assert result["fig_size"] == simple_layout_config["fig_size"]

    def test_to_yaml(self, simple_layout):
        """to_yaml saves config to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.yaml"
            simple_layout.to_yaml(path)
            assert path.exists()

    def test_row_validation(self):
        """Rows must have cols and size."""
        layout = SubplotLayout(config={
            "fig_size": (7, 5),
            "row_1": {"cols": 2},  # Missing size
        })
        with pytest.raises(ValueError, match="'cols' and 'size'"):
            layout.get_coordinates()  # Validation happens when getting coords


class TestConvertToInches:
    """Tests for convert_to_inches function."""

    def test_single_coordinate(self):
        """Convert single coordinate to inches."""
        coord = (0.1, 0.2, 0.3, 0.4)
        result = convert_to_inches(coord, (10, 8))
        assert result == (1.0, 1.6, 3.0, 3.2)

    def test_multiple_coordinates(self):
        """Convert list of coordinates to inches."""
        coords = [(0.1, 0.1, 0.2, 0.2), (0.5, 0.5, 0.2, 0.2)]
        result = convert_to_inches(coords, (10, 10))
        assert len(result) == 2
        assert result[0] == (1.0, 1.0, 2.0, 2.0)
        assert result[1] == (5.0, 5.0, 2.0, 2.0)

    def test_invalid_input_raises(self):
        """Invalid input type raises ValueError."""
        with pytest.raises(ValueError):
            convert_to_inches("invalid", (10, 10))


class TestExpandCoordinates:
    """Tests for expand_coordinates function."""

    def test_single_coordinate(self):
        """Expand single coordinate."""
        coord = (0.3, 0.3, 0.4, 0.4)
        result = expand_coordinates(coord, (10, 10))
        assert result[0] < 0.3  # Left expanded
        assert result[1] < 0.3  # Bottom expanded
        assert result[2] > 0.4  # Width increased
        assert result[3] > 0.4  # Height increased

    def test_multiple_coordinates(self):
        """Expand list of coordinates."""
        coords = [(0.3, 0.3, 0.3, 0.3), (0.3, 0.3, 0.3, 0.3)]
        result = expand_coordinates(coords, (10, 10))
        assert len(result) == 2

    def test_custom_margins(self):
        """Custom margins affect expansion."""
        coord = (0.5, 0.5, 0.2, 0.2)
        small_margin = expand_coordinates(
            coord, (10, 10),
            margins={"left": 0.1, "right": 0.1, "top": 0.1, "bottom": 0.1}
        )
        large_margin = expand_coordinates(
            coord, (10, 10),
            margins={"left": 1.0, "right": 1.0, "top": 1.0, "bottom": 1.0}
        )
        assert large_margin[2] > small_margin[2]  # Larger width


class TestCalculateRowSpacing:
    """Tests for calculate_row_spacing function."""

    def test_basic_calculation(self):
        """Calculate spacing for fitting subplots."""
        spacing = calculate_row_spacing(
            fig_size_inches=(10, 6),
            num_subplots=3,
            subplot_width=2.5,
        )
        assert spacing is not None
        assert spacing > 0

    def test_single_subplot(self):
        """Single subplot needs no spacing."""
        spacing = calculate_row_spacing(
            fig_size_inches=(10, 6),
            num_subplots=1,
            subplot_width=2.5,
        )
        assert spacing == 0.0

    def test_too_many_subplots_returns_none(self):
        """Returns None when subplots don't fit."""
        spacing = calculate_row_spacing(
            fig_size_inches=(5, 6),
            num_subplots=10,
            subplot_width=2.5,
        )
        assert spacing is None

    def test_invalid_num_subplots(self):
        """Invalid num_subplots raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            calculate_row_spacing((10, 6), 0, 2.5)

    def test_invalid_subplot_width(self):
        """Invalid subplot_width raises ValueError."""
        with pytest.raises(ValueError, match="positive"):
            calculate_row_spacing((10, 6), 3, -1)

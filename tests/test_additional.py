"""Additional tests to improve coverage."""

import pytest
import numpy as np
import matplotlib.pyplot as plt

from yplot.config import rcParams
from yplot.figure.debug import (
    create_example_figure,
    draw_boxes_around_subplots,
)
from yplot.figure.image import load_and_fit_image_to_subplot
from yplot.layout import SubplotLayout
from yplot.plots.bar import plot_pop_avg_diff_from_rows
from yplot.utils.logger import setup_applevel_logger


class TestFigureDebug:
    """Additional tests for figure debug module."""

    def test_draw_boxes_around_subplots(self, simple_layout):
        """Draw boxes around multiple subplots."""
        from yplot.figure import create_figure_with_layout
        fig, axes = create_figure_with_layout(simple_layout)
        coords = simple_layout.get_final_coordinates()
        result = draw_boxes_around_subplots(fig, coords)
        assert result is fig
        assert len(fig.patches) > 0


class TestFigureImage:
    """Additional tests for image loading."""

    def test_invalid_image_path(self):
        """Invalid image path raises ValueError."""
        fig, ax = plt.subplots()
        with pytest.raises(ValueError, match="Could not load image"):
            load_and_fit_image_to_subplot("/nonexistent/path.png", ax)


class TestLayoutSubplotLayout:
    """Additional SubplotLayout tests."""

    def test_yaml_file_not_found(self):
        """Non-existent YAML file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            SubplotLayout(yaml_file="/nonexistent/file.yaml")

    def test_size_validation(self):
        """Size must be tuple/list of 2."""
        layout = SubplotLayout(config={
            "fig_size": (7, 5),
            "row_1": {"cols": 2, "size": "invalid"},
        })
        with pytest.raises(ValueError, match="size"):
            layout.get_coordinates()


class TestPlotsBar:
    """Additional bar plot tests."""

    def test_pop_avg_diff_creates_3_panels(
        self, sample_sequence, sample_structure, sample_reactivities
    ):
        """Creates 3-panel difference plot."""
        row1 = {
            "sequence": sample_sequence,
            "structure": sample_structure,
            "data": sample_reactivities,
        }
        row2 = {
            "sequence": sample_sequence,
            "structure": sample_structure,
            "data": [x + 0.1 for x in sample_reactivities],
        }
        fig = plot_pop_avg_diff_from_rows(row1, row2)
        assert len(fig.axes) == 3


class TestRcParamsRepr:
    """Test RcParams repr."""

    def test_repr(self):
        """Repr returns formatted string."""
        repr_str = repr(rcParams)
        assert "RcParams" in repr_str
        assert "font.size" in repr_str


class TestLoggerWithFile:
    """Test logger with file output."""

    def test_setup_with_file(self, tmp_path):
        """Logger can write to file."""
        log_file = tmp_path / "test.log"
        logger = setup_applevel_logger(file_name=str(log_file))
        logger.info("Test message")
        assert log_file.exists()

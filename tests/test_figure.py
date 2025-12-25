"""Tests for yplot.figure module."""

import pytest
import matplotlib.pyplot as plt

from yplot.figure import (
    add_ax_corner_text,
    add_subplot_labels,
    create_figure_with_layout,
    create_figure_with_true_size,
    draw_box_around_figure,
    draw_box_around_subplot,
    render_example_figure,
)
from yplot.layout import SubplotLayout


class TestCreateFigureWithLayout:
    """Tests for create_figure_with_layout function."""

    def test_creates_figure_and_axes(self, simple_layout):
        """Creates figure with correct number of axes."""
        fig, axes = create_figure_with_layout(simple_layout)
        assert fig is not None
        assert len(axes) == 2  # 2 columns

    def test_figure_has_correct_size(self, simple_layout):
        """Figure has correct size from layout."""
        fig, axes = create_figure_with_layout(simple_layout)
        assert fig.get_size_inches()[0] == pytest.approx(7, abs=0.01)
        assert fig.get_size_inches()[1] == pytest.approx(5, abs=0.01)


class TestCreateFigureWithTrueSize:
    """Tests for create_figure_with_true_size function."""

    def test_creates_figure(self):
        """Creates figure with specified size."""
        fig, ax = create_figure_with_true_size(4, 3)
        assert fig is not None
        assert ax is not None

    def test_axes_match_size(self):
        """Axes match specified dimensions."""
        fig, ax = create_figure_with_true_size(4, 3)
        fig.canvas.draw()
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        assert bbox.width == pytest.approx(4, abs=0.1)
        assert bbox.height == pytest.approx(3, abs=0.1)


class TestAddSubplotLabels:
    """Tests for add_subplot_labels function."""

    def test_adds_labels(self, simple_layout):
        """Adds letter labels to subplots."""
        fig, axes = create_figure_with_layout(simple_layout)
        coords = simple_layout.get_final_coordinates()
        add_subplot_labels(fig, coords)
        # Check figure has text elements
        assert len(fig.texts) == 2

    def test_starts_from_letter(self, simple_layout):
        """Starts from specified letter."""
        fig, axes = create_figure_with_layout(simple_layout)
        coords = simple_layout.get_final_coordinates()
        add_subplot_labels(fig, coords, start="C")
        labels = [t.get_text() for t in fig.texts]
        assert "C" in labels
        assert "D" in labels


class TestAddAxCornerText:
    """Tests for add_ax_corner_text function."""

    def test_adds_text(self):
        """Adds text to corner."""
        fig, ax = plt.subplots()
        add_ax_corner_text(ax, "Test", pos="upper left")
        assert len(ax.texts) == 1
        assert ax.texts[0].get_text() == "Test"

    def test_different_positions(self):
        """Works with different positions."""
        positions = ["upper left", "upper right", "lower left", "lower right"]
        for pos in positions:
            fig, ax = plt.subplots()
            add_ax_corner_text(ax, "Test", pos=pos)
            assert len(ax.texts) == 1

    def test_invalid_position_raises(self):
        """Invalid position raises ValueError."""
        fig, ax = plt.subplots()
        with pytest.raises(ValueError, match="Unknown position"):
            add_ax_corner_text(ax, "Test", pos="center")


class TestRenderExampleFigure:
    """Tests for render_example_figure function."""

    def test_renders_layout(self, simple_layout):
        """Renders example figure from layout."""
        fig = render_example_figure(simple_layout)
        assert fig is not None
        assert len(fig.axes) == 2

    def test_invalid_layout_raises(self):
        """Non-SubplotLayout raises ValueError."""
        with pytest.raises(ValueError, match="must be a SubplotLayout"):
            render_example_figure({"not": "a layout"})


class TestDrawBoxAroundFigure:
    """Tests for draw_box_around_figure function."""

    def test_adds_box(self):
        """Adds bounding box to figure."""
        fig, ax = plt.subplots()
        draw_box_around_figure(fig)
        assert len(fig.patches) == 1


class TestDrawBoxAroundSubplot:
    """Tests for draw_box_around_subplot function."""

    def test_adds_box(self):
        """Adds box around subplot coordinates."""
        fig, ax = plt.subplots()
        coords = (0.1, 0.1, 0.8, 0.8)
        draw_box_around_subplot(fig, coords)
        assert len(fig.patches) == 1

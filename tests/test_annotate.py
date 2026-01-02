"""Tests for annotation functions."""

import matplotlib.pyplot as plt
import numpy as np
import pytest

from yplot.annotate import (
    add_arrow,
    add_callout,
    add_pvalue,
    add_scale_bar,
    add_significance,
    add_text_box,
    significance_bracket,
    star_notation,
    text,
)
from yplot.annotate.stats import add_regression_stats, add_significance_bars


class TestStarNotation:
    """Tests for star notation function."""

    def test_three_stars(self):
        assert star_notation(0.0001) == "***"
        assert star_notation(0.0005) == "***"

    def test_two_stars(self):
        assert star_notation(0.005) == "**"

    def test_one_star(self):
        assert star_notation(0.03) == "*"

    def test_not_significant(self):
        assert star_notation(0.1) == "n.s."
        assert star_notation(0.5) == "n.s."


class TestSignificanceBracket:
    """Tests for significance bracket function."""

    @pytest.fixture(autouse=True)
    def setup_axes(self):
        self.fig, self.ax = plt.subplots()
        yield
        plt.close(self.fig)

    def test_draws_bracket(self):
        significance_bracket(self.ax, 0, 1, 0.9, 0.05)
        assert len(self.ax.lines) == 1


class TestAddSignificance:
    """Tests for add_significance function."""

    @pytest.fixture(autouse=True)
    def setup_axes(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_ylim(0, 1)
        yield
        plt.close(self.fig)

    def test_adds_bracket_and_text(self):
        add_significance(self.ax, 0, 1, 0.8, pvalue=0.01)
        assert len(self.ax.texts) == 1

    def test_uses_stars_by_default(self):
        add_significance(self.ax, 0, 1, 0.8, pvalue=0.0001)
        assert "***" in self.ax.texts[0].get_text()

    def test_can_show_pvalue(self):
        add_significance(self.ax, 0, 1, 0.8, pvalue=0.01, use_stars=False)
        assert "p=" in self.ax.texts[0].get_text()


class TestAddPvalue:
    """Tests for add_pvalue function."""

    @pytest.fixture(autouse=True)
    def setup_axes(self):
        self.fig, self.ax = plt.subplots()
        yield
        plt.close(self.fig)

    def test_adds_pvalue_text(self):
        add_pvalue(self.ax, 0.5, 0.5, 0.034)
        assert len(self.ax.texts) == 1
        assert "p" in self.ax.texts[0].get_text()

    def test_very_small_pvalue(self):
        add_pvalue(self.ax, 0.5, 0.5, 0.0001)
        assert "< 0.001" in self.ax.texts[0].get_text()


class TestAddSignificanceBars:
    """Tests for add_significance_bars function."""

    @pytest.fixture(autouse=True)
    def setup_axes(self):
        self.fig, self.ax = plt.subplots()
        self.ax.bar([0, 1, 2], [1, 2, 3])
        yield
        plt.close(self.fig)

    def test_adds_multiple_brackets(self):
        comparisons = [(0, 1, 0.01), (0, 2, 0.001)]
        add_significance_bars(self.ax, comparisons)
        assert len(self.ax.texts) == 2


class TestAddRegressionStats:
    """Tests for add_regression_stats function."""

    @pytest.fixture(autouse=True)
    def setup_axes(self):
        self.fig, self.ax = plt.subplots()
        yield
        plt.close(self.fig)

    def test_adds_r_squared(self):
        add_regression_stats(self.ax, r_squared=0.85)
        assert len(self.ax.texts) == 1
        assert "R²" in self.ax.texts[0].get_text()

    def test_adds_all_stats(self):
        add_regression_stats(
            self.ax, r_squared=0.85, pvalue=0.001,
            slope=1.5, intercept=0.5
        )
        text = self.ax.texts[0].get_text()
        assert "R²" in text
        assert "p" in text
        assert "y =" in text


class TestAddArrow:
    """Tests for add_arrow function."""

    @pytest.fixture(autouse=True)
    def setup_axes(self):
        self.fig, self.ax = plt.subplots()
        yield
        plt.close(self.fig)

    def test_adds_arrow(self):
        add_arrow(self.ax, 0.2, 0.8, 0.4, 0.6)
        assert len(self.ax.texts) >= 1  # annotation creates text

    def test_adds_arrow_with_text(self):
        add_arrow(self.ax, 0.2, 0.8, 0.4, 0.6, text="Test")
        texts = [t.get_text() for t in self.ax.texts]
        assert "Test" in texts


class TestAddScaleBar:
    """Tests for add_scale_bar function."""

    @pytest.fixture(autouse=True)
    def setup_axes(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        yield
        plt.close(self.fig)

    def test_adds_scale_bar(self):
        add_scale_bar(self.ax, length=10, unit="nm")
        assert len(self.ax.lines) >= 1
        assert len(self.ax.texts) >= 1

    def test_scale_bar_label(self):
        add_scale_bar(self.ax, length=10, label="10 units")
        text = self.ax.texts[-1].get_text()
        assert "10 units" in text


class TestAddCallout:
    """Tests for add_callout function."""

    @pytest.fixture(autouse=True)
    def setup_axes(self):
        self.fig, self.ax = plt.subplots()
        yield
        plt.close(self.fig)

    def test_adds_callout(self):
        add_callout(self.ax, 0.5, 0.5, "Important", 0.7, 0.8)
        assert len(self.ax.texts) >= 1
        texts = [t.get_text() for t in self.ax.texts]
        assert "Important" in texts


class TestAddTextBox:
    """Tests for add_text_box function."""

    @pytest.fixture(autouse=True)
    def setup_axes(self):
        self.fig, self.ax = plt.subplots()
        yield
        plt.close(self.fig)

    def test_adds_text_box(self):
        add_text_box(self.ax, 0.1, 0.9, "n = 100")
        assert len(self.ax.texts) == 1
        assert "n = 100" in self.ax.texts[0].get_text()

    def test_different_transforms(self):
        add_text_box(self.ax, 0.5, 0.5, "test", transform="data")
        assert len(self.ax.texts) == 1


class TestText:
    """Tests for text function."""

    @pytest.fixture(autouse=True)
    def setup_axes(self):
        self.fig, self.ax = plt.subplots()
        yield
        plt.close(self.fig)

    def test_top_left(self):
        """Text at top left position."""
        t = text(self.ax, "test", pos="top left")
        assert t.get_text() == "test"
        # Position is at anchor (0, 1), offset applied via transform
        pos = t.get_position()
        assert pos[0] == 0  # anchored at left edge
        assert pos[1] == 1  # anchored at top edge

    def test_top_right(self):
        """Text at top right position."""
        t = text(self.ax, "test", pos="top right")
        pos = t.get_position()
        assert pos[0] == 1  # anchored at right edge
        assert pos[1] == 1  # anchored at top edge

    def test_bottom_left(self):
        """Text at bottom left position."""
        t = text(self.ax, "test", pos="bottom left")
        pos = t.get_position()
        assert pos[0] == 0  # anchored at left edge
        assert pos[1] == 0  # anchored at bottom edge

    def test_bottom_right(self):
        """Text at bottom right position."""
        t = text(self.ax, "test", pos="bottom right")
        pos = t.get_position()
        assert pos[0] == 1  # anchored at right edge
        assert pos[1] == 0  # anchored at bottom edge

    def test_center(self):
        """Text at center position."""
        t = text(self.ax, "test", pos="center")
        pos = t.get_position()
        assert pos[0] == 0.5
        assert pos[1] == 0.5

    def test_aliases(self):
        """Short aliases work."""
        t1 = text(self.ax, "tl", pos="tl")
        t2 = text(self.ax, "tr", pos="tr")
        t3 = text(self.ax, "bl", pos="bl")
        t4 = text(self.ax, "br", pos="br")
        assert t1.get_position() == (0, 1)
        assert t2.get_position() == (1, 1)
        assert t3.get_position() == (0, 0)
        assert t4.get_position() == (1, 0)

    def test_above(self):
        """Text above axes."""
        t = text(self.ax, "test", pos="above")
        pos = t.get_position()
        # Anchored at top center, offset pushes it above
        assert pos[0] == 0.5
        assert pos[1] == 1  # anchor at top, offset moves it above

    def test_below(self):
        """Text below axes."""
        t = text(self.ax, "test", pos="below")
        pos = t.get_position()
        assert pos[0] == 0.5
        assert pos[1] == 0  # anchor at bottom, offset moves it below

    def test_custom_position(self):
        """Custom (x, y) tuple position."""
        t = text(self.ax, "test", pos=(0.3, 0.7))
        pos = t.get_position()
        assert abs(pos[0] - 0.3) < 0.01
        assert abs(pos[1] - 0.7) < 0.01

    def test_fontsize(self):
        """Custom fontsize."""
        t = text(self.ax, "test", pos="center", fontsize=12)
        assert t.get_fontsize() == 12

    def test_box_false_by_default(self):
        """Box is not added by default."""
        t = text(self.ax, "test", pos="center")
        assert t.get_bbox_patch() is None

    def test_box_true(self):
        """Box is added when box=True."""
        t = text(self.ax, "test", pos="center", box=True)
        assert t.get_bbox_patch() is not None

    def test_kwargs_passed_through(self):
        """Additional kwargs are passed to ax.text."""
        t = text(self.ax, "test", pos="center", color="red", fontweight="bold")
        assert t.get_color() == "red"
        assert t.get_fontweight() == "bold"

    def test_invalid_position_raises(self):
        """Invalid position raises ValueError."""
        with pytest.raises(ValueError, match="Unknown position"):
            text(self.ax, "test", pos="invalid")

    def test_custom_offset(self):
        """Custom offset changes the point-based offset."""
        # Just verify it runs without error - offset is in the transform
        t = text(self.ax, "test", pos="top left", offset=10)
        assert t.get_text() == "test"

    def test_offset_independent_of_axes_size(self):
        """Offset is in points, not relative to axes size."""
        # Create two different sized axes
        fig1, ax1 = plt.subplots(figsize=(4, 4))
        fig2, ax2 = plt.subplots(figsize=(8, 8))

        t1 = text(ax1, "test", pos="top left")
        t2 = text(ax2, "test", pos="top left")

        # Both should have same anchor position (offset is in transform)
        assert t1.get_position() == t2.get_position()

        plt.close(fig1)
        plt.close(fig2)

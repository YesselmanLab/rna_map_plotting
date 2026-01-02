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

"""Tests for yplot.plots module."""

import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from yplot.plots import (
    lollipop_plot,
    plot_pop_avg,
    plot_pop_avg_all,
    plot_pop_avg_from_row,
    plot_pop_avg_traces_all,
    plot_regression_line,
    scatter_plot_w_regression,
)


class TestScatterPlotWRegression:
    """Tests for scatter_plot_w_regression function."""

    def test_creates_scatter_plot(self):
        """Creates scatter plot with regression line."""
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([1, 2, 3, 4, 5])
        fig, ax = plt.subplots()
        scatter_plot_w_regression(x=x, y=y, ax=ax)
        # Should have scatter and regression line
        assert len(ax.collections) >= 1  # Scatter
        assert len(ax.lines) >= 1  # Regression line

    def test_with_dataframe(self):
        """Works with DataFrame input."""
        df = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [1, 2, 3, 4]})
        fig, ax = plt.subplots()
        scatter_plot_w_regression(data=df, x='x', y='y', ax=ax)
        assert len(ax.collections) >= 1

    def test_creates_new_axes_if_none(self):
        """Creates new axes if not provided."""
        x = np.array([1, 2, 3])
        y = np.array([1, 2, 3])
        ax = scatter_plot_w_regression(x=x, y=y)
        assert ax is not None


class TestPlotRegressionLine:
    """Tests for plot_regression_line function."""

    def test_adds_regression_line(self):
        """Adds regression line to axes."""
        fig, ax = plt.subplots()
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([1, 2, 3, 4, 5])
        r2 = plot_regression_line(x, y, ax)
        assert 0 <= r2 <= 1
        assert len(ax.lines) >= 1

    def test_returns_r2(self):
        """Returns R-squared value."""
        fig, ax = plt.subplots()
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([1, 2, 3, 4, 5])
        r2 = plot_regression_line(x, y, ax)
        assert r2 == pytest.approx(1.0, abs=0.01)

    def test_no_r2_annotation(self):
        """Can disable R-squared annotation."""
        fig, ax = plt.subplots()
        x = np.array([1, 2, 3, 4, 5])
        y = np.array([1, 2, 3, 4, 5])
        plot_regression_line(x, y, ax, show_r2=False)
        # Check no text annotations
        assert len(ax.texts) == 0


class TestLollipopPlot:
    """Tests for lollipop_plot function."""

    def test_creates_lollipop(self):
        """Creates lollipop plot."""
        x = [1, 2, 3, 4]
        y1 = [0.1, 0.2, 0.3, 0.4]
        y2 = [0.15, 0.25, 0.35, 0.45]
        fig, ax = plt.subplots()
        lollipop_plot(x, y1, y2, ax=ax)
        # Should have scatter collections (at least 2)
        assert len(ax.collections) >= 2

    def test_missing_y2_raises(self):
        """Missing y2 raises ValueError."""
        x = [1, 2, 3]
        y1 = [0.1, 0.2, 0.3]
        fig, ax = plt.subplots()
        with pytest.raises(ValueError, match="y2 is required"):
            lollipop_plot(x, y1, ax=ax)

    def test_creates_new_axes_if_none(self):
        """Creates new axes if not provided."""
        x = [1, 2, 3]
        y1 = [0.1, 0.2, 0.3]
        y2 = [0.2, 0.3, 0.4]
        ax = lollipop_plot(x, y1, y2)
        assert ax is not None


class TestPlotPopAvg:
    """Tests for plot_pop_avg function."""

    def test_creates_bar_plot(self, sample_sequence, sample_structure, sample_reactivities):
        """Creates bar plot for reactivities."""
        fig, ax = plt.subplots()
        plot_pop_avg(sample_sequence, sample_structure, sample_reactivities, ax=ax)
        # Should have bar containers
        assert len(ax.containers) >= 1

    def test_colors_by_nucleotide(self, sample_sequence, sample_structure, sample_reactivities):
        """Bars are colored by nucleotide identity."""
        fig, ax = plt.subplots()
        plot_pop_avg(sample_sequence, sample_structure, sample_reactivities, ax=ax)
        # Just verify no errors in coloring

    def test_creates_new_axes_if_none(self, sample_sequence, sample_structure, sample_reactivities):
        """Creates new axes if not provided."""
        ax = plot_pop_avg(sample_sequence, sample_structure, sample_reactivities)
        assert ax is not None


class TestPlotPopAvgFromRow:
    """Tests for plot_pop_avg_from_row function."""

    def test_plots_from_row_dict(self, sample_sequence, sample_structure, sample_reactivities):
        """Plots from row dictionary."""
        row = {
            "sequence": sample_sequence,
            "structure": sample_structure,
            "data": sample_reactivities,
        }
        fig, ax = plt.subplots()
        plot_pop_avg_from_row(row, ax=ax)
        assert len(ax.containers) >= 1


class TestPlotPopAvgAll:
    """Tests for plot_pop_avg_all function."""

    def test_plots_all_rows(self, sample_sequence, sample_structure, sample_reactivities):
        """Plots all rows in DataFrame."""
        df = pd.DataFrame({
            "sequence": [sample_sequence, sample_sequence],
            "structure": [sample_structure, sample_structure],
            "data": [sample_reactivities, sample_reactivities],
        })
        fig = plot_pop_avg_all(df)
        assert fig is not None


class TestPlotPopAvgTracesAll:
    """Tests for plot_pop_avg_traces_all function."""

    def test_plots_traces(self, sample_reactivities):
        """Plots overlaid traces."""
        df = pd.DataFrame({
            "data": [sample_reactivities, sample_reactivities],
            "rna_name": ["RNA1", "RNA2"],
        })
        fig, ax = plt.subplots()
        plot_pop_avg_traces_all(df, ax=ax)
        assert len(ax.lines) == 2

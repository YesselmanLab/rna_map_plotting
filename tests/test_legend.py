"""Tests for yplot.legend module."""

import pytest
import matplotlib.pyplot as plt

from yplot.legend import add_legend, add_legend_above_subplot


class TestAddLegend:
    """Tests for add_legend function."""

    def test_adds_legend(self):
        """Adds legend to axes."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], label='test')
        legend = add_legend(ax, ["Series 1", "Series 2"])
        assert legend is not None

    def test_custom_location(self):
        """Works with custom location."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], label='test')
        legend = add_legend(ax, ["Series 1"], loc="lower left")
        assert legend is not None

    def test_custom_fontsize(self):
        """Works with custom font size."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], label='test')
        legend = add_legend(ax, ["Series 1"], fontsize=12)
        assert legend is not None


class TestAddLegendAboveSubplot:
    """Tests for add_legend_above_subplot function."""

    def test_adds_legend_above(self):
        """Adds legend above subplot."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], label='test1')
        ax.plot([2, 3, 4], label='test2')
        legend = add_legend_above_subplot(ax, ["Series 1", "Series 2"])
        assert legend is not None

    def test_custom_offsets(self):
        """Works with custom offsets."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], label='test1')
        legend = add_legend_above_subplot(
            ax, ["Series 1"],
            x_offset_axes=0.5,
            y_offset_axes=0.1
        )
        assert legend is not None

    def test_figure_coords_mode(self):
        """Works with figure coordinates."""
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], label='test1')
        legend = add_legend_above_subplot(
            ax, ["Series 1"],
            use_figure_coords=True
        )
        assert legend is not None

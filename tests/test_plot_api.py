"""Tests for the DataFrame-first plotting API."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

import yplot.plot as yp
from yplot.plot.base import PlotData, extract_data, group_by_category


class TestPlotData:
    """Tests for PlotData dataclass."""

    def test_create_basic(self):
        x = np.array([1, 2, 3])
        y = np.array([4, 5, 6])
        data = PlotData(x=x, y=y)
        assert len(data.x) == 3
        assert len(data.y) == 3

    def test_optional_fields_default_none(self):
        data = PlotData(x=np.array([1]), y=np.array([1]))
        assert data.color is None
        assert data.size is None
        assert data.error is None


class TestExtractData:
    """Tests for extract_data function."""

    def test_extract_from_dataframe(self):
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        result = extract_data(df, x="a", y="b")
        np.testing.assert_array_equal(result.x, [1, 2, 3])
        np.testing.assert_array_equal(result.y, [4, 5, 6])

    def test_extract_from_arrays(self):
        result = extract_data(None, x=[1, 2, 3], y=[4, 5, 6])
        np.testing.assert_array_equal(result.x, [1, 2, 3])
        np.testing.assert_array_equal(result.y, [4, 5, 6])

    def test_extracts_labels(self):
        df = pd.DataFrame({"x_col": [1], "y_col": [2]})
        result = extract_data(df, x="x_col", y="y_col")
        assert result.labels["x"] == "x_col"
        assert result.labels["y"] == "y_col"

    def test_extract_error(self):
        df = pd.DataFrame({"x": [1], "y": [2], "err": [0.1]})
        result = extract_data(df, x="x", y="y", error="err")
        np.testing.assert_array_equal(result.error, [0.1])


class TestGroupByCategory:
    """Tests for group_by_category function."""

    def test_no_category(self):
        data = PlotData(x=np.array([1, 2]), y=np.array([3, 4]))
        groups = group_by_category(data, "color")
        assert None in groups
        assert len(groups) == 1

    def test_with_category(self):
        data = PlotData(
            x=np.array([1, 2, 3, 4]),
            y=np.array([5, 6, 7, 8]),
            color=np.array(["A", "A", "B", "B"]),
        )
        groups = group_by_category(data, "color")
        assert len(groups) == 2
        assert "A" in groups
        assert "B" in groups


class TestScatterPlot:
    """Tests for scatter plot function."""

    @pytest.fixture(autouse=True)
    def close_figs(self):
        yield
        plt.close("all")

    def test_basic_scatter(self):
        ax = yp.scatter(x=[1, 2, 3], y=[4, 5, 6])
        assert len(ax.collections) >= 1

    def test_scatter_from_dataframe(self):
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        ax = yp.scatter(df, x="x", y="y")
        assert len(ax.collections) >= 1

    def test_scatter_with_color_groups(self):
        df = pd.DataFrame({
            "x": [1, 2, 3, 4],
            "y": [5, 6, 7, 8],
            "group": ["A", "A", "B", "B"],
        })
        ax = yp.scatter(df, x="x", y="y", color="group")
        assert len(ax.collections) >= 2

    def test_scatter_with_size(self):
        ax = yp.scatter(x=[1, 2, 3], y=[4, 5, 6], size=100)
        assert len(ax.collections) >= 1


class TestLinePlot:
    """Tests for line plot function."""

    @pytest.fixture(autouse=True)
    def close_figs(self):
        yield
        plt.close("all")

    def test_basic_line(self):
        ax = yp.line(x=[1, 2, 3], y=[4, 5, 6])
        assert len(ax.lines) >= 1

    def test_line_from_dataframe(self):
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})
        ax = yp.line(df, x="x", y="y")
        assert len(ax.lines) >= 1

    def test_line_with_error(self):
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "y": [4, 5, 6],
            "err": [0.1, 0.2, 0.3],
        })
        ax = yp.line(df, x="x", y="y", error="err")
        assert len(ax.lines) >= 1
        assert len(ax.collections) >= 1  # fill_between creates collection

    def test_line_with_group(self):
        df = pd.DataFrame({
            "x": [1, 2, 3, 1, 2, 3],
            "y": [4, 5, 6, 7, 8, 9],
            "group": ["A", "A", "A", "B", "B", "B"],
        })
        ax = yp.line(df, x="x", y="y", group="group")
        assert len(ax.lines) >= 2


class TestBarPlot:
    """Tests for bar plot function."""

    @pytest.fixture(autouse=True)
    def close_figs(self):
        yield
        plt.close("all")

    def test_basic_bar(self):
        ax = yp.bar(x=["A", "B", "C"], y=[1, 2, 3])
        assert len(ax.patches) == 3

    def test_bar_from_dataframe(self):
        df = pd.DataFrame({"cat": ["A", "B", "C"], "val": [1, 2, 3]})
        ax = yp.bar(df, x="cat", y="val")
        assert len(ax.patches) == 3

    def test_bar_with_error(self):
        df = pd.DataFrame({
            "cat": ["A", "B"],
            "val": [1, 2],
            "err": [0.1, 0.2],
        })
        ax = yp.bar(df, x="cat", y="val", error="err")
        assert len(ax.patches) == 2

    def test_grouped_bar(self):
        df = pd.DataFrame({
            "cat": ["A", "A", "B", "B"],
            "val": [1, 2, 3, 4],
            "group": ["X", "Y", "X", "Y"],
        })
        ax = yp.grouped_bar(df, x="cat", y="val", group="group")
        assert len(ax.patches) == 4


class TestDistributionPlots:
    """Tests for distribution plots."""

    @pytest.fixture(autouse=True)
    def close_figs(self):
        yield
        plt.close("all")

    @pytest.fixture
    def sample_df(self):
        np.random.seed(42)
        return pd.DataFrame({
            "group": ["A"] * 20 + ["B"] * 20,
            "value": np.concatenate([
                np.random.normal(0, 1, 20),
                np.random.normal(1, 1, 20),
            ]),
        })

    def test_violin(self, sample_df):
        ax = yp.violin(sample_df, x="group", y="value")
        assert ax is not None

    def test_box(self, sample_df):
        ax = yp.box(sample_df, x="group", y="value")
        assert len(ax.patches) >= 2

    def test_swarm(self, sample_df):
        ax = yp.swarm(sample_df, x="group", y="value")
        assert len(ax.collections) >= 2

    def test_strip(self, sample_df):
        ax = yp.strip(sample_df, x="group", y="value")
        assert len(ax.collections) >= 2


class TestHeatmap:
    """Tests for heatmap function."""

    @pytest.fixture(autouse=True)
    def close_figs(self):
        yield
        plt.close("all")

    def test_heatmap_from_array(self):
        data = np.array([[1, 2], [3, 4]])
        ax = yp.heatmap(data)
        assert ax is not None

    def test_heatmap_from_dataframe(self):
        df = pd.DataFrame(
            [[1, 2], [3, 4]],
            index=["A", "B"],
            columns=["X", "Y"],
        )
        ax = yp.heatmap(df)
        assert ax is not None

    def test_heatmap_with_annotations(self):
        data = np.array([[1, 2], [3, 4]])
        ax = yp.heatmap(data, annot=True)
        assert len(ax.texts) == 4

    def test_heatmap_pivot(self):
        df = pd.DataFrame({
            "x": ["A", "A", "B", "B"],
            "y": ["X", "Y", "X", "Y"],
            "value": [1, 2, 3, 4],
        })
        ax = yp.heatmap(df, x="x", y="y", values="value")
        assert ax is not None

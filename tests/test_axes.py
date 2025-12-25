"""Tests for yplot.axes module."""

import pytest
import numpy as np
import matplotlib.pyplot as plt

from yplot.axes import (
    add_custom_ticks,
    apply_x_axis_by_name,
    compute_eps_and_transform,
    log_axis_with_zero,
    sequence_and_structure_x_axis,
    sequence_x_axis,
    set_tick_params,
    structure_x_axis,
)


class TestSequenceXAxis:
    """Tests for sequence_x_axis function."""

    def test_sets_xticks(self, sample_sequence):
        """Sets x-ticks for each nucleotide."""
        fig, ax = plt.subplots()
        sequence_x_axis(ax, sample_sequence)
        ticks = ax.get_xticks()
        assert len(ticks) == len(sample_sequence)

    def test_sets_labels(self, sample_sequence):
        """Sets tick labels to nucleotides."""
        fig, ax = plt.subplots()
        sequence_x_axis(ax, sample_sequence)
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == list(sample_sequence)

    def test_sets_xlim(self, sample_sequence):
        """Sets x-limits with padding."""
        fig, ax = plt.subplots()
        sequence_x_axis(ax, sample_sequence, x_delta=2)
        xlim = ax.get_xlim()
        assert xlim[0] == -2
        assert xlim[1] == len(sample_sequence) - 1 + 2


class TestStructureXAxis:
    """Tests for structure_x_axis function."""

    def test_sets_structure_labels(self, sample_structure):
        """Sets tick labels to structure characters."""
        fig, ax = plt.subplots()
        structure_x_axis(ax, sample_structure)
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == list(sample_structure)


class TestSequenceAndStructureXAxis:
    """Tests for sequence_and_structure_x_axis function."""

    def test_combines_sequence_and_structure(self, sample_sequence, sample_structure):
        """Creates combined labels with sequence and structure."""
        fig, ax = plt.subplots()
        sequence_and_structure_x_axis(ax, sample_sequence, sample_structure)
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert len(labels) == len(sample_sequence)
        # Each label should contain newline
        assert "\n" in labels[0]


class TestApplyXAxisByName:
    """Tests for apply_x_axis_by_name function."""

    def test_sequence_type(self, sample_sequence, sample_structure):
        """Applies sequence axis type."""
        fig, ax = plt.subplots()
        apply_x_axis_by_name(ax, sample_sequence, sample_structure, "sequence")
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == list(sample_sequence)

    def test_structure_type(self, sample_sequence, sample_structure):
        """Applies structure axis type."""
        fig, ax = plt.subplots()
        apply_x_axis_by_name(ax, sample_sequence, sample_structure, "structure")
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == list(sample_structure)

    def test_sequence_structure_type(self, sample_sequence, sample_structure):
        """Applies sequence_structure axis type."""
        fig, ax = plt.subplots()
        apply_x_axis_by_name(ax, sample_sequence, sample_structure, "sequence_structure")
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert "\n" in labels[0]

    def test_invalid_type_raises(self, sample_sequence, sample_structure):
        """Invalid axis type raises ValueError."""
        fig, ax = plt.subplots()
        with pytest.raises(ValueError, match="Unknown axis_type"):
            apply_x_axis_by_name(ax, sample_sequence, sample_structure, "invalid")


class TestAddCustomTicks:
    """Tests for add_custom_ticks function."""

    def test_x_axis_ticks(self):
        """Adds custom ticks to x-axis."""
        fig, ax = plt.subplots()
        add_custom_ticks(ax, "x", 0.0, 1.0, 5)
        ticks = ax.get_xticks()
        assert len(ticks) == 5
        assert ticks[0] == pytest.approx(0.0)
        assert ticks[-1] == pytest.approx(1.0)

    def test_y_axis_ticks(self):
        """Adds custom ticks to y-axis."""
        fig, ax = plt.subplots()
        add_custom_ticks(ax, "y", 0.0, 2.0, 5)
        ticks = ax.get_yticks()
        assert len(ticks) == 5

    def test_invalid_num_ticks(self):
        """num_ticks < 2 raises ValueError."""
        fig, ax = plt.subplots()
        with pytest.raises(ValueError, match="at least 2"):
            add_custom_ticks(ax, "x", 0, 1, 1)

    def test_invalid_axis(self):
        """Invalid axis raises ValueError."""
        fig, ax = plt.subplots()
        with pytest.raises(ValueError, match="must be"):
            add_custom_ticks(ax, "z", 0, 1, 5)


class TestSetTickParams:
    """Tests for set_tick_params function."""

    def test_sets_tick_params(self):
        """Sets tick parameters on axes."""
        fig, ax = plt.subplots()
        set_tick_params(ax, width=2.0, size=5.0)
        # Just verify no errors - matplotlib doesn't expose these easily


class TestComputeEpsAndTransform:
    """Tests for compute_eps_and_transform function."""

    def test_basic_transform(self):
        """Transforms data with zeros."""
        x = np.array([0, 0.1, 1, 10])
        eps, pos, x_plot = compute_eps_and_transform(x)
        assert eps > 0
        assert eps < 0.1
        assert len(pos) == 3  # Only positive values
        assert x_plot[0] == eps  # Zero replaced with eps

    def test_all_zeros_raises(self):
        """All zeros raises ValueError."""
        x = np.array([0, 0, 0])
        with pytest.raises(ValueError, match="All x values are zero"):
            compute_eps_and_transform(x)

    def test_custom_epsilon_factor(self):
        """Custom epsilon factor affects eps."""
        x = np.array([0, 1, 10])
        eps1, _, _ = compute_eps_and_transform(x, epsilon_factor=0.1)
        eps2, _, _ = compute_eps_and_transform(x, epsilon_factor=0.01)
        assert eps2 < eps1


class TestLogAxisWithZero:
    """Tests for log_axis_with_zero function."""

    def test_sets_log_scale(self):
        """Sets x-axis to log scale."""
        fig, ax = plt.subplots()
        x = np.array([0, 0.1, 1, 10])
        eps, pos, x_plot = compute_eps_and_transform(x)
        ax.scatter(x_plot, [1, 2, 3, 4])
        log_axis_with_zero(ax, eps, pos)
        assert ax.get_xscale() == "log"

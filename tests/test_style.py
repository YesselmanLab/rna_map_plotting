"""Tests for yplot.style module."""

import pytest
import matplotlib.pyplot as plt

from yplot.config import rcParams
from yplot.style import (
    PRESETS,
    apply_style_to_figure,
    get_preset,
    list_presets,
    publication_style_ax,
    use,
)


class TestPublicationStyleAx:
    """Tests for publication_style_ax function."""

    def test_applies_default_style(self):
        """Applies styling with default rcParams values."""
        fig, ax = plt.subplots()
        publication_style_ax(ax)
        # Check spine linewidth
        for spine in ax.spines.values():
            assert spine.get_linewidth() == rcParams["axes.linewidth"]

    def test_custom_font_size(self):
        """Custom font size overrides default."""
        fig, ax = plt.subplots()
        publication_style_ax(ax, fsize=14)
        assert ax.xaxis.label.get_fontsize() == 14

    def test_custom_tick_sizes(self):
        """Custom tick sizes override defaults."""
        fig, ax = plt.subplots()
        publication_style_ax(ax, xtick_size=10, ytick_size=12)
        # Note: Tick labels need text to test size
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        fig.canvas.draw()


class TestApplyStyleToFigure:
    """Tests for apply_style_to_figure function."""

    def test_applies_to_all_axes(self):
        """Applies style to all axes in figure."""
        fig, axes = plt.subplots(2, 2)
        apply_style_to_figure(fig)
        for ax in axes.flat:
            for spine in ax.spines.values():
                assert spine.get_linewidth() == rcParams["axes.linewidth"]


class TestUse:
    """Tests for use function."""

    def test_apply_publication_preset(self):
        """Applying publication preset updates rcParams."""
        use("publication")
        assert rcParams["font.size"] == PRESETS["publication"]["font.size"]

    def test_apply_presentation_preset(self):
        """Applying presentation preset updates rcParams."""
        use("presentation")
        assert rcParams["font.size"] == PRESETS["presentation"]["font.size"]

    def test_apply_poster_preset(self):
        """Applying poster preset updates rcParams."""
        use("poster")
        assert rcParams["font.size"] == PRESETS["poster"]["font.size"]

    def test_invalid_preset_raises(self):
        """Invalid preset name raises ValueError."""
        with pytest.raises(ValueError, match="Unknown style"):
            use("invalid_preset")


class TestListPresets:
    """Tests for list_presets function."""

    def test_returns_preset_names(self):
        """Returns list of preset names."""
        presets = list_presets()
        assert "publication" in presets
        assert "presentation" in presets
        assert "poster" in presets


class TestGetPreset:
    """Tests for get_preset function."""

    def test_returns_preset_dict(self):
        """Returns copy of preset configuration."""
        preset = get_preset("publication")
        assert "font.size" in preset
        assert preset["font.size"] == PRESETS["publication"]["font.size"]

    def test_returns_copy(self):
        """Returned dict is independent copy."""
        preset = get_preset("publication")
        preset["font.size"] = 999
        assert PRESETS["publication"]["font.size"] != 999

    def test_invalid_preset_raises(self):
        """Invalid preset name raises ValueError."""
        with pytest.raises(ValueError, match="Unknown preset"):
            get_preset("invalid")

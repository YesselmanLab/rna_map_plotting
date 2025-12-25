"""Tests for backward compatibility with existing code."""

import pytest


class TestBackwardCompatibleImports:
    """Verify all backward-compatible imports work."""

    def test_import_yplot(self):
        """Can import yplot."""
        import yplot
        assert yplot.__version__

    def test_import_rcparams(self):
        """Can import rcParams."""
        from yplot import rcParams
        assert rcParams is not None

    def test_import_rc_context(self):
        """Can import rc_context."""
        from yplot import rc_context
        assert rc_context is not None

    def test_import_use(self):
        """Can import use function."""
        from yplot import use
        assert callable(use)

    def test_import_subplot_layout(self):
        """Can import SubplotLayout."""
        from yplot import SubplotLayout
        assert SubplotLayout is not None

    def test_import_publication_style_ax(self):
        """Can import publication_style_ax."""
        from yplot import publication_style_ax
        assert callable(publication_style_ax)

    def test_import_create_figure_with_layout(self):
        """Can import create_figure_with_layout."""
        from yplot import create_figure_with_layout
        assert callable(create_figure_with_layout)

    def test_import_scatter_plot_w_regression(self):
        """Can import scatter_plot_w_regression."""
        from yplot import scatter_plot_w_regression
        assert callable(scatter_plot_w_regression)

    def test_import_lollipop_plot(self):
        """Can import lollipop_plot."""
        from yplot import lollipop_plot
        assert callable(lollipop_plot)

    def test_import_add_subplot_labels(self):
        """Can import add_subplot_labels."""
        from yplot import add_subplot_labels
        assert callable(add_subplot_labels)

    def test_import_add_legend(self):
        """Can import add_legend."""
        from yplot import add_legend
        assert callable(add_legend)

    def test_import_sequence_x_axis(self):
        """Can import sequence_x_axis."""
        from yplot import sequence_x_axis
        assert callable(sequence_x_axis)

    def test_import_colors_for_sequence(self):
        """Can import colors_for_sequence."""
        from yplot import colors_for_sequence
        assert callable(colors_for_sequence)

    def test_import_render_example_figure(self):
        """Can import render_example_figure."""
        from yplot import render_example_figure
        assert callable(render_example_figure)

    def test_import_load_and_fit_image_to_subplot(self):
        """Can import load_and_fit_image_to_subplot."""
        from yplot import load_and_fit_image_to_subplot
        assert callable(load_and_fit_image_to_subplot)

    def test_import_draw_box_around_figure(self):
        """Can import draw_box_around_figure."""
        from yplot import draw_box_around_figure
        assert callable(draw_box_around_figure)

    def test_import_add_custom_ticks(self):
        """Can import add_custom_ticks."""
        from yplot import add_custom_ticks
        assert callable(add_custom_ticks)


class TestBackwardCompatibleAliases:
    """Test backward compatibility aliases."""

    def test_expand_subplot_coordinates_alias(self):
        """expand_subplot_coordinates alias works."""
        from yplot import expand_subplot_coordinates
        from yplot.layout import expand_coordinates
        assert expand_subplot_coordinates is expand_coordinates

    def test_convert_coordinates_to_inches_alias(self):
        """convert_coordinates_to_inches alias works."""
        from yplot import convert_coordinates_to_inches
        from yplot.layout import convert_to_inches
        assert convert_coordinates_to_inches is convert_to_inches

    def test_compute_eps_and_xplot_alias(self):
        """compute_eps_and_xplot alias works."""
        from yplot import compute_eps_and_xplot
        from yplot.axes import compute_eps_and_transform
        assert compute_eps_and_xplot is compute_eps_and_transform


class TestSubplotLayoutBackwardCompat:
    """Test SubplotLayout backward compatibility."""

    def test_config_dict_format(self):
        """Old config dict format still works."""
        from yplot import SubplotLayout

        config = {
            "fig_size": (7, 5),
            "margins": {"left": 0.5, "right": 0.1, "top": 0.1, "bottom": 0.5},
            "row_1": {
                "size": (3.0, 2.0),
                "spacing": {"hspace": 0.5, "wspace": 0.3},
                "cols": 2,
            },
        }
        layout = SubplotLayout(config=config)
        assert layout.fig_size_inches == (7, 5)

    def test_get_coordinates_method(self):
        """get_coordinates method works."""
        from yplot import SubplotLayout

        config = {
            "fig_size": (7, 5),
            "row_1": {"size": (3.0, 2.0), "cols": 2},
        }
        layout = SubplotLayout(config=config)
        coords = layout.get_coordinates()
        assert len(coords) == 2

    def test_get_final_coordinates_method(self):
        """get_final_coordinates method works."""
        from yplot import SubplotLayout

        config = {
            "fig_size": (7, 5),
            "row_1": {"size": (3.0, 2.0), "cols": 2},
        }
        layout = SubplotLayout(config=config)
        coords = layout.get_final_coordinates()
        assert len(coords) == 2

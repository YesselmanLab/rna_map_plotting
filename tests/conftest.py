"""Pytest fixtures for yplot tests."""

import pytest
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for testing

import matplotlib.pyplot as plt

from yplot.config import rcParams
from yplot.layout import SubplotLayout


@pytest.fixture(autouse=True)
def reset_rcparams():
    """Reset rcParams to defaults before each test."""
    rcParams.reset()
    yield
    rcParams.reset()


@pytest.fixture(autouse=True)
def close_figures():
    """Close all matplotlib figures after each test."""
    yield
    plt.close('all')


@pytest.fixture
def simple_layout_config():
    """Simple layout configuration for testing."""
    return {
        "fig_size": (7, 5),
        "margins": {"left": 0.5, "right": 0.1, "top": 0.1, "bottom": 0.5},
        "row_1": {
            "size": (3.0, 2.0),
            "spacing": {"hspace": 0.5, "wspace": 0.3},
            "cols": 2,
        },
    }


@pytest.fixture
def multi_row_layout_config():
    """Multi-row layout configuration for testing."""
    return {
        "fig_size": (7, 8),
        "margins": {"left": 0.4, "right": 0.0, "top": 0.0, "bottom": 0.3},
        "row_1": {
            "size": (2.9, 2.5),
            "spacing": {"hspace": 0.70, "wspace": 0.40},
            "cols": 2,
        },
        "row_2": {
            "size": (2.9, 1.2),
            "spacing": {"hspace": 0.70, "wspace": 0.40},
            "cols": 2,
        },
    }


@pytest.fixture
def layout_with_images():
    """Layout with image subplots for testing."""
    return {
        "fig_size": (7, 8),
        "margins": {"left": 0.4, "right": 0.0, "top": 0.0, "bottom": 0.3},
        "row_1": {
            "size": (2.9, 2.5),
            "spacing": {"hspace": 0.70, "wspace": 0.40},
            "cols": 2,
            "image": [0],
        },
        "row_2": {
            "size": (2.9, 1.2),
            "spacing": {"hspace": 0.70, "wspace": 0.40},
            "cols": 2,
        },
    }


@pytest.fixture
def simple_layout(simple_layout_config):
    """SubplotLayout instance for testing."""
    return SubplotLayout(config=simple_layout_config)


@pytest.fixture
def sample_sequence():
    """Sample RNA sequence for testing."""
    return "ACGU"


@pytest.fixture
def sample_structure():
    """Sample secondary structure for testing."""
    return "(..)"


@pytest.fixture
def sample_reactivities():
    """Sample reactivity values for testing."""
    return [0.1, 0.2, 0.3, 0.4]

"""Tests for yplot.utils module."""

import pytest
import logging

from yplot.utils import (
    APP_LOGGER_NAME,
    COLOR_MAPPING,
    colors_for_sequence,
    get_logger,
    setup_applevel_logger,
)


class TestColorsForSequence:
    """Tests for colors_for_sequence function."""

    def test_basic_sequence(self):
        """Returns correct colors for basic sequence."""
        colors = colors_for_sequence("ACGU")
        assert colors == ["red", "blue", "orange", "green"]

    def test_dna_sequence(self):
        """Works with DNA (T instead of U)."""
        colors = colors_for_sequence("ACGT")
        assert colors == ["red", "blue", "orange", "green"]

    def test_lowercase(self):
        """Handles lowercase sequences."""
        colors = colors_for_sequence("acgu")
        assert colors == ["red", "blue", "orange", "green"]

    def test_ampersand(self):
        """Handles ampersand character."""
        colors = colors_for_sequence("A&C")
        assert colors == ["red", "gray", "blue"]

    def test_invalid_character_raises(self):
        """Invalid character raises ValueError."""
        with pytest.raises(ValueError, match="Invalid character"):
            colors_for_sequence("ACGX")

    def test_empty_sequence(self):
        """Empty sequence returns empty list."""
        colors = colors_for_sequence("")
        assert colors == []


class TestColorMapping:
    """Tests for COLOR_MAPPING constant."""

    def test_has_all_nucleotides(self):
        """Contains all standard nucleotides."""
        assert "A" in COLOR_MAPPING
        assert "C" in COLOR_MAPPING
        assert "G" in COLOR_MAPPING
        assert "T" in COLOR_MAPPING
        assert "U" in COLOR_MAPPING


class TestLogger:
    """Tests for logger functions."""

    def test_get_logger(self):
        """get_logger returns child logger."""
        logger = get_logger("test_module")
        assert logger.name == f"{APP_LOGGER_NAME}.test_module"

    def test_setup_applevel_logger(self):
        """setup_applevel_logger creates logger."""
        logger = setup_applevel_logger(is_debug=True)
        assert logger.level == logging.DEBUG

    def test_logger_info_level(self):
        """Default logger is INFO level."""
        logger = setup_applevel_logger(is_debug=False)
        assert logger.level == logging.INFO

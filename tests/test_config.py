"""Tests for yplot.config module."""

import pytest

from yplot.config import (
    DEFAULT_PARAMS,
    RcParams,
    get_default,
    list_keys,
    rc_context,
    rcParams,
)


class TestRcParams:
    """Tests for RcParams class."""

    def test_initialization_with_defaults(self):
        """RcParams initializes with default values."""
        params = RcParams()
        assert len(params) == len(DEFAULT_PARAMS)
        assert params["font.size"] == DEFAULT_PARAMS["font.size"]

    def test_get_valid_key(self):
        """Getting a valid key returns correct value."""
        assert rcParams["font.family"] == "Arial"
        assert rcParams["axes.linewidth"] == 0.75

    def test_get_invalid_key_raises(self):
        """Getting an invalid key raises KeyError."""
        with pytest.raises(KeyError, match="not a valid yplot"):
            _ = rcParams["invalid.key"]

    def test_set_valid_key(self):
        """Setting a valid key works correctly."""
        rcParams["font.size"] = 12
        assert rcParams["font.size"] == 12

    def test_set_invalid_key_raises(self):
        """Setting an invalid key raises KeyError."""
        with pytest.raises(KeyError, match="not a valid yplot"):
            rcParams["invalid.key"] = 10

    def test_reset_single_key(self):
        """Reset restores a single key to default."""
        original = rcParams["font.size"]
        rcParams["font.size"] = 99
        rcParams.reset("font.size")
        assert rcParams["font.size"] == original

    def test_reset_all_keys(self):
        """Reset restores all keys to defaults."""
        rcParams["font.size"] = 99
        rcParams["axes.linewidth"] = 99
        rcParams.reset()
        assert rcParams["font.size"] == DEFAULT_PARAMS["font.size"]
        assert rcParams["axes.linewidth"] == DEFAULT_PARAMS["axes.linewidth"]

    def test_update_from_dict(self):
        """Update from dict sets multiple values."""
        rcParams.update_from_dict({"font.size": 14, "axes.linewidth": 2.0})
        assert rcParams["font.size"] == 14
        assert rcParams["axes.linewidth"] == 2.0

    def test_copy(self):
        """Copy creates independent instance."""
        rcParams["font.size"] = 20
        copied = rcParams.copy()
        rcParams["font.size"] = 30
        assert copied["font.size"] == 20

    def test_find_all(self):
        """Find all returns matching keys."""
        font_params = rcParams.find_all("font")
        assert "font.size" in font_params
        assert "font.family" in font_params
        assert "axes.linewidth" not in font_params

    def test_iteration(self):
        """Iteration yields sorted keys."""
        keys = list(rcParams)
        assert keys == sorted(keys)


class TestRcContext:
    """Tests for rc_context context manager."""

    def test_temporary_changes(self):
        """Context manager applies temporary changes."""
        original = rcParams["font.size"]
        with rc_context({"font.size": 20}):
            assert rcParams["font.size"] == 20
        assert rcParams["font.size"] == original

    def test_restores_on_exception(self):
        """Context manager restores values on exception."""
        original = rcParams["font.size"]
        try:
            with rc_context({"font.size": 20}):
                raise ValueError("test")
        except ValueError:
            pass
        assert rcParams["font.size"] == original

    def test_empty_context(self):
        """Empty context doesn't modify values."""
        original = rcParams["font.size"]
        with rc_context():
            assert rcParams["font.size"] == original


class TestDefaults:
    """Tests for defaults module functions."""

    def test_get_default_valid_key(self):
        """get_default returns correct value for valid key."""
        assert get_default("font.size") == 8

    def test_get_default_invalid_key(self):
        """get_default raises for invalid key."""
        with pytest.raises(KeyError, match="Unknown configuration"):
            get_default("invalid.key")

    def test_list_keys(self):
        """list_keys returns all configuration keys."""
        keys = list_keys()
        assert "font.size" in keys
        assert "axes.linewidth" in keys
        assert len(keys) == len(DEFAULT_PARAMS)

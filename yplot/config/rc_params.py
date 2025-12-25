"""
RcParams class for matplotlib-style configuration management.

This module provides a dictionary-like configuration object that validates
keys and allows global style customization for yplot.
"""

from collections.abc import Iterator
from typing import Any, Optional

from yplot.config.defaults import DEFAULT_PARAMS


class RcParams(dict):
    """
    Dictionary-like object for yplot configuration parameters.

    Similar to matplotlib's rcParams, this class provides validated access
    to configuration values with support for dot-notation keys.

    Example:
        >>> from yplot import rcParams
        >>> rcParams['font.size'] = 10
        >>> rcParams['axes.linewidth'] = 1.0
    """

    def __init__(self, defaults: Optional[dict[str, Any]] = None) -> None:
        """
        Initialize RcParams with default values.

        Args:
            defaults: Optional dictionary of default values.
                     If None, uses DEFAULT_PARAMS.
        """
        super().__init__()
        source = defaults if defaults is not None else DEFAULT_PARAMS
        for key, value in source.items():
            dict.__setitem__(self, key, value)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set a configuration value with validation.

        Args:
            key: Configuration key (must exist in defaults).
            value: New value to set.

        Raises:
            KeyError: If key is not a valid configuration parameter.
        """
        if key not in DEFAULT_PARAMS:
            raise KeyError(
                f"'{key}' is not a valid yplot configuration key. "
                f"Use rcParams.keys() to see available keys."
            )
        dict.__setitem__(self, key, value)

    def __getitem__(self, key: str) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key to retrieve.

        Returns:
            The current value for the key.

        Raises:
            KeyError: If key is not a valid configuration parameter.
        """
        if key not in DEFAULT_PARAMS:
            raise KeyError(
                f"'{key}' is not a valid yplot configuration key. "
                f"Use rcParams.keys() to see available keys."
            )
        return dict.__getitem__(self, key)

    def reset(self, key: Optional[str] = None) -> None:
        """
        Reset configuration to defaults.

        Args:
            key: Specific key to reset. If None, resets all keys.
        """
        if key is not None:
            if key not in DEFAULT_PARAMS:
                raise KeyError(f"'{key}' is not a valid configuration key.")
            dict.__setitem__(self, key, DEFAULT_PARAMS[key])
        else:
            for k, v in DEFAULT_PARAMS.items():
                dict.__setitem__(self, k, v)

    def update_from_dict(self, params: dict[str, Any]) -> None:
        """
        Update multiple parameters from a dictionary.

        Args:
            params: Dictionary of key-value pairs to update.

        Raises:
            KeyError: If any key is not valid.
        """
        for key, value in params.items():
            self[key] = value

    def copy(self) -> "RcParams":
        """
        Create a copy of the current configuration.

        Returns:
            New RcParams instance with same values.
        """
        new_params = RcParams.__new__(RcParams)
        dict.__init__(new_params)
        for key, value in self.items():
            dict.__setitem__(new_params, key, value)
        return new_params

    def find_all(self, pattern: str) -> dict[str, Any]:
        """
        Find all keys matching a pattern prefix.

        Args:
            pattern: Prefix to match (e.g., 'font' matches 'font.size').

        Returns:
            Dictionary of matching key-value pairs.
        """
        return {k: v for k, v in self.items() if k.startswith(pattern)}

    def __repr__(self) -> str:
        """Return a formatted string representation."""
        lines = [f"RcParams({len(self)} parameters):"]
        for key in sorted(self.keys()):
            lines.append(f"  {key}: {self[key]!r}")
        return "\n".join(lines)

    def __iter__(self) -> Iterator[str]:
        """Iterate over sorted keys."""
        return iter(sorted(dict.keys(self)))


# Global instance
rcParams = RcParams()

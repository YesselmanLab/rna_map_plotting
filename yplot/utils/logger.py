"""
Logging utilities for yplot.

This module provides logging setup and configuration for the library.
"""

import logging
import sys
from typing import Optional

APP_LOGGER_NAME = "yplot"


def setup_applevel_logger(
    logger_name: str = APP_LOGGER_NAME,
    is_debug: bool = False,
    file_name: Optional[str] = None,
) -> logging.Logger:
    """
    Set up the application logger.

    Args:
        logger_name: Name of the logger.
        is_debug: If True, set level to DEBUG; otherwise INFO.
        file_name: Optional file path for log output.

    Returns:
        Configured Logger instance.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if is_debug else logging.INFO)

    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(handler)

    if file_name:
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(module_name: str) -> logging.Logger:
    """
    Get a logger for a specific module.

    Args:
        module_name: Name of the module.

    Returns:
        Logger object for the module.
    """
    return logging.getLogger(APP_LOGGER_NAME).getChild(module_name)

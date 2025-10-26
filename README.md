# yplot

A Python library for flexible subplot layout customization with per-row and per-column sizing, spacing, and margins.

## Features

- **Flexible subplot layouts** with exact size control
- **Per-row and per-column customization** for different subplot sizes
- **Variable spacing** between rows and columns
- **Backward compatibility** with uniform layouts
- **Mixed specifications** combining uniform and per-row settings

## Install

To install yplot:

```shell
python -m pip install git+https://github.com/jyesselm/yplot
```

## Quick Start

```python
from yplot.figure import calculate_subplot_coordinates

# Uniform layout (backward compatible)
coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 5),
    subplot_layout=(2, 3),
    subplot_size_inches=(1.8, 1.8),
    spacing={'hspace': 0.3, 'wspace': 0.3, 'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}}
)

# Per-row customization
coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 6),
    subplot_layout=(3, 2),
    subplot_size_inches={'row_heights': [2.0, 1.5, 1.0], 'col_widths': [2.0, 2.0]},
    spacing={'hspace': [0.3], 'wspace': [0.3, 0.3], 'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}}
)
```

## Documentation

For comprehensive examples and API reference, see:

- **[Per-Row Subplot Customization Examples](docs/per_row_subplot_examples.md)** - Detailed examples showing different layout configurations, command code, and resulting figures
- **[Figure Layout Examples](notebooks/figure.ipynb)** - Jupyter notebook demonstrating figure layout capabilities
- **[Legend Examples](notebooks/legend.ipynb)** - Jupyter notebook showing legend customization options

## TODO

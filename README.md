# yplot

A Python library for flexible subplot layout customization with per-row and per-column sizing, spacing, and margins.

## Features

- **Unified SubplotLayout system** with class, dictionary, and YAML configuration support
- **Flexible subplot layouts** with exact size control
- **Per-row and per-column customization** for different subplot sizes
- **Variable spacing** between rows and columns
- **YAML file support** for easy configuration management
- **Backward compatibility** with uniform layouts
- **Mixed specifications** combining uniform and per-row settings

## Install

To install yplot:

```shell
python -m pip install git+https://github.com/jyesselm/yplot
```

## Quick Start

### New SubplotLayout System (Recommended)

```python
from yplot.figure import SubplotLayout
from yplot.plotting import create_figure_with_layout

# Create layout object
layout = SubplotLayout(fig_size_inches=(10, 8), rows=2, cols=3)
layout.row_heights = [3.0, 2.0]
layout.col_widths = [2.5, 2.5, 2.5]
layout.set_uniform_wspace(0.5)
layout.set_uniform_hspace(0.3)

# Create figure
fig, axes = create_figure_with_layout(layout)
```

### YAML Configuration

```yaml
# layout.yaml
fig_size: [10, 8]
rows: 2
cols: 3
row_heights: [3.0, 2.0]
col_widths: [2.5, 2.5, 2.5]
wspace: [0.5]
hspace: [0.3, 0.3]
margins:
  left: 0.75
  right: 0.75
  top: 0.75
  bottom: 0.75
```

```python
# Load from YAML
fig, axes = create_figure_with_layout('layout.yaml')
```

### Legacy Interface (Still Supported)

```python
from yplot.figure import calculate_subplot_coordinates

# Uniform layout (backward compatible)
coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 5),
    subplot_layout=(2, 3),
    subplot_size_inches=(1.8, 1.8),
    spacing={'hspace': 0.3, 'wspace': 0.3, 'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}}
)
```

## Documentation

For comprehensive examples and API reference, see:

- **[Main Documentation](docs/README.md)** - Complete guide with examples, API reference, and migration guide
- **[SubplotLayout Guide](docs/subplot_layout_guide.md)** - Focused guide to the SubplotLayout system with YAML support
- **[Expand Subplot Coordinates](docs/expand_subplot_coordinates.md)** - Guide for coordinate expansion and figure insertion
- **[Figure Layout Examples](notebooks/figure.ipynb)** - Jupyter notebook demonstrating figure layout capabilities
- **[Legend Examples](notebooks/legend.ipynb)** - Jupyter notebook showing legend customization options
- **[SubplotLayout Examples](examples/subplot_layout_example.py)** - Comprehensive example script demonstrating all features
- **[Expand Coordinates Examples](examples/expand_coordinates_example.py)** - Examples for coordinate expansion functionality

## TODO

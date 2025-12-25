# SubplotLayout Guide

This guide explains how to use the `SubplotLayout` system in yplot, which provides a unified interface for managing subplot configurations.

## Overview

The `SubplotLayout` class is a unified configuration system that supports:

- **Class-based configuration**: Direct parameter initialization
- **Dictionary configuration**: Load from Python dictionaries
- **YAML file loading**: Load configurations from YAML files
- **Flexible configuration**: Supports multiple initialization methods

## Basic Usage

### 1. Class-based Configuration

```python
from yplot.figure import SubplotLayout
from yplot.plotting import create_figure_with_layout

# Create a complete layout in one command
layout = SubplotLayout(
    fig_size_inches=(10, 8),
    rows=2,
    cols=3,
    row_heights=[3.0, 2.0],
    col_widths=[2.5, 2.5, 2.5],
    wspace=[0.5],
    hspace=[0.3, 0.3],
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
)

# Create figure
fig, axes = create_figure_with_layout(layout)
```

### 2. Dictionary Configuration

```python
# Define layout as dictionary
config = {
    'fig_size': [12, 8],
    'rows': 2,
    'cols': 4,
    'row_heights': [3.0, 2.5],
    'col_widths': [2.0, 2.5, 2.0, 2.5],
    'wspace': [0.4],
    'hspace': [0.2, 0.3, 0.2],
    'margins': {
        'left': 0.5,
        'right': 0.5,
        'top': 0.5,
        'bottom': 0.5
    }
}

# Create figure using dictionary
fig, axes = create_figure_with_layout(config)
```

### 3. YAML File Configuration

```yaml
# simple_layout.yaml
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
# Load from YAML file
fig, axes = create_figure_with_layout('simple_layout.yaml')
```

## Advanced Features

### Row-based Configuration

For complex layouts with different configurations per row, use the `subplot_info` format:

```yaml
# complex_layout.yaml
fig_size: [14, 12]
subplot_info:
  row_1:
    cols: 3
    size: [3.0, 2.5]
    hspace: 0.3
    wspace: 0.4
    margins:
      left: 0.5
      right: 0.5
      top: 0.5
      bottom: 0.5
  row_2:
    cols: 2
    size: [4.5, 3.0]
    hspace: 0.5
    wspace: 0.3
    margins:
      left: 0.5
      right: 0.5
      top: 0.0
      bottom: 0.0
  row_3:
    cols: 4
    size: [2.0, 2.0]
    hspace: 0.2
    margins:
      left: 0.5
      right: 0.5
      top: 0.0
      bottom: 0.5
```

### Saving and Loading Configurations

```python
# Create a complete layout in one command
layout = SubplotLayout(
    fig_size_inches=(8, 6), 
    rows=2, 
    cols=2,
    row_heights=[2.5, 2.0],
    col_widths=[3.0, 3.0],
    wspace=[0.3],
    hspace=[0.2],
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
)

# Save to YAML
layout.to_yaml('my_layout.yaml')

# Load from YAML
loaded_layout = SubplotLayout(yaml_file='my_layout.yaml')
```

## Configuration Parameters

### Basic Parameters

- `fig_size` or `fig_size_inches`: Figure size as [width, height] in inches
- `rows`: Number of rows in the subplot grid
- `cols`: Number of columns in the subplot grid

### Sizing Parameters

- `row_heights`: List of heights in inches for each row
- `col_widths`: List of widths in inches for each column

### Spacing Parameters

- `wspace`: Vertical spacing between rows (list of floats)
- `hspace`: Horizontal spacing between columns (list of floats)

### Margin Parameters

- `margins`: Dictionary with keys 'left', 'right', 'top', 'bottom' (all in inches)

### Complex Layout Parameters

- `subplot_info`: Dictionary with row-based configuration (see row-based example above)

## Examples

See the main documentation for comprehensive examples demonstrating all the features described in this guide.

## Backward Compatibility

The old interface is still fully supported. All existing code using `calculate_subplot_coordinates` with the traditional parameters will continue to work without modification.

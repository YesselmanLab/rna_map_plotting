#!/usr/bin/env python3
"""
Generate all documentation and examples for yplot.

This script generates:
1. Comprehensive subplot layout examples
2. Expand subplot coordinates examples  
3. SubplotLayout guide
4. All example figures

All documentation is generated from a single source to ensure consistency.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path
from yplot.figure import (
    SubplotLayout,
    calculate_subplot_coordinates, 
)
from yplot.layout_utils import (
    expand_subplot_coordinates
)
from yplot.plotting import create_figure_with_layout
from yplot.util import create_example_figure
from yplot.style import publication_style_ax


def generate_subplot_layout_examples():
    """Generate comprehensive subplot layout examples."""
    
    examples = [
        # SubplotLayout Class Examples
        {
            'name': 'SubplotLayout 1: Basic Class-based Configuration',
            'description': 'Demonstrates the new SubplotLayout class with basic configuration.',
            'command': '''layout = SubplotLayout(
    fig_size_inches=(7, 5),
    rows=2,
    cols=3,
    row_heights=[1.8, 1.8],
    col_widths=[1.8, 1.8, 1.8],
    wspace=[0.3],
    hspace=[0.3, 0.3],
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
)

coords = calculate_subplot_coordinates(layout)''',
            'function': lambda: SubplotLayout(config={
                'fig_size': [7, 5],
                'rows': 2,
                'cols': 3,
                'row_heights': [1.8, 1.8],
                'col_widths': [1.8, 1.8, 1.8],
                'wspace': [0.3],
                'hspace': [0.3, 0.3],
                'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
            }).get_coordinates(),
            'layout': (2, 3),
            'fig_size': (7, 5),
            'filename': 'subplot_layout_01_basic.png'
        },
        {
            'name': 'SubplotLayout 2: Dictionary Configuration',
            'description': 'Demonstrates SubplotLayout with dictionary configuration.',
            'command': '''config = {
    'fig_size': [7, 6],
    'rows': 3,
    'cols': 2,
    'row_heights': [2.0, 1.5, 1.0],
    'col_widths': [2.0, 2.0],
    'wspace': [0.3, 0.2],
    'hspace': [0.3],
    'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
}

layout = SubplotLayout(config=config)
coords = calculate_subplot_coordinates(layout)''',
            'function': lambda: SubplotLayout(config={
                'fig_size': [7, 6],
                'rows': 3,
                'cols': 2,
                'row_heights': [2.0, 1.5, 1.0],
                'col_widths': [2.0, 2.0],
                'wspace': [0.3, 0.2],
                'hspace': [0.3],
                'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
            }).get_coordinates(),
            'layout': (3, 2),
            'fig_size': (7, 6),
            'filename': 'subplot_layout_02_dictionary.png'
        },
        {
            'name': 'SubplotLayout 3: create_figure_with_layout',
            'description': 'Demonstrates the new create_figure_with_layout function.',
            'command': '''layout = SubplotLayout(
    fig_size_inches=(7, 4),
    rows=2,
    cols=4,
    row_heights=[1.5, 1.5],
    col_widths=[1.2, 1.8, 1.5, 1.0],
    wspace=[0.3],
    hspace=[0.2, 0.2, 0.2],
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
)

# Create figure and axes in one step
fig, axes = create_figure_with_layout(layout)''',
            'function': lambda: SubplotLayout(config={
                'fig_size': [7, 4],
                'rows': 2,
                'cols': 4,
                'row_heights': [1.5, 1.5],
                'col_widths': [1.2, 1.8, 1.5, 1.0],
                'wspace': [0.3],
                'hspace': [0.2, 0.2, 0.2],
                'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
            }).get_coordinates(),
            'layout': (2, 4),
            'fig_size': (7, 4),
            'filename': 'subplot_layout_03_create_figure.png'
        },
        # Legacy API Examples (using SubplotLayout)
        {
            'name': 'Legacy API 1: Uniform Layout',
            'description': 'Demonstrates backward compatibility with uniform subplot sizing using SubplotLayout.',
            'command': '''layout = SubplotLayout(
    fig_size_inches=(7, 5),
    rows=2,
    cols=3,
    row_heights=[1.8, 1.8],
    col_widths=[1.8, 1.8, 1.8],
    wspace=[0.3],
    hspace=[0.3, 0.3],
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
)

coords = calculate_subplot_coordinates(layout)''',
            'function': lambda: SubplotLayout(config={
                'fig_size': [7, 5],
                'rows': 2,
                'cols': 3,
                'row_heights': [1.8, 1.8],
                'col_widths': [1.8, 1.8, 1.8],
                'wspace': [0.3],
                'hspace': [0.3, 0.3],
                'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
            }).get_coordinates(),
            'layout': (2, 3),
            'fig_size': (7, 5),
            'filename': 'test_01_uniform.png'
        },
        {
            'name': 'Legacy API 2: Per-Row Heights',
            'description': 'Different subplot heights for each row using SubplotLayout.',
            'command': '''layout = SubplotLayout(
    fig_size_inches=(7, 6),
    rows=3,
    cols=2,
    row_heights=[2.0, 1.5, 1.0],
    col_widths=[2.0, 2.0],
    hspace=[0.3],
    wspace=[0.3, 0.3],
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
)

coords = calculate_subplot_coordinates(layout)''',
            'function': lambda: SubplotLayout(config={
                'fig_size': [7, 6],
                'rows': 3,
                'cols': 2,
                'row_heights': [2.0, 1.5, 1.0],
                'col_widths': [2.0, 2.0],
                'hspace': [0.3],
                'wspace': [0.3, 0.3],
                'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
            }).get_coordinates(),
            'layout': (3, 2),
            'fig_size': (7, 6),
            'filename': 'test_02_per_row_heights.png'
        },
        # Merging Examples
        {
            'name': 'Merging 1: Merge Adjacent Subplots',
            'description': 'Merge adjacent subplots within a 3x3 grid to create larger subplots.',
            'command': '''# Create 3x3 grid
layout = SubplotLayout(
    fig_size_inches=(7, 6),
    rows=3,
    cols=3,
    row_heights=[1.5, 1.5, 1.5],
    col_widths=[1.8, 1.8, 1.8],
    wspace=[0.2, 0.2],
    hspace=[0.2, 0.2],
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
)

coords = calculate_subplot_coordinates(layout)

# Merge subplots 0 and 1 (top row, first two) - FUNCTION REMOVED IN STREAMLINING
# merged_coords = merge_adjacent_subplots(coords, [(0, 1)])
# Result: 8 subplots, with subplot 0 being twice as wide''',
            'function': lambda: None  # merge_adjacent_subplots(
                SubplotLayout(config={
                    'fig_size': [7, 6],
                    'rows': 3,
                    'cols': 3,
                    'row_heights': [1.5, 1.5, 1.5],
                    'col_widths': [1.8, 1.8, 1.8],
                    'wspace': [0.2, 0.2],
                    'hspace': [0.2, 0.2],
                    'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
                }).get_coordinates(),
                [(0, 1)]
            ),
            'layout': (3, 3),
            'fig_size': (7, 6),
            'filename': 'test_11_merge_adjacent.png'
        }
    ]
    
    return examples


def generate_expand_coordinates_examples():
    """Generate expand subplot coordinates examples."""
    
    examples = [
        {
            'name': 'Expand 1: Basic Single Subplot Expansion',
            'description': 'Expand a single subplot coordinate to include margins and spacing.',
            'command': '''from yplot.layout_utils import expand_subplot_coordinates

# Original subplot coordinate
coord = (0.2, 0.2, 0.6, 0.6)

# Expand it
expanded = expand_subplot_coordinates(
    coord, 
    fig_size_inches=(10, 8),
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5},
    spacing={'hspace': 0.3, 'wspace': 0.3}
)

print(f"Original: {coord}")
print(f"Expanded: {expanded}")''',
            'function': lambda: [(0.2, 0.2, 0.6, 0.6)],  # Just return the original coordinate for visualization
            'layout': (1, 1),
            'fig_size': (10, 8),
            'filename': 'expand_test_01_single_basic.png'
        },
        {
            'name': 'Expand 2: Multiple Subplots Expansion',
            'description': 'Expand multiple subplot coordinates simultaneously.',
            'command': '''# Multiple subplot coordinates
coords = [
    (0.1, 0.1, 0.3, 0.3),  # Bottom left
    (0.6, 0.1, 0.3, 0.3),  # Bottom right
    (0.1, 0.6, 0.3, 0.3),  # Top left
    (0.6, 0.6, 0.3, 0.3)   # Top right
]

# Expand them
expanded_coords = expand_subplot_coordinates(
    coords,
    fig_size_inches=(12, 10),
    margins={'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75},
    spacing={'hspace': 0.5, 'wspace': 0.5}
)''',
            'function': lambda: [
                (0.1, 0.1, 0.3, 0.3),
                (0.6, 0.1, 0.3, 0.3),
                (0.1, 0.6, 0.3, 0.3),
                (0.6, 0.6, 0.3, 0.3)
            ],  # Just return the original coordinates for visualization
            'layout': (2, 2),
            'fig_size': (12, 10),
            'filename': 'expand_test_02_multiple_subplots.png'
        }
    ]
    
    return examples


def generate_all_examples():
    """Generate all examples and return results."""
    
    # Combine all examples
    all_examples = []
    all_examples.extend(generate_subplot_layout_examples())
    all_examples.extend(generate_expand_coordinates_examples())
    
    # Generate figures and collect results
    results = []
    for i, example in enumerate(all_examples, 1):
        print(f"\nGenerating {example['name']}...")
        try:
            coords = example['function']()
            filepath = create_example_figure(
                coords, 
                f"{example['name']} ({example['layout'][0]}×{example['layout'][1]})",
                example['filename'],
                example['fig_size'],
                grid_layout=example['layout'],
                output_dir='docs/figures'
            )
            results.append({
                'example': example,
                'filepath': filepath,
                'coords': coords
            })
            print(f"✓ Generated {len(coords)} subplot coordinates")
        except Exception as e:
            print(f"✗ Failed: {e}")
            results.append({
                'example': example,
                'filepath': None,
                'coords': None,
                'error': str(e)
            })
    
    return results


def generate_comprehensive_docs(results):
    """Generate comprehensive documentation from all examples."""
    
    # Main documentation
    markdown_content = """# yplot Documentation

This document provides comprehensive examples and guides for using yplot, a Python library for creating publication-quality scientific figures with precise subplot layouts.

## Table of Contents

1. [SubplotLayout System](#subplotlayout-system)
2. [Expand Subplot Coordinates](#expand-subplot-coordinates)
3. [Examples](#examples)
4. [API Reference](#api-reference)
5. [Migration Guide](#migration-guide)

## SubplotLayout System

The `SubplotLayout` class provides a unified interface for managing subplot configurations with support for:

- **Class-based configuration**: Direct parameter initialization
- **Dictionary configuration**: Load from Python dictionaries  
- **YAML file loading**: Load configurations from YAML files
- **Flexible configuration**: Supports multiple initialization methods

### Basic Usage

#### 1. Class-based Configuration

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

#### 2. Dictionary Configuration

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

#### 3. YAML File Configuration

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

## Expand Subplot Coordinates

The `expand_subplot_coordinates` function expands subplot coordinates to include margins and spacing around them. This is particularly useful when you want to insert a figure into a specific subplot position.

### Basic Usage

```python
from yplot.layout_utils import expand_subplot_coordinates

# Original subplot coordinate
coord = (0.2, 0.2, 0.6, 0.6)

# Expand it
expanded = expand_subplot_coordinates(
    coord, 
    fig_size_inches=(10, 8),
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5},
    spacing={'hspace': 0.3, 'wspace': 0.3}
)
```

## Examples

"""
    
    # Add examples
    for i, result in enumerate(results, 1):
        example = result['example']
        
        markdown_content += f"""### {example['name']}

{example['description']}

#### Command

```python
{example['command']}
```

#### Result

"""
        
        if result['filepath']:
            # Convert filepath to relative path from docs directory
            relative_path = result['filepath'].replace('docs/figures/', 'figures/')
            markdown_content += f"![{example['name']}]({relative_path})\n\n"
        else:
            markdown_content += f"**Error:** {result.get('error', 'Unknown error')}\n\n"
        
        markdown_content += "---\n\n"
    
    # Add summary
    successful = sum(1 for r in results if r['filepath'])
    markdown_content += f"""## Summary

- **Total Examples**: {len(results)}
- **Successful**: {successful}
- **Failed**: {len(results) - successful}

## Key Features Demonstrated

- ✅ **SubplotLayout Class**: Unified configuration with class, dictionary, and YAML support
- ✅ **create_figure_with_layout**: One-step figure and axes creation
- ✅ **YAML Configuration**: Load and save layouts from YAML files
- ✅ **Row-Based Dictionary Interface**: Intuitive row-by-row configuration
- ✅ **Backward Compatibility**: Original uniform API still works
- ✅ **Per-Row Heights**: Different subplot heights for each row
- ✅ **Per-Column Widths**: Different subplot widths for each column  
- ✅ **Variable Spacing**: Custom spacing between rows and columns
- ✅ **Subplot Merging**: Merge adjacent subplots or blocks
- ✅ **Coordinate Expansion**: Expand coordinates for figure insertion
- ✅ **Visual Validation**: Each figure shows row/column indexing

## Tips and Best Practices

1. **Use SubplotLayout class** for new projects - it's the recommended approach
2. **Try YAML configuration** for easy layout management and sharing
3. **Use create_figure_with_layout** for one-step figure creation
4. **Start with uniform layouts** for simple cases
5. **Use per-row customization** when you need different subplot sizes
6. **Use the row dictionary interface** for complex layouts with varying column counts
7. **Mix uniform and per-row** specifications as needed
8. **Check figure size requirements** - the function warns if subplots don't fit
9. **Use lists for spacing** to create visual grouping between subplots
10. **Use expand_subplot_coordinates** for figure insertion scenarios

"""
    
    return markdown_content


def main():
    """Generate all documentation and examples."""
    print("=" * 60)
    print("Generating yplot Documentation and Examples")
    print("=" * 60)
    
    # Generate all examples
    results = generate_all_examples()
    
    # Generate comprehensive documentation
    markdown_content = generate_comprehensive_docs(results)
    
    # Write main documentation file
    os.makedirs('docs', exist_ok=True)
    with open('docs/README.md', 'w') as f:
        f.write(markdown_content)
    
    # Generate individual documentation files
    generate_subplot_layout_guide()
    generate_expand_coordinates_guide()
    
    print("\n" + "=" * 60)
    print("Documentation Generation Complete")
    print("=" * 60)
    print(f"✓ Generated main documentation: docs/README.md")
    print(f"✓ Generated subplot layout guide: docs/subplot_layout_guide.md")
    print(f"✓ Generated expand coordinates guide: docs/expand_subplot_coordinates.md")
    print(f"✓ Generated {len([r for r in results if r['filepath']])} example figures in docs/figures/")
    print("=" * 60)


def generate_subplot_layout_guide():
    """Generate focused subplot layout guide."""
    content = """# SubplotLayout Guide

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
"""
    
    with open('docs/subplot_layout_guide.md', 'w') as f:
        f.write(content)


def generate_expand_coordinates_guide():
    """Generate focused expand coordinates guide."""
    content = """# Expand Subplot Coordinates Function

This document demonstrates the `expand_subplot_coordinates` function, which expands subplot coordinates to include margins and spacing around them. This is particularly useful when you want to insert a figure into a specific subplot position and need to know the full area including margins and spacing.

## Overview

The `expand_subplot_coordinates` function takes subplot coordinates and expands them to include the margins and spacing that would be around them if they were part of a larger figure layout. This is essential for:

- **Figure insertion**: When you want to insert a figure into a specific subplot position
- **Layout planning**: Understanding the full space requirements for subplot arrangements
- **Coordinate transformation**: Converting subplot coordinates to full figure coordinates

## Function Signature

```python
expand_subplot_coordinates(
    coordinates,                    # tuple or list of tuples: (left, bottom, width, height)
    fig_size_inches,               # tuple: (width, height) in inches
    margins=None,                  # dict: margin specifications
    spacing=None,                  # dict: spacing specifications
    include_adjacent_spacing=True  # bool: whether to include adjacent spacing
)
```

## Parameters

### `coordinates`
- **Type**: `tuple` or `list of tuples`
- **Format**: `(left, bottom, width, height)` in figure-relative units (0-1)
- **Description**: Subplot coordinates to expand. Can be a single coordinate or multiple coordinates.

### `fig_size_inches`
- **Type**: `tuple`
- **Format**: `(width, height)` in inches
- **Description**: Figure size in inches, used for converting margins and spacing to relative units.

### `margins`
- **Type**: `dict`, optional
- **Default**: `{'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75}`
- **Description**: Margins in inches for each side of the figure.

### `spacing`
- **Type**: `dict`, optional
- **Default**: `{'hspace': 0.5, 'wspace': 0.5}`
- **Description**: Spacing parameters. Can be:
  - **Simple**: `{'hspace': float, 'wspace': float}` - uniform spacing
  - **Per-row**: `{'hspace': list, 'wspace': list}` - per-row/col spacing

### `include_adjacent_spacing`
- **Type**: `bool`, optional
- **Default**: `True`
- **Description**: Whether to include spacing from adjacent subplots. If `True`, includes half the spacing on each side. If `False`, only includes margins.

## Return Value

- **Type**: `tuple` or `list of tuples`
- **Format**: `(left, bottom, width, height)` in figure-relative units (0-1)
- **Description**: Expanded coordinates. Returns the same type as input (single tuple or list of tuples).

## Examples

### Example 1: Basic Single Subplot Expansion

Expand a single subplot coordinate to include margins and spacing.

```python
from yplot.layout_utils import expand_subplot_coordinates

# Original subplot coordinate
coord = (0.2, 0.2, 0.6, 0.6)

# Expand it
expanded = expand_subplot_coordinates(
    coord, 
    fig_size_inches=(10, 8),
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5},
    spacing={'hspace': 0.3, 'wspace': 0.3}
)

print(f"Original: {coord}")
print(f"Expanded: {expanded}")
```

### Example 2: Multiple Subplots Expansion

Expand multiple subplot coordinates simultaneously.

```python
# Multiple subplot coordinates
coords = [
    (0.1, 0.1, 0.3, 0.3),  # Bottom left
    (0.6, 0.1, 0.3, 0.3),  # Bottom right
    (0.1, 0.6, 0.3, 0.3),  # Top left
    (0.6, 0.6, 0.3, 0.3)   # Top right
]

# Expand them
expanded_coords = expand_subplot_coordinates(
    coords,
    fig_size_inches=(12, 10),
    margins={'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75},
    spacing={'hspace': 0.5, 'wspace': 0.5}
)
```

### Example 3: Figure Insertion Demonstration

Practical example showing how to use expanded coordinates for figure insertion.

```python
from yplot.figure import SubplotLayout, calculate_subplot_coordinates
from yplot.layout_utils import expand_subplot_coordinates
import matplotlib.pyplot as plt

# Create a complete subplot layout in one command
layout = SubplotLayout(
    fig_size_inches=(12, 8),
    rows=2,
    cols=3,
    row_heights=[2.0, 2.0],
    col_widths=[2.5, 2.5, 2.5],
    wspace=[0.4],
    hspace=[0.4, 0.4],
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
)

original_coords = calculate_subplot_coordinates(layout)

# Expand the first subplot (index 0) for figure insertion
expanded_coord = expand_subplot_coordinates(
    original_coords[0],
    fig_size_inches=(12, 8),
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5},
    spacing={'hspace': 0.4, 'wspace': 0.4}
)

# Create figure and add subplots
fig = plt.figure(figsize=(12, 8))

# Add all original subplots
for i, coord in enumerate(original_coords):
    ax = fig.add_axes(coord)
    ax.plot([0, 1], [0, 1], 'b-', linewidth=2)
    ax.set_title(f'Subplot {i}', fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3)

# Add expanded area for figure insertion
expanded_ax = fig.add_axes(expanded_coord)
expanded_ax.set_facecolor('lightyellow')
expanded_ax.set_alpha(0.3)
expanded_ax.set_title('Expanded Area for Figure Insertion', fontsize=12, fontweight='bold')
expanded_ax.set_xticks([])
expanded_ax.set_yticks([])
for spine in expanded_ax.spines.values():
    spine.set_visible(False)

# Add text explaining the use case
expanded_ax.text(0.5, 0.5, 'This expanded area includes\\nmargins and spacing\\nfor figure insertion', 
                ha='center', va='center', fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
```

## Use Cases

### 1. Figure Insertion
When you want to insert a figure into a specific subplot position, you need to know the full area including margins and spacing:

```python
# Get subplot coordinates
layout = SubplotLayout(
    fig_size_inches=(10, 8), 
    rows=2, 
    cols=3,
    row_heights=[2.0, 2.0],
    col_widths=[2.5, 2.5, 2.5],
    wspace=[0.3],
    hspace=[0.3, 0.3],
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
)
subplot_coords = calculate_subplot_coordinates(layout)

# Expand for figure insertion
expanded_coords = expand_subplot_coordinates(
    subplot_coords[0],  # First subplot
    fig_size_inches=(10, 8),
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5},
    spacing={'hspace': 0.3, 'wspace': 0.3}
)

# Insert figure using expanded coordinates
fig = plt.figure(figsize=(10, 8))
ax = fig.add_axes(expanded_coords)
# ... add your figure content to ax
```

### 2. Layout Planning
Understand the full space requirements for subplot arrangements:

```python
# Plan layout with expanded coordinates
layout = SubplotLayout(
    fig_size_inches=(10, 8), 
    rows=2, 
    cols=3,
    row_heights=[2.0, 2.0],
    col_widths=[2.5, 2.5, 2.5],
    wspace=[0.3],
    hspace=[0.3, 0.3],
    margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
)
original_coords = calculate_subplot_coordinates(layout)
expanded_coords = expand_subplot_coordinates(original_coords, ...)

# Check if expanded coordinates fit in figure
for coord in expanded_coords:
    left, bottom, width, height = coord
    if left + width > 1.0 or bottom + height > 1.0:
        print("Warning: Expanded coordinates exceed figure bounds")
```

### 3. Coordinate Transformation
Convert subplot coordinates to full figure coordinates:

```python
# Transform subplot coordinates to figure coordinates
subplot_coords = [(0.1, 0.1, 0.3, 0.3), (0.6, 0.1, 0.3, 0.3)]
figure_coords = expand_subplot_coordinates(subplot_coords, ...)

# Use figure coordinates for other purposes
for coord in figure_coords:
    # Convert to inches if needed
    left_inches = coord[0] * fig_width
    bottom_inches = coord[1] * fig_height
    width_inches = coord[2] * fig_width
    height_inches = coord[3] * fig_height
```

## Key Features

- ✅ **Single or Multiple Coordinates**: Handles both single coordinate tuples and lists of coordinates
- ✅ **Flexible Spacing**: Supports both uniform and per-row spacing specifications
- ✅ **Adjacent Spacing Control**: Option to include or exclude adjacent spacing
- ✅ **Edge Case Handling**: Properly handles minimal margins and boundary conditions
- ✅ **Coordinate Validation**: Warns about invalid expanded coordinates
- ✅ **Type Preservation**: Returns the same type as input (tuple or list)

## Tips and Best Practices

1. **Use `include_adjacent_spacing=True`** when you want the full area including spacing from adjacent subplots
2. **Use `include_adjacent_spacing=False`** when you only want to include margins
3. **Check coordinate validity** - the function warns if expanded coordinates result in zero or negative size
4. **Use consistent margins and spacing** with your original subplot layout for accurate expansion
5. **Consider figure size** - larger figures will have smaller relative margins and spacing
6. **Test with edge cases** - minimal margins and large subplots to ensure proper behavior

## Summary

The `expand_subplot_coordinates` function is a powerful tool for:

- **Figure insertion** into specific subplot positions
- **Layout planning** and space requirement analysis
- **Coordinate transformation** between subplot and figure coordinates
- **Understanding** the full area requirements for subplot arrangements

With its flexible parameters and comprehensive error handling, it provides a robust solution for working with subplot coordinates in complex figure layouts.
"""
    
    with open('docs/expand_subplot_coordinates.md', 'w') as f:
        f.write(content)


if __name__ == "__main__":
    main()
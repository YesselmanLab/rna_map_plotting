# Expand Subplot Coordinates Function

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
expanded_ax.text(0.5, 0.5, 'This expanded area includes\nmargins and spacing\nfor figure insertion', 
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

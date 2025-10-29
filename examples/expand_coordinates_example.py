#!/usr/bin/env python3
"""
Example script demonstrating the expand_subplot_coordinates function.

This script shows practical usage of the expand_subplot_coordinates function
for figure insertion and layout planning.
"""

import matplotlib.pyplot as plt
import numpy as np
from yplot.figure import SubplotLayout, calculate_subplot_coordinates, expand_subplot_coordinates
from yplot.plotting import create_figure_with_layout
from yplot.style import publication_style_ax

def example_1_basic_expansion():
    """Example 1: Basic expansion of a single subplot coordinate."""
    print("Example 1: Basic expansion of a single subplot coordinate")
    
    # Original subplot coordinate
    coord = (0.2, 0.2, 0.6, 0.6)
    print(f"Original coordinate: {coord}")
    
    # Expand it
    expanded = expand_subplot_coordinates(
        coord, 
        fig_size_inches=(10, 8),
        margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5},
        spacing={'hspace': 0.3, 'wspace': 0.3}
    )
    
    print(f"Expanded coordinate: {expanded}")
    print(f"Expansion factor: {expanded[2]/coord[2]:.2f}x width, {expanded[3]/coord[3]:.2f}x height")
    print()

def example_2_figure_insertion():
    """Example 2: Practical figure insertion demonstration."""
    print("Example 2: Figure insertion demonstration")
    
    # Create a subplot layout using SubplotLayout
    layout = SubplotLayout(
        fig_size_inches=(12, 8),
        rows=2,
        cols=3
    )
    layout.set_uniform_row_height(2.0)
    layout.set_uniform_col_width(2.5)
    layout.set_uniform_wspace(0.4)
    layout.set_uniform_hspace(0.4)
    layout.margins = {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    
    # Get coordinates
    coords = calculate_subplot_coordinates(layout)
    
    # Expand the first subplot for figure insertion
    expanded_coord = expand_subplot_coordinates(
        coords[0],
        fig_size_inches=(12, 8),
        margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5},
        spacing={'hspace': 0.4, 'wspace': 0.4}
    )
    
    print(f"Original subplot coordinate: {coords[0]}")
    print(f"Expanded coordinate for insertion: {expanded_coord}")
    
    # Create a demonstration figure
    fig = plt.figure(figsize=(12, 8))
    
    # Add all original subplots
    for i, coord in enumerate(coords):
        ax = fig.add_axes(coord)
        ax.plot([0, 1], [0, 1], 'b-', linewidth=2)
        ax.set_title(f'Subplot {i}', fontsize=10)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        publication_style_ax(ax)
    
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
    
    fig.suptitle("Example 2: Figure Insertion Demonstration", fontsize=16, fontweight='bold')
    
    # Save the figure
    fig.savefig('docs/figures/example_02_figure_insertion.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print("Saved demonstration figure: docs/figures/example_02_figure_insertion.png")
    print()

def example_3_multiple_expansion():
    """Example 3: Expanding multiple subplot coordinates."""
    print("Example 3: Expanding multiple subplot coordinates")
    
    # Multiple subplot coordinates
    coords = [
        (0.1, 0.1, 0.3, 0.3),  # Bottom left
        (0.6, 0.1, 0.3, 0.3),  # Bottom right
        (0.1, 0.6, 0.3, 0.3),  # Top left
        (0.6, 0.6, 0.3, 0.3)   # Top right
    ]
    
    print("Original coordinates:")
    for i, coord in enumerate(coords):
        print(f"  Subplot {i}: {coord}")
    
    # Expand them
    expanded_coords = expand_subplot_coordinates(
        coords,
        fig_size_inches=(12, 10),
        margins={'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75},
        spacing={'hspace': 0.5, 'wspace': 0.5}
    )
    
    print("\nExpanded coordinates:")
    for i, coord in enumerate(expanded_coords):
        print(f"  Subplot {i}: {coord}")
    
    # Calculate expansion factors
    print("\nExpansion factors:")
    for i, (orig, exp) in enumerate(zip(coords, expanded_coords)):
        width_factor = exp[2] / orig[2]
        height_factor = exp[3] / orig[3]
        print(f"  Subplot {i}: {width_factor:.2f}x width, {height_factor:.2f}x height")
    print()

def example_4_with_without_spacing():
    """Example 4: Comparison of with and without adjacent spacing."""
    print("Example 4: Comparison of with and without adjacent spacing")
    
    # Original coordinate
    coord = (0.2, 0.2, 0.6, 0.6)
    
    # Expand with adjacent spacing
    expanded_with = expand_subplot_coordinates(
        coord,
        fig_size_inches=(10, 8),
        margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5},
        spacing={'hspace': 0.3, 'wspace': 0.3},
        include_adjacent_spacing=True
    )
    
    # Expand without adjacent spacing
    expanded_without = expand_subplot_coordinates(
        coord,
        fig_size_inches=(10, 8),
        margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5},
        spacing={'hspace': 0.3, 'wspace': 0.3},
        include_adjacent_spacing=False
    )
    
    print(f"Original coordinate: {coord}")
    print(f"With adjacent spacing: {expanded_with}")
    print(f"Without adjacent spacing: {expanded_without}")
    
    # Calculate differences
    width_diff = expanded_with[2] - expanded_without[2]
    height_diff = expanded_with[3] - expanded_without[3]
    
    print(f"Difference (with - without): {width_diff:.4f} width, {height_diff:.4f} height")
    print()

def example_5_create_figure_with_layout():
    """Example 5: Using create_figure_with_layout for easy figure creation."""
    print("Example 5: Using create_figure_with_layout")
    
    # Create layout using SubplotLayout
    layout = SubplotLayout(
        fig_size_inches=(10, 6),
        rows=2,
        cols=3
    )
    layout.row_heights = [2.5, 2.0]
    layout.col_widths = [2.5, 2.5, 2.5]
    layout.set_uniform_wspace(0.3)
    layout.set_uniform_hspace(0.2)
    layout.margins = {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    
    # Create figure and axes in one step
    fig, axes = create_figure_with_layout(layout)
    
    # Add some content to demonstrate
    for i, ax in enumerate(axes):
        x = np.linspace(0, 2*np.pi, 100)
        y = np.sin(x + i * np.pi/6)
        ax.plot(x, y, linewidth=2)
        ax.set_title(f'Plot {i+1}', fontsize=12)
        ax.grid(True, alpha=0.3)
        publication_style_ax(ax)
    
    fig.suptitle("Example 5: create_figure_with_layout", fontsize=16, fontweight='bold')
    
    # Save the figure
    fig.savefig('docs/figures/example_05_create_figure_with_layout.png', dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print("Saved demonstration figure: docs/figures/example_05_create_figure_with_layout.png")
    print()

def example_6_per_row_spacing():
    """Example 6: Expansion with per-row spacing."""
    print("Example 6: Expansion with per-row spacing")
    
    # Multiple subplot coordinates
    coords = [
        (0.1, 0.1, 0.3, 0.3),  # Bottom left
        (0.6, 0.1, 0.3, 0.3),  # Bottom right
        (0.1, 0.6, 0.3, 0.3),  # Top left
        (0.6, 0.6, 0.3, 0.3)   # Top right
    ]
    
    # Expand with per-row spacing
    expanded_coords = expand_subplot_coordinates(
        coords,
        fig_size_inches=(12, 10),
        margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5},
        spacing={'hspace': [0.2, 0.4], 'wspace': [0.3, 0.6]}
    )
    
    print("Original coordinates:")
    for i, coord in enumerate(coords):
        print(f"  Subplot {i}: {coord}")
    
    print("\nExpanded coordinates (per-row spacing):")
    for i, coord in enumerate(expanded_coords):
        print(f"  Subplot {i}: {coord}")
    print()

def run_all_examples():
    """Run all example functions."""
    print("=" * 60)
    print("Expand Subplot Coordinates - Examples")
    print("=" * 60)
    print()
    
    example_1_basic_expansion()
    example_2_figure_insertion()
    example_3_multiple_expansion()
    example_4_with_without_spacing()
    example_5_create_figure_with_layout()
    example_6_per_row_spacing()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_examples()

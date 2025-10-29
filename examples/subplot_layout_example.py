#!/usr/bin/env python3
"""
Example script demonstrating the new SubplotLayout functionality.

This script shows how to use the refactored figure.py with SubplotLayout objects,
dictionary configurations, and YAML files.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Import the new functionality
from yplot.figure import SubplotLayout, calculate_subplot_coordinates
from yplot.plotting import create_figure_with_layout, plot_pop_avg_with_layout


def create_sample_data():
    """Create sample data for demonstration."""
    data = []
    sequences = ["ACGU", "UGCA", "CGAU", "UACG", "GCUA", "AUGC"]
    structures = ["(())", "((..))", "(..)", "((.))", "(())", "((..))"]
    
    for i, (seq, struct) in enumerate(zip(sequences, structures)):
        # Generate random reactivity data
        reactivities = np.random.uniform(0, 1, len(seq))
        data.append({
            'sequence': seq,
            'structure': struct,
            'data': reactivities.tolist(),
            'rna_name': f'RNA_{i+1}'
        })
    
    return pd.DataFrame(data)


def example_1_subplot_layout_object():
    """Example 1: Using SubplotLayout object directly."""
    print("Example 1: SubplotLayout object")
    
    # Create complete layout in one command
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
    
    # Add some content to demonstrate
    for i, ax in enumerate(axes):
        ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
        ax.set_title(f'Subplot {i+1}')
    
    plt.suptitle('Example 1: SubplotLayout Object')
    plt.tight_layout()
    plt.show()


def example_2_dictionary_config():
    """Example 2: Using dictionary configuration."""
    print("Example 2: Dictionary configuration")
    
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
    
    # Add content
    for i, ax in enumerate(axes):
        x = np.linspace(0, 2*np.pi, 100)
        y = np.sin(x + i * np.pi/4)
        ax.plot(x, y)
        ax.set_title(f'Plot {i+1}')
    
    plt.suptitle('Example 2: Dictionary Configuration')
    plt.tight_layout()
    plt.show()


def example_3_yaml_file():
    """Example 3: Using YAML file."""
    print("Example 3: YAML file")
    
    # Create YAML file if it doesn't exist
    yaml_file = Path(__file__).parent / 'simple_layout.yaml'
    
    if not yaml_file.exists():
        print(f"YAML file not found: {yaml_file}")
        return
    
    # Create figure using YAML file
    fig, axes = create_figure_with_layout(str(yaml_file))
    
    # Add content
    for i, ax in enumerate(axes):
        x = np.random.randn(50)
        y = np.random.randn(50)
        ax.scatter(x, y, alpha=0.6)
        ax.set_title(f'Scatter {i+1}')
    
    plt.suptitle('Example 3: YAML File')
    plt.tight_layout()
    plt.show()


def example_4_plotting_functions():
    """Example 4: Using plotting functions with layouts."""
    print("Example 4: Plotting functions with layouts")
    
    # Create sample data
    df = create_sample_data()
    
    # Create complete layout in one command
    layout = SubplotLayout(
        fig_size_inches=(12, 10),
        rows=2,
        cols=3,
        row_heights=[4.0, 3.0],
        col_widths=[3.0, 3.0, 3.0],
        wspace=[0.5],
        hspace=[0.3, 0.3],
        margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    )
    
    # Plot using the new function
    fig = plot_pop_avg_with_layout(df, layout)
    plt.suptitle('Example 4: Plotting Functions with Layout')
    plt.tight_layout()
    plt.show()


def example_5_backward_compatibility():
    """Example 5: Backward compatibility with old interface."""
    print("Example 5: Backward compatibility")
    
    # Create complete layout in one command
    layout = SubplotLayout(
        fig_size_inches=(10, 6),
        rows=2,
        cols=3,
        row_heights=[2.0, 2.0],
        col_widths=[2.5, 2.5, 2.5],
        wspace=[0.5],
        hspace=[0.5, 0.5],
        margins={'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75}
    )
    
    # Get coordinates
    coords = calculate_subplot_coordinates(layout)
    
    # Create figure manually
    fig = plt.figure(figsize=(10, 6))
    axes = []
    for i, (left, bottom, width, height) in enumerate(coords):
        ax = fig.add_axes([left, bottom, width, height])
        axes.append(ax)
        ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
        ax.set_title(f'Legacy {i+1}')
    
    plt.suptitle('Example 5: Backward Compatibility')
    plt.tight_layout()
    plt.show()


def example_6_yaml_save_load():
    """Example 6: Save and load YAML configurations."""
    print("Example 6: Save and load YAML")
    
    # Create complete layout in one command
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
    yaml_file = Path(__file__).parent / 'saved_layout.yaml'
    layout.to_yaml(yaml_file)
    print(f"Saved layout to: {yaml_file}")
    
    # Load from YAML
    loaded_layout = SubplotLayout(yaml_file=yaml_file)
    
    # Create figure with loaded layout
    fig, axes = create_figure_with_layout(loaded_layout)
    
    # Add content
    for i, ax in enumerate(axes):
        x = np.linspace(0, 4, 100)
        y = np.sin(x) * np.exp(-x/4)
        ax.plot(x, y)
        ax.set_title(f'Loaded {i+1}')
    
    plt.suptitle('Example 6: Save and Load YAML')
    plt.tight_layout()
    plt.show()


def example_7_row_based_dictionary():
    """Example 7: Using row-based dictionary format (NEW)."""
    print("Example 7: Row-based dictionary format")
    
    # Define layout using row-based dictionary (row_1, row_2, etc.)
    layout_dict = {
        "fig_size": (8, 6),
        "row_1": {
            "size": (1.5, 2.0),
            "hspace": 0.3,
            "wspace": 0.4,
            "margins": {"left": 0.5, "right": 0.5, "top": 0.3, "bottom": 0.2},
            "cols": 3
        },
        "row_2": {
            "size": (2.0, 1.8),
            "hspace": 0.4,
            "wspace": 0.5,
            "margins": {"left": 0.5, "right": 0.5, "top": 0.2, "bottom": 0.3},
            "cols": 2
        },
    }
    
    # Create layout and figure
    layout = SubplotLayout(config=layout_dict)
    fig, axes = create_figure_with_layout(layout)
    
    # Add content
    for i, ax in enumerate(axes):
        x = np.linspace(0, 2*np.pi, 100)
        y = np.sin(x + i * np.pi/4)
        ax.plot(x, y, linewidth=2)
        ax.set_title(f'Row-based {i+1}')
    
    plt.suptitle('Example 7: Row-Based Dictionary Format (NEW)')
    plt.tight_layout()
    plt.show()


def example_8_simple_row_layout():
    """Example 8: Simple single-row layout."""
    print("Example 8: Simple single-row layout")
    
    # Simple 1x4 layout
    layout_dict = {
        "fig_size": (7, 2),
        "row_1": {
            "size": (1.3, 1.3),
            "hspace": 0.45,
            "wspace": 0.50,
            "margins": {"left": 0.40, "right": 0.0, "top": 0.0, "bottom": 0.50},
            "cols": 4
        },
    }
    
    # Create layout and figure
    layout = SubplotLayout(config=layout_dict)
    fig, axes = create_figure_with_layout(layout)
    
    # Add simple content
    for i, ax in enumerate(axes):
        ax.plot([1, 2, 3], [1, 2, 1], marker='o')
        ax.set_title(f'Plot {i+1}')
    
    plt.suptitle('Example 8: Simple Row Layout')
    plt.tight_layout()
    plt.show()


def main():
    """Run all examples."""
    print("SubplotLayout Examples")
    print("=" * 50)
    
    try:
        example_1_subplot_layout_object()
        example_2_dictionary_config()
        example_3_yaml_file()
        example_4_plotting_functions()
        example_5_backward_compatibility()
        example_6_yaml_save_load()
        example_7_row_based_dictionary()
        example_8_simple_row_layout()
        
        print("\nAll examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

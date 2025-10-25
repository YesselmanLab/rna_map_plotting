"""
Example demonstrating per-row subplot customization using calculate_subplot_coordinates.

This example shows how to specify different subplot sizes, spacing, and margins
for each row using the updated calculate_subplot_coordinates function.
"""

from yplot.figure import calculate_subplot_coordinates


def example_1_uniform_backward_compatible():
    """Example 1: Uniform layout (backward compatible with original API)"""
    print("Example 1: Uniform Layout (Backward Compatible)")
    print("-" * 60)
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(10, 6),
        subplot_layout=(2, 3),
        subplot_size_inches=(2.5, 2.0),  # Single tuple - all subplots same size
        spacing={
            'hspace': 0.5,  # Single value - uniform spacing
            'wspace': 0.5,
            'margins': {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75}
        }
    )
    
    print(f"Figure size: (10, 6)")
    print(f"Layout: 2 rows x 3 cols")
    print(f"All subplots: 2.5\" x 2.0\"")
    print(f"Generated {len(coords)} subplot coordinates")
    print()
    return coords


def example_2_per_row_heights():
    """Example 2: Different subplot height for each row"""
    print("Example 2: Different Subplot Heights Per Row")
    print("-" * 60)
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(10, 8),
        subplot_layout=(3, 2),  # 3 rows, 2 columns
        subplot_size_inches={
            'row_heights': [3.0, 2.0, 1.5],  # Top row tallest, bottom shortest
            'col_widths': [3.0, 3.0]  # Both columns same width
        },
        spacing={
            'hspace': [0.5],  # Uniform horizontal spacing between columns
            'wspace': [0.5, 0.5],  # Uniform vertical spacing between rows
            'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
        }
    )
    
    print(f"Figure size: (10, 8)")
    print(f"Layout: 3 rows x 2 cols")
    print(f"Row heights: [3.0\", 2.0\", 1.5\"]")
    print(f"Col widths: [3.0\", 3.0\"]")
    print(f"Generated {len(coords)} subplot coordinates")
    print()
    return coords


def example_3_per_row_variable_spacing():
    """Example 3: Variable spacing between rows"""
    print("Example 3: Variable Spacing Between Rows")
    print("-" * 60)
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(10, 9),
        subplot_layout=(3, 3),
        subplot_size_inches={
            'row_heights': [2.5, 2.5, 2.5],
            'col_widths': [2.5, 2.5, 2.5]
        },
        spacing={
            'hspace': [0.3, 0.3],  # Uniform horizontal spacing
            'wspace': [0.3, 1.0],  # Small gap after row 0, large gap after row 1
            'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
        }
    )
    
    print(f"Figure size: (10, 9)")
    print(f"Layout: 3 rows x 3 cols")
    print(f"Vertical spacing: [0.3\", 1.0\"] - creates visual grouping")
    print(f"  (0.3\" between rows 0-1, 1.0\" between rows 1-2)")
    print(f"Generated {len(coords)} subplot coordinates")
    print()
    return coords


def example_4_complex_per_row():
    """Example 4: Complex layout with all per-row customizations"""
    print("Example 4: Complex Per-Row Customization")
    print("-" * 60)
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(12, 10),
        subplot_layout=(4, 3),  # 4 rows, 3 columns
        subplot_size_inches={
            'row_heights': [2.0, 3.0, 2.5, 1.5],  # Each row different height
            'col_widths': [3.0, 4.0, 3.5]  # Each column different width
        },
        spacing={
            'hspace': [0.4, 0.5],  # Different spacing between each column pair
            'wspace': [0.3, 0.6, 0.4],  # Different spacing between each row pair
            'margins': {
                'left': 0.75,
                'right': 0.5,
                'top': 0.5,
                'bottom': 1.0  # Extra space at bottom for labels
            }
        }
    )
    
    print(f"Figure size: (12, 10)")
    print(f"Layout: 4 rows x 3 cols")
    print(f"Row heights: [2.0\", 3.0\", 2.5\", 1.5\"]")
    print(f"Col widths: [3.0\", 4.0\", 3.5\"]")
    print(f"Horizontal spacing: [0.4\", 0.5\"]")
    print(f"Vertical spacing: [0.3\", 0.6\", 0.4\"]")
    print(f"Margins: left=0.75\", right=0.5\", top=0.5\", bottom=1.0\"")
    print(f"Generated {len(coords)} subplot coordinates")
    print()
    return coords


def example_5_mixed_api():
    """Example 5: Mix uniform and per-row specifications"""
    print("Example 5: Mixed Uniform and Per-Row")
    print("-" * 60)
    
    # Uniform subplot sizes, but variable spacing
    coords = calculate_subplot_coordinates(
        fig_size_inches=(9, 8),
        subplot_layout=(3, 2),
        subplot_size_inches=(3.0, 2.0),  # Uniform sizes (tuple)
        spacing={
            'hspace': 0.5,  # Uniform horizontal spacing (single value)
            'wspace': [0.3, 0.8],  # Variable vertical spacing (list)
            'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
        }
    )
    
    print(f"Figure size: (9, 8)")
    print(f"Layout: 3 rows x 2 cols")
    print(f"All subplots: 3.0\" x 2.0\" (uniform)")
    print(f"Horizontal spacing: 0.5\" (uniform)")
    print(f"Vertical spacing: [0.3\", 0.8\"] (variable)")
    print(f"Generated {len(coords)} subplot coordinates")
    print()
    return coords


def print_coordinates_detail(coords, title):
    """Helper to print coordinate details"""
    print(f"\n{title}")
    print("=" * 60)
    for idx, (left, bottom, width, height) in enumerate(coords):
        print(f"  Subplot {idx}: left={left:.3f}, bottom={bottom:.3f}, "
              f"width={width:.3f}, height={height:.3f}")
    print()


if __name__ == "__main__":
    print("=" * 60)
    print("Per-Row Subplot Customization Examples")
    print("=" * 60)
    print()
    
    # Run all examples
    coords1 = example_1_uniform_backward_compatible()
    coords2 = example_2_per_row_heights()
    coords3 = example_3_per_row_variable_spacing()
    coords4 = example_4_complex_per_row()
    coords5 = example_5_mixed_api()
    
    print("=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
    print()
    
    # Optional: Show detailed coordinates for one example
    print("Detailed coordinates for Example 2:")
    print_coordinates_detail(coords2, "3 rows x 2 cols with varying row heights")
    
    print("\nKey Features:")
    print("  - Backward compatible: Use tuples for uniform layouts")
    print("  - Per-row heights: Supply 'row_heights' list in dict")
    print("  - Per-col widths: Supply 'col_widths' list in dict")
    print("  - Variable spacing: Use lists for hspace/wspace")
    print("  - Mix and match: Combine uniform and per-row specifications")


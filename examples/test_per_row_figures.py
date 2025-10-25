"""
Test suite for per-row subplot customization with 10 different configurations.
Each test generates a figure and saves it as a PNG.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from yplot.figure import calculate_subplot_coordinates
import os
import textwrap


def create_test_figure(coords, layout, title, filename, fig_size_inches, command_code=None):
    """Create and save a test figure with the given coordinates."""
    fig = plt.figure(figsize=fig_size_inches, dpi=100)
    
    # Color palette for different rows
    row_colors = ['#ffcccc', '#ccffcc', '#ccccff', '#ffffcc', '#ffccff', '#ccffff']
    
    for idx, (left, bottom, width, height) in enumerate(coords):
        ax = fig.add_axes([left, bottom, width, height])
        
        # Determine which row this subplot is in
        row = idx // layout[1]  # layout[1] is number of columns
        col = idx % layout[1]
        
        # Set background color based on row
        ax.set_facecolor(row_colors[row % len(row_colors)])
        
        # Add text showing subplot info
        ax.text(0.5, 0.5, f'R{row}C{col}\n{idx}', 
                ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Add a subtle border
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(0.5)
        
        # Remove ticks for cleaner look
        ax.set_xticks([])
        ax.set_yticks([])
    
    fig.suptitle(title, fontsize=14, fontweight='bold', y=0.95)
    
    # Save the figure
    output_dir = 'test_figures'
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    
    print(f"✓ Saved: {filepath}")
    return filepath, command_code


def test_1_uniform_backward_compatible():
    """Test 1: Uniform layout (backward compatible)"""
    print("\nTest 1: Uniform Layout (Backward Compatible)")
    print("-" * 50)
    
    command_code = '''coords = calculate_subplot_coordinates(
    fig_size_inches=(10, 6),
    subplot_layout=(2, 3),
    subplot_size_inches=(2.5, 2.0),  # tuple - uniform sizing
    spacing={
        'hspace': 0.5,
        'wspace': 0.5,
        'margins': {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75}
    }
)'''
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(10, 6),
        subplot_layout=(2, 3),
        subplot_size_inches=(2.5, 2.0),
        spacing={
            'hspace': 0.5,
            'wspace': 0.5,
            'margins': {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75}
        }
    )
    
    return create_test_figure(
        coords, (2, 3), 
        "Test 1: Uniform Layout (2×3, 2.5\"×2.0\" each)",
        "test_01_uniform.png",
        (10, 6),
        command_code
    )


def test_2_per_row_heights():
    """Test 2: Different subplot heights per row"""
    print("\nTest 2: Per-Row Heights")
    print("-" * 50)
    
    command_code = '''coords = calculate_subplot_coordinates(
    fig_size_inches=(10, 8),
    subplot_layout=(3, 2),
    subplot_size_inches={
        'row_heights': [3.0, 2.0, 1.5],  # dict - per-row heights
        'col_widths': [3.0, 3.0]
    },
    spacing={
        'hspace': [0.5],  # list - per-column spacing
        'wspace': [0.5, 0.5],  # list - per-row spacing
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    }
)'''
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(10, 8),
        subplot_layout=(3, 2),
        subplot_size_inches={
            'row_heights': [3.0, 2.0, 1.5],  # Top row tallest, bottom shortest
            'col_widths': [3.0, 3.0]
        },
        spacing={
            'hspace': [0.5],
            'wspace': [0.5, 0.5],
            'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
        }
    )
    
    return create_test_figure(
        coords, (3, 2),
        "Test 2: Per-Row Heights (3×2, heights: 3.0\", 2.0\", 1.5\")",
        "test_02_per_row_heights.png",
        (10, 8),
        command_code
    )


def test_3_per_column_widths():
    """Test 3: Different subplot widths per column"""
    print("\nTest 3: Per-Column Widths")
    print("-" * 50)
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(12, 6),
        subplot_layout=(2, 4),
        subplot_size_inches={
            'row_heights': [2.5, 2.5],
            'col_widths': [2.0, 3.0, 2.5, 1.5]  # Varying column widths
        },
        spacing={
            'hspace': [0.3, 0.3, 0.3],
            'wspace': [0.5],
            'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
        }
    )
    
    return create_test_figure(
        coords, (2, 4),
        "Test 3: Per-Column Widths (2×4, widths: 2.0\", 3.0\", 2.5\", 1.5\")",
        "test_03_per_column_widths.png",
        (12, 6)
    )


def test_4_variable_vertical_spacing():
    """Test 4: Variable vertical spacing between rows"""
    print("\nTest 4: Variable Vertical Spacing")
    print("-" * 50)
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(10, 9),
        subplot_layout=(3, 3),
        subplot_size_inches={
            'row_heights': [2.5, 2.5, 2.5],
            'col_widths': [2.5, 2.5, 2.5]
        },
        spacing={
            'hspace': [0.3, 0.3],
            'wspace': [0.3, 1.0],  # Small gap after row 0, large gap after row 1
            'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
        }
    )
    
    return create_test_figure(
        coords, (3, 3),
        "Test 4: Variable Vertical Spacing (3×3, wspace: 0.3\", 1.0\")",
        "test_04_variable_vertical_spacing.png",
        (10, 9)
    )


def test_5_variable_horizontal_spacing():
    """Test 5: Variable horizontal spacing between columns"""
    print("\nTest 5: Variable Horizontal Spacing")
    print("-" * 50)
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(12, 6),
        subplot_layout=(2, 4),
        subplot_size_inches={
            'row_heights': [2.5, 2.5],
            'col_widths': [2.5, 2.5, 2.5, 2.5]
        },
        spacing={
            'hspace': [0.3, 0.8, 0.3],  # Variable horizontal spacing
            'wspace': [0.5],
            'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
        }
    )
    
    return create_test_figure(
        coords, (2, 4),
        "Test 5: Variable Horizontal Spacing (2×4, hspace: 0.3\", 0.8\", 0.3\")",
        "test_05_variable_horizontal_spacing.png",
        (12, 6)
    )


def test_6_complex_mixed():
    """Test 6: Complex layout with all customizations"""
    print("\nTest 6: Complex Mixed Layout")
    print("-" * 50)
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(14, 10),
        subplot_layout=(4, 3),
        subplot_size_inches={
            'row_heights': [2.0, 3.0, 2.5, 1.5],  # Each row different height
            'col_widths': [3.0, 4.0, 3.5]  # Each column different width
        },
        spacing={
            'hspace': [0.4, 0.5],  # Different spacing between columns
            'wspace': [0.3, 0.6, 0.4],  # Different spacing between rows
            'margins': {
                'left': 0.75,
                'right': 0.5,
                'top': 0.5,
                'bottom': 1.0  # Extra space at bottom
            }
        }
    )
    
    return create_test_figure(
        coords, (4, 3),
        "Test 6: Complex Mixed (4×3, all custom sizes & spacing)",
        "test_06_complex_mixed.png",
        (14, 10)
    )


def test_7_tall_narrow():
    """Test 7: Tall and narrow subplots"""
    print("\nTest 7: Tall and Narrow Subplots")
    print("-" * 50)
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(8, 12),
        subplot_layout=(4, 2),
        subplot_size_inches={
            'row_heights': [2.5, 2.5, 2.5, 2.5],
            'col_widths': [3.0, 3.0]
        },
        spacing={
            'hspace': [0.5],
            'wspace': [0.3, 0.3, 0.3],
            'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
        }
    )
    
    return create_test_figure(
        coords, (4, 2),
        "Test 7: Tall and Narrow (4×2, portrait layout)",
        "test_07_tall_narrow.png",
        (8, 12)
    )


def test_8_wide_short():
    """Test 8: Wide and short subplots"""
    print("\nTest 8: Wide and Short Subplots")
    print("-" * 50)
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(15, 4),
        subplot_layout=(2, 5),
        subplot_size_inches={
            'row_heights': [1.5, 1.5],
            'col_widths': [2.5, 2.5, 2.5, 2.5, 2.5]
        },
        spacing={
            'hspace': [0.2, 0.2, 0.2, 0.2],
            'wspace': [0.3],
            'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
        }
    )
    
    return create_test_figure(
        coords, (2, 5),
        "Test 8: Wide and Short (2×5, landscape layout)",
        "test_08_wide_short.png",
        (15, 4)
    )


def test_9_asymmetric():
    """Test 9: Asymmetric layout with different row/column counts"""
    print("\nTest 9: Asymmetric Layout")
    print("-" * 50)
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(12, 8),
        subplot_layout=(3, 5),  # 3 rows, 5 columns
        subplot_size_inches={
            'row_heights': [2.0, 3.0, 2.0],  # Middle row taller
            'col_widths': [2.0, 2.0, 2.0, 2.0, 2.0]
        },
        spacing={
            'hspace': [0.3, 0.3, 0.3, 0.3],
            'wspace': [0.4, 0.4],
            'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
        }
    )
    
    return create_test_figure(
        coords, (3, 5),
        "Test 9: Asymmetric (3×5, middle row taller)",
        "test_09_asymmetric.png",
        (12, 8)
    )


def test_10_minimal_margins():
    """Test 10: Minimal margins and tight spacing"""
    print("\nTest 10: Minimal Margins")
    print("-" * 50)
    
    coords = calculate_subplot_coordinates(
        fig_size_inches=(10, 8),
        subplot_layout=(3, 3),
        subplot_size_inches={
            'row_heights': [2.5, 2.5, 2.5],
            'col_widths': [2.5, 2.5, 2.5]
        },
        spacing={
            'hspace': [0.1, 0.1],  # Very tight horizontal spacing
            'wspace': [0.1, 0.1],  # Very tight vertical spacing
            'margins': {
                'left': 0.2, 'right': 0.2, 'top': 0.2, 'bottom': 0.2
            }
        }
    )
    
    return create_test_figure(
        coords, (3, 3),
        "Test 10: Minimal Margins (3×3, tight spacing)",
        "test_10_minimal_margins.png",
        (10, 8)
    )


def main():
    """Run all 10 tests and generate figures."""
    print("=" * 60)
    print("Per-Row Subplot Customization Test Suite")
    print("=" * 60)
    print("Generating 10 test figures with different configurations...")
    print()
    
    # Create output directory
    os.makedirs('test_figures', exist_ok=True)
    
    # Run all tests
    tests = [
        test_1_uniform_backward_compatible,
        test_2_per_row_heights,
        test_3_per_column_widths,
        test_4_variable_vertical_spacing,
        test_5_variable_horizontal_spacing,
        test_6_complex_mixed,
        test_7_tall_narrow,
        test_8_wide_short,
        test_9_asymmetric,
        test_10_minimal_margins
    ]
    
    results = []
    for i, test_func in enumerate(tests, 1):
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {i} failed: {e}")
            results.append(None)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    successful = sum(1 for r in results if r is not None)
    print(f"✓ Successful: {successful}/10")
    print(f"✗ Failed: {10 - successful}/10")
    print()
    print("Generated files:")
    for result in results:
        if result:
            print(f"  - {result}")
    
    print(f"\nAll figures saved in: test_figures/")
    print("=" * 60)


if __name__ == "__main__":
    main()

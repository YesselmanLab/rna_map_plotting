"""
Generate markdown documentation with test figures and command examples.
All figures use 7" width and max 9" height.
"""

import matplotlib.pyplot as plt
from yplot.figure import calculate_subplot_coordinates
import os


def create_test_figure(coords, layout, title, filename, fig_size_inches):
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
    return filepath


def generate_markdown_docs():
    """Generate markdown documentation with all test examples."""
    
    # Test configurations with their command codes - all using 7" width, max 9" height
    tests = [
        {
            'name': 'Test 1: Uniform Layout (Backward Compatible)',
            'description': 'Demonstrates backward compatibility with uniform subplot sizing.',
            'command': '''coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 5),
    subplot_layout=(2, 3),
    subplot_size_inches=(1.8, 1.8),  # tuple - uniform sizing
    spacing={
        'hspace': 0.3,
        'wspace': 0.3,
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    }
)''',
            'function': lambda: calculate_subplot_coordinates(
                fig_size_inches=(7, 5),
                subplot_layout=(2, 3),
                subplot_size_inches=(1.8, 1.8),
                spacing={
                    'hspace': 0.3,
                    'wspace': 0.3,
                    'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
                }
            ),
            'layout': (2, 3),
            'fig_size': (7, 5),
            'filename': 'test_01_uniform.png'
        },
        {
            'name': 'Test 2: Per-Row Heights',
            'description': 'Different subplot heights for each row using dictionary specification.',
            'command': '''coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 6),
    subplot_layout=(3, 2),
    subplot_size_inches={
        'row_heights': [2.0, 1.5, 1.0],  # dict - per-row heights
        'col_widths': [2.0, 2.0]
    },
    spacing={
        'hspace': [0.3],  # list - per-column spacing
        'wspace': [0.3, 0.3],  # list - per-row spacing
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    }
)''',
            'function': lambda: calculate_subplot_coordinates(
                fig_size_inches=(7, 6),
                subplot_layout=(3, 2),
                subplot_size_inches={
                    'row_heights': [2.0, 1.5, 1.0],
                    'col_widths': [2.0, 2.0]
                },
                spacing={
                    'hspace': [0.3],
                    'wspace': [0.3, 0.3],
                    'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
                }
            ),
            'layout': (3, 2),
            'fig_size': (7, 6),
            'filename': 'test_02_per_row_heights.png'
        },
        {
            'name': 'Test 3: Per-Column Widths',
            'description': 'Different subplot widths for each column.',
            'command': '''coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 4),
    subplot_layout=(2, 4),
    subplot_size_inches={
        'row_heights': [1.5, 1.5],
        'col_widths': [1.2, 1.8, 1.5, 1.0]  # varying column widths
    },
    spacing={
        'hspace': [0.2, 0.2, 0.2],  # list - per-column spacing
        'wspace': [0.3],  # single value - uniform row spacing
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    }
)''',
            'function': lambda: calculate_subplot_coordinates(
                fig_size_inches=(7, 4),
                subplot_layout=(2, 4),
                subplot_size_inches={
                    'row_heights': [1.5, 1.5],
                    'col_widths': [1.2, 1.8, 1.5, 1.0]
                },
                spacing={
                    'hspace': [0.2, 0.2, 0.2],
                    'wspace': [0.3],
                    'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
                }
            ),
            'layout': (2, 4),
            'fig_size': (7, 4),
            'filename': 'test_03_per_column_widths.png'
        },
        {
            'name': 'Test 4: Variable Vertical Spacing',
            'description': 'Different vertical spacing between rows to create visual grouping.',
            'command': '''coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 6),
    subplot_layout=(3, 3),
    subplot_size_inches={
        'row_heights': [1.5, 1.5, 1.5],
        'col_widths': [1.8, 1.8, 1.8]
    },
    spacing={
        'hspace': [0.2, 0.2],  # uniform horizontal spacing
        'wspace': [0.2, 0.6],  # variable vertical spacing
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    }
)''',
            'function': lambda: calculate_subplot_coordinates(
                fig_size_inches=(7, 6),
                subplot_layout=(3, 3),
                subplot_size_inches={
                    'row_heights': [1.5, 1.5, 1.5],
                    'col_widths': [1.8, 1.8, 1.8]
                },
                spacing={
                    'hspace': [0.2, 0.2],
                    'wspace': [0.2, 0.6],
                    'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
                }
            ),
            'layout': (3, 3),
            'fig_size': (7, 6),
            'filename': 'test_04_variable_vertical_spacing.png'
        },
        {
            'name': 'Test 5: Variable Horizontal Spacing',
            'description': 'Different horizontal spacing between columns.',
            'command': '''coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 4),
    subplot_layout=(2, 4),
    subplot_size_inches={
        'row_heights': [1.5, 1.5],
        'col_widths': [1.5, 1.5, 1.5, 1.5]
    },
    spacing={
        'hspace': [0.2, 0.5, 0.2],  # variable horizontal spacing
        'wspace': [0.3],  # uniform vertical spacing
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    }
)''',
            'function': lambda: calculate_subplot_coordinates(
                fig_size_inches=(7, 4),
                subplot_layout=(2, 4),
                subplot_size_inches={
                    'row_heights': [1.5, 1.5],
                    'col_widths': [1.5, 1.5, 1.5, 1.5]
                },
                spacing={
                    'hspace': [0.2, 0.5, 0.2],
                    'wspace': [0.3],
                    'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
                }
            ),
            'layout': (2, 4),
            'fig_size': (7, 4),
            'filename': 'test_05_variable_horizontal_spacing.png'
        },
        {
            'name': 'Test 6: Complex Mixed Layout',
            'description': 'Complex layout with all customizations: different row heights, column widths, and variable spacing.',
            'command': '''coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 8),
    subplot_layout=(4, 2),
    subplot_size_inches={
        'row_heights': [1.5, 2.0, 1.8, 1.2],  # each row different height
        'col_widths': [2.0, 2.0]  # equal column widths
    },
    spacing={
        'hspace': [0.3],  # uniform horizontal spacing
        'wspace': [0.2, 0.4, 0.3],  # different spacing between rows
        'margins': {
            'left': 0.5,
            'right': 0.5,
            'top': 0.5,
            'bottom': 0.8  # extra space at bottom
        }
    }
)''',
            'function': lambda: calculate_subplot_coordinates(
                fig_size_inches=(7, 8),
                subplot_layout=(4, 2),
                subplot_size_inches={
                    'row_heights': [1.5, 2.0, 1.8, 1.2],
                    'col_widths': [2.0, 2.0]
                },
                spacing={
                    'hspace': [0.3],
                    'wspace': [0.2, 0.4, 0.3],
                    'margins': {
                        'left': 0.5,
                        'right': 0.5,
                        'top': 0.5,
                        'bottom': 0.8
                    }
                }
            ),
            'layout': (4, 2),
            'fig_size': (7, 8),
            'filename': 'test_06_complex_mixed.png'
        },
        {
            'name': 'Test 7: Tall and Narrow Layout',
            'description': 'Portrait layout with tall, narrow subplots.',
            'command': '''coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 9),
    subplot_layout=(4, 2),
    subplot_size_inches={
        'row_heights': [1.8, 1.8, 1.8, 1.8],
        'col_widths': [2.0, 2.0]
    },
    spacing={
        'hspace': [0.3],  # uniform horizontal spacing
        'wspace': [0.2, 0.2, 0.2],  # uniform vertical spacing
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    }
)''',
            'function': lambda: calculate_subplot_coordinates(
                fig_size_inches=(7, 9),
                subplot_layout=(4, 2),
                subplot_size_inches={
                    'row_heights': [1.8, 1.8, 1.8, 1.8],
                    'col_widths': [2.0, 2.0]
                },
                spacing={
                    'hspace': [0.3],
                    'wspace': [0.2, 0.2, 0.2],
                    'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
                }
            ),
            'layout': (4, 2),
            'fig_size': (7, 9),
            'filename': 'test_07_tall_narrow.png'
        },
        {
            'name': 'Test 8: Wide and Short Layout',
            'description': 'Landscape layout with wide, short subplots.',
            'command': '''coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 3),
    subplot_layout=(2, 5),
    subplot_size_inches={
        'row_heights': [1.0, 1.0],
        'col_widths': [1.0, 1.0, 1.0, 1.0, 1.0]
    },
    spacing={
        'hspace': [0.1, 0.1, 0.1, 0.1],  # tight horizontal spacing
        'wspace': [0.2],  # uniform vertical spacing
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    }
)''',
            'function': lambda: calculate_subplot_coordinates(
                fig_size_inches=(7, 3),
                subplot_layout=(2, 5),
                subplot_size_inches={
                    'row_heights': [1.0, 1.0],
                    'col_widths': [1.0, 1.0, 1.0, 1.0, 1.0]
                },
                spacing={
                    'hspace': [0.1, 0.1, 0.1, 0.1],
                    'wspace': [0.2],
                    'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
                }
            ),
            'layout': (2, 5),
            'fig_size': (7, 3),
            'filename': 'test_08_wide_short.png'
        },
        {
            'name': 'Test 9: Asymmetric Layout',
            'description': 'Asymmetric layout with different row/column counts and middle row taller.',
            'command': '''coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 6),
    subplot_layout=(3, 4),  # 3 rows, 4 columns
    subplot_size_inches={
        'row_heights': [1.5, 2.0, 1.5],  # middle row taller
        'col_widths': [1.2, 1.2, 1.2, 1.2]
    },
    spacing={
        'hspace': [0.2, 0.2, 0.2],  # uniform horizontal spacing
        'wspace': [0.3, 0.3],  # uniform vertical spacing
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    }
)''',
            'function': lambda: calculate_subplot_coordinates(
                fig_size_inches=(7, 6),
                subplot_layout=(3, 4),
                subplot_size_inches={
                    'row_heights': [1.5, 2.0, 1.5],
                    'col_widths': [1.2, 1.2, 1.2, 1.2]
                },
                spacing={
                    'hspace': [0.2, 0.2, 0.2],
                    'wspace': [0.3, 0.3],
                    'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
                }
            ),
            'layout': (3, 4),
            'fig_size': (7, 6),
            'filename': 'test_09_asymmetric.png'
        },
        {
            'name': 'Test 10: Minimal Margins',
            'description': 'Minimal margins and tight spacing for maximum subplot area.',
            'command': '''coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 6),
    subplot_layout=(3, 3),
    subplot_size_inches={
        'row_heights': [1.5, 1.5, 1.5],
        'col_widths': [1.8, 1.8, 1.8]
    },
    spacing={
        'hspace': [0.1, 0.1],  # very tight horizontal spacing
        'wspace': [0.1, 0.1],  # very tight vertical spacing
        'margins': {
            'left': 0.2, 'right': 0.2, 'top': 0.2, 'bottom': 0.2
        }
    }
)''',
            'function': lambda: calculate_subplot_coordinates(
                fig_size_inches=(7, 6),
                subplot_layout=(3, 3),
                subplot_size_inches={
                    'row_heights': [1.5, 1.5, 1.5],
                    'col_widths': [1.8, 1.8, 1.8]
                },
                spacing={
                    'hspace': [0.1, 0.1],
                    'wspace': [0.1, 0.1],
                    'margins': {
                        'left': 0.2, 'right': 0.2, 'top': 0.2, 'bottom': 0.2
                    }
                }
            ),
            'layout': (3, 3),
            'fig_size': (7, 6),
            'filename': 'test_10_minimal_margins.png'
        }
    ]
    
    # Generate figures and collect results
    results = []
    for i, test in enumerate(tests, 1):
        print(f"\nGenerating {test['name']}...")
        try:
            coords = test['function']()
            filepath = create_test_figure(
                coords, test['layout'], 
                f"{test['name']} ({test['layout'][0]}×{test['layout'][1]})",
                test['filename'],
                test['fig_size']
            )
            results.append({
                'test': test,
                'filepath': filepath,
                'coords': coords
            })
            print(f"✓ Generated {len(coords)} subplot coordinates")
        except Exception as e:
            print(f"✗ Failed: {e}")
            results.append({
                'test': test,
                'filepath': None,
                'coords': None,
                'error': str(e)
            })
    
    # Generate markdown documentation
    generate_markdown_file(results)
    
    return results


def generate_markdown_file(results):
    """Generate markdown documentation file."""
    
    markdown_content = """# Per-Row Subplot Customization Examples

This document demonstrates the enhanced `calculate_subplot_coordinates` function that supports per-row and per-column customization of subplot layouts.

## Overview

The updated function supports both backward-compatible uniform layouts and advanced per-row/column customization:

- **Uniform layouts**: Use tuples for `subplot_size_inches` and single values for spacing
- **Per-row customization**: Use dictionaries with lists for `row_heights`, `col_widths`, and spacing
- **Mixed specifications**: Combine uniform and per-row settings as needed

## API Reference

### Function Signature
```python
calculate_subplot_coordinates(
    fig_size_inches,      # tuple: (width, height) in inches
    subplot_layout,       # tuple: (rows, columns)
    subplot_size_inches,  # tuple or dict: uniform or per-row/col sizes
    spacing              # dict: spacing and margin parameters
)
```

### Parameters

#### `subplot_size_inches`
- **tuple**: `(width, height)` - uniform size for all subplots
- **dict**: `{'row_heights': list, 'col_widths': list}` - per-row/col sizes

#### `spacing`
- **Uniform**: `{'hspace': float, 'wspace': float, 'margins': dict}`
- **Per-row**: `{'hspace': list, 'wspace': list, 'margins': dict}`

---

"""
    
    # Add each test to the markdown
    for i, result in enumerate(results, 1):
        test = result['test']
        
        markdown_content += f"""## {test['name']}

{test['description']}

### Command

```python
{test['command']}
```

### Result

"""
        
        if result['filepath']:
            markdown_content += f"![{test['name']}]({result['filepath']})\n\n"
        else:
            markdown_content += f"**Error:** {result.get('error', 'Unknown error')}\n\n"
        
        markdown_content += "---\n\n"
    
    # Add summary
    successful = sum(1 for r in results if r['filepath'])
    markdown_content += f"""## Summary

- **Total Tests**: {len(results)}
- **Successful**: {successful}
- **Failed**: {len(results) - successful}

## Key Features Demonstrated

- ✅ **Backward Compatibility**: Original uniform API still works
- ✅ **Per-Row Heights**: Different subplot heights for each row
- ✅ **Per-Column Widths**: Different subplot widths for each column  
- ✅ **Variable Spacing**: Custom spacing between rows and columns
- ✅ **Mixed Specifications**: Combine uniform and per-row settings
- ✅ **Complex Layouts**: Multiple customizations in one layout
- ✅ **Visual Validation**: Each figure shows row/column indexing

## Usage Tips

1. **Start with uniform layouts** for simple cases
2. **Use per-row customization** when you need different subplot sizes
3. **Mix uniform and per-row** specifications as needed
4. **Check figure size requirements** - the function warns if subplots don't fit
5. **Use lists for spacing** to create visual grouping between subplots

"""
    
    # Write markdown file
    with open('per_row_subplot_examples.md', 'w') as f:
        f.write(markdown_content)
    
    print(f"\n✓ Generated markdown documentation: per_row_subplot_examples.md")


if __name__ == "__main__":
    print("=" * 60)
    print("Generating Per-Row Subplot Documentation")
    print("=" * 60)
    
    results = generate_markdown_docs()
    
    print("\n" + "=" * 60)
    print("Documentation Generation Complete")
    print("=" * 60)
    print(f"✓ Generated markdown file: per_row_subplot_examples.md")
    print(f"✓ Generated {len([r for r in results if r['filepath']])} test figures")
    print("=" * 60)

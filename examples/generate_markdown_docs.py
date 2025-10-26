"""
Generate markdown documentation with test figures and command examples.
All figures use 7" width and max 9" height.
"""

import matplotlib.pyplot as plt
from yplot.figure import (
    calculate_subplot_coordinates, 
    merge_adjacent_subplots,
    merge_subplot_blocks
)
from yplot.util import create_example_figure
import os




def generate_markdown_docs():
    """Generate markdown documentation with all test examples."""
    
    # Test configurations with their command codes - all using 7" width, max 9" height
    tests = [
        # NEW: Examples showing the row-based dictionary interface
        {
            'name': 'New Syntax 1: Row Dictionary Interface - Basic',
            'description': 'Demonstrates the new row-based dictionary interface using subplot_info parameter.',
            'command': '''coords = calculate_subplot_coordinates(
    fig_size_inches=(12, 10),
    subplot_info={
        'row_1': {'cols': 3, 'size': (2.5, 3.0), 'hspace': 0.3, 'wspace': 0.4},
        'row_2': {'cols': 2, 'size': (4.0, 2.0), 'hspace': 0.3, 'wspace': 0.3},
        'row_3': {'cols': 4, 'size': (1.8, 2.5), 'hspace': 0.3}
    }
)''',
            'function': lambda: calculate_subplot_coordinates(
                fig_size_inches=(12, 10),
                subplot_info={
                    'row_1': {'cols': 3, 'size': (2.5, 3.0), 'hspace': 0.3, 'wspace': 0.4},
                    'row_2': {'cols': 2, 'size': (4.0, 2.0), 'hspace': 0.3, 'wspace': 0.3},
                    'row_3': {'cols': 4, 'size': (1.8, 2.5), 'hspace': 0.3}
                }
            ),
            'layout': (3, 4),
            'fig_size': (12, 10),
            'filename': 'row_dict_interface_test.png'
        },
        {
            'name': 'New Syntax 2: Row Dictionary Interface - Complex Layout',
            'description': 'Demonstrates complex layout with different configurations for each row.',
            'command': '''coords = calculate_subplot_coordinates(
    fig_size_inches=(14, 12),
    subplot_info={
        'row_1': {'cols': 2, 'size': (3.0, 2.5), 'hspace': 0.3, 'wspace': 0.4},
        'row_2': {'cols': 4, 'size': (2.0, 2.0), 'hspace': 0.2, 'wspace': 0.3},
        'row_3': {'cols': 1, 'size': (4.0, 3.0), 'hspace': 0.0, 'wspace': 0.5},
        'row_4': {'cols': 3, 'size': (2.5, 1.8), 'hspace': 0.3}
    }
)''',
            'function': lambda: calculate_subplot_coordinates(
                fig_size_inches=(14, 12),
                subplot_info={
                    'row_1': {'cols': 2, 'size': (3.0, 2.5), 'hspace': 0.3, 'wspace': 0.4},
                    'row_2': {'cols': 4, 'size': (2.0, 2.0), 'hspace': 0.2, 'wspace': 0.3},
                    'row_3': {'cols': 1, 'size': (4.0, 3.0), 'hspace': 0.0, 'wspace': 0.5},
                    'row_4': {'cols': 3, 'size': (2.5, 1.8), 'hspace': 0.3}
                }
            ),
            'layout': (4, 4),
            'fig_size': (14, 12),
            'filename': 'complex_row_dict_test.png'
        },
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
        },
        {
            'name': 'Test 11: Merge Adjacent Subplots',
            'description': 'Merge adjacent subplots within a 3x3 grid to create larger subplots.',
            'command': '''# Create 3x3 grid
coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 6),
    subplot_layout=(3, 3),
    subplot_size_inches=(1.8, 1.5),
    spacing={'hspace': 0.2, 'wspace': 0.2, 'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}}
)

# Merge subplots 0 and 1 (top row, first two)
merged_coords = merge_adjacent_subplots(coords, [(0, 1)])
# Result: 8 subplots, with subplot 0 being twice as wide''',
            'function': lambda: merge_adjacent_subplots(
                calculate_subplot_coordinates(
                    fig_size_inches=(7, 6),
                    subplot_layout=(3, 3),
                    subplot_size_inches=(1.8, 1.5),
                    spacing={'hspace': 0.2, 'wspace': 0.2, 'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}}
                ),
                [(0, 1)]
            ),
            'layout': (3, 3),
            'fig_size': (7, 6),
            'filename': 'test_11_merge_adjacent.png'
        },
        {
            'name': 'Test 12: Merge Multiple Pairs',
            'description': 'Merge multiple pairs of adjacent subplots in a 3x3 grid.',
            'command': '''# Create 3x3 grid
coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 6),
    subplot_layout=(3, 3),
    subplot_size_inches=(1.8, 1.5),
    spacing={'hspace': 0.2, 'wspace': 0.2, 'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}}
)

# Merge multiple pairs: (0,1), (3,4), (6,7)
merged_coords = merge_adjacent_subplots(coords, [(0, 1), (3, 4), (6, 7)])
# Result: 6 subplots with 3 merged pairs''',
            'function': lambda: merge_adjacent_subplots(
                calculate_subplot_coordinates(
                    fig_size_inches=(7, 6),
                    subplot_layout=(3, 3),
                    subplot_size_inches=(1.8, 1.5),
                    spacing={'hspace': 0.2, 'wspace': 0.2, 'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}}
                ),
                [(0, 1), (3, 4), (6, 7)]
            ),
            'layout': (3, 3),
            'fig_size': (7, 6),
            'filename': 'test_12_merge_multiple_pairs.png'
        },
        {
            'name': 'Test 13: Merge 2x2 Block',
            'description': 'Merge a 2x2 block of subplots using merge_subplot_blocks.',
            'command': '''# Create 3x3 grid
coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 6),
    subplot_layout=(3, 3),
    subplot_size_inches=(1.8, 1.5),
    spacing={'hspace': 0.2, 'wspace': 0.2, 'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}}
)

# Merge a 2x2 block starting at subplot 0
merged_coords = merge_subplot_blocks(coords, [{
    'top_left': 0,
    'rows': 2,
    'cols': 2
}])
# Result: 5 subplots with one large 2x2 subplot''',
            'function': lambda: merge_subplot_blocks(
                calculate_subplot_coordinates(
                    fig_size_inches=(7, 6),
                    subplot_layout=(3, 3),
                    subplot_size_inches=(1.8, 1.5),
                    spacing={'hspace': 0.2, 'wspace': 0.2, 'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}}
                ),
                [{'top_left': 0, 'rows': 2, 'cols': 2}]
            ),
            'layout': (3, 3),
            'fig_size': (7, 6),
            'filename': 'test_13_merge_2x2_block.png'
        },
        {
            'name': 'Test 14: Complex Merging',
            'description': 'Complex merging with multiple blocks in a 4x4 grid.',
            'command': '''# Create 4x4 grid
coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 6),
    subplot_layout=(4, 4),
    subplot_size_inches=(1.2, 1.0),
    spacing={'hspace': 0.15, 'wspace': 0.15, 'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}}
)

# Merge multiple blocks:
# - 2x2 block at top-left (subplots 0,1,4,5)
# - 1x2 block at top-right (subplots 2,3)
# - 2x1 block at bottom-left (subplots 8,12)
merged_coords = merge_adjacent_subplots(coords, [
    (0, 1), (0, 4), (1, 5),  # 2x2 block at top-left
    (2, 3),                   # 1x2 block at top-right
    (8, 12)                   # 2x1 block at bottom-left
])
# Result: 12 subplots with multiple merged blocks''',
            'function': lambda: merge_adjacent_subplots(
                calculate_subplot_coordinates(
                    fig_size_inches=(7, 6),
                    subplot_layout=(4, 4),
                    subplot_size_inches=(1.2, 1.0),
                    spacing={'hspace': 0.15, 'wspace': 0.15, 'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}}
                ),
                [(0, 1), (0, 4), (1, 5), (2, 3), (8, 12)]
            ),
            'layout': (4, 4),
            'fig_size': (7, 6),
            'filename': 'test_14_complex_merging.png'
        },
        {
            'name': 'Test 15: Merge in Per-Row Layout',
            'description': 'Merge subplots in a per-row customized layout.',
            'command': '''# Create 3x3 grid with per-row customization
coords = calculate_subplot_coordinates(
    fig_size_inches=(7, 6),
    subplot_layout=(3, 3),
    subplot_size_inches={
        'row_heights': [2.0, 1.5, 1.0],  # Different row heights
        'col_widths': [1.8, 1.8, 1.8]
    },
    spacing={
        'hspace': [0.2, 0.2],  # Horizontal spacing
        'wspace': [0.3, 0.2],  # Vertical spacing
        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    }
)

# Merge subplots 0 and 1 (top row, first two)
merged_coords = merge_adjacent_subplots(coords, [(0, 1)])
# Result: 8 subplots with per-row customization preserved''',
            'function': lambda: merge_adjacent_subplots(
                calculate_subplot_coordinates(
                    fig_size_inches=(7, 6),
                    subplot_layout=(3, 3),
                    subplot_size_inches={
                        'row_heights': [2.0, 1.5, 1.0],
                        'col_widths': [1.8, 1.8, 1.8]
                    },
                    spacing={
                        'hspace': [0.2, 0.2],
                        'wspace': [0.3, 0.2],
                        'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
                    }
                ),
                [(0, 1)]
            ),
            'layout': (3, 3),
            'fig_size': (7, 6),
            'filename': 'test_15_merge_per_row.png'
        }
    ]
    
    # Generate figures and collect results
    results = []
    for i, test in enumerate(tests, 1):
        print(f"\nGenerating {test['name']}...")
        try:
            coords = test['function']()
            filepath = create_example_figure(
                coords, 
                f"{test['name']} ({test['layout'][0]}×{test['layout'][1]})",
                test['filename'],
                test['fig_size'],
                grid_layout=test['layout'],
                output_dir='docs/figures'
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

This document demonstrates the enhanced `calculate_subplot_coordinates` function that supports per-row and per-column customization of subplot layouts, including the new row-based dictionary interface.

## Overview

The updated function supports multiple interfaces for creating subplot layouts:

- **NEW: Row-based dictionary interface**: Use the `subplot_info` parameter for intuitive row-by-row configuration
- **Uniform layouts**: Use tuples for `subplot_size_inches` and single values for spacing (backward compatible)
- **Per-row customization**: Use dictionaries with lists for `row_heights`, `col_widths`, and spacing
- **Variable columns**: Specify different numbers of columns per row
- **Mixed specifications**: Combine uniform and per-row settings as needed

## NEW: Row-Based Dictionary Interface

The new `subplot_info` parameter provides an intuitive way to configure layouts row-by-row:

```python
coords = calculate_subplot_coordinates(
    fig_size_inches=(12, 10),
    subplot_info={
        'row_1': {'cols': 3, 'size': (2.5, 3.0), 'hspace': 0.3, 'wspace': 0.4},
        'row_2': {'cols': 2, 'size': (4.0, 2.0), 'hspace': 0.3, 'wspace': 0.3},
        'row_3': {'cols': 4, 'size': (1.8, 2.5), 'hspace': 0.3}
    }
)
```

### Row Configuration Options

Each row can specify:
- `cols`: Number of columns in this row
- `size`: (width, height) tuple for subplots in this row
- `hspace`: Horizontal spacing between subplots in this row (default: 0.3)
- `wspace`: Vertical spacing after this row, except the last row (default: 0.3)
- `margins`: Row-specific margins (optional, default: uniform margins)

## Legacy API Reference

### Function Signature
```python
calculate_subplot_coordinates(
    fig_size_inches,      # tuple: (width, height) in inches
    subplot_layout,       # tuple: (rows, columns) or list: columns per row
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
            # Convert filepath to relative path from docs directory
            relative_path = result['filepath'].replace('docs/figures/', 'figures/')
            markdown_content += f"![{test['name']}]({relative_path})\n\n"
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

- ✅ **NEW: Row-Based Dictionary Interface**: Intuitive row-by-row configuration with `subplot_info` parameter
- ✅ **Backward Compatibility**: Original uniform API still works
- ✅ **Per-Row Heights**: Different subplot heights for each row
- ✅ **Per-Column Widths**: Different subplot widths for each column  
- ✅ **Variable Spacing**: Custom spacing between rows and columns
- ✅ **Variable Columns**: Different number of columns per row
- ✅ **Mixed Specifications**: Combine uniform and per-row settings
- ✅ **Complex Layouts**: Multiple customizations in one layout
- ✅ **Visual Validation**: Each figure shows row/column indexing

## Usage Tips

1. **Try the new row-based interface** (`subplot_info`) for intuitive row-by-row configuration
2. **Start with uniform layouts** for simple cases
3. **Use per-row customization** when you need different subplot sizes
4. **Use the row dictionary interface** for complex layouts with varying column counts
5. **Mix uniform and per-row** specifications as needed
6. **Check figure size requirements** - the function warns if subplots don't fit
7. **Use lists for spacing** to create visual grouping between subplots

"""
    
    # Write markdown file
    os.makedirs('docs', exist_ok=True)
    with open('docs/per_row_subplot_examples.md', 'w') as f:
        f.write(markdown_content)
    
    print(f"\n✓ Generated markdown documentation: docs/per_row_subplot_examples.md")


if __name__ == "__main__":
    print("=" * 60)
    print("Generating Per-Row Subplot Documentation")
    print("=" * 60)
    
    results = generate_markdown_docs()
    
    print("\n" + "=" * 60)
    print("Documentation Generation Complete")
    print("=" * 60)
    print(f"✓ Generated markdown file: docs/per_row_subplot_examples.md")
    print(f"✓ Generated {len([r for r in results if r['filepath']])} test figures in docs/figures/")
    print("=" * 60)

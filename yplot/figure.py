from symbol import factor
import yaml
from pathlib import Path
from typing import Union, Dict, List, Tuple, Optional


class SubplotLayout:
    """
    Unified subplot layout configuration class that supports both dictionary and class-based configuration.
    
    This class can be initialized from:
    - Direct parameters (class-based)
    - Dictionary configuration
    - YAML file
    
    Parameters:
    -----------
    fig_size_inches : tuple, optional
        Figure size as (width, height) in inches
    rows : int, optional
        Number of rows in the subplot grid
    cols : int, optional
        Number of columns in the subplot grid
    config : dict, optional
        Configuration dictionary
    yaml_file : str or Path, optional
        Path to YAML configuration file
    
    Attributes:
    -----------
    fig_size_inches : tuple
        Figure size as (width, height) in inches
    rows : int
        Number of rows in the subplot grid
    cols : int
        Number of columns in the subplot grid
    row_heights : list of float
        Height in inches for each row
    col_widths : list of float
        Width in inches for each column
    wspace : list of float
        Vertical spacing in inches between rows
    hspace : list of float
        Horizontal spacing in inches between columns
    margins : dict
        Margins in inches: {'left': float, 'right': float, 'top': float, 'bottom': float}
    subplot_info : dict, optional
        Row-based configuration dictionary for complex layouts
    
    Examples:
    ---------
    # Single command with all parameters
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
    
    # From dictionary
    config = {'fig_size': [10, 8], 'rows': 2, 'cols': 3, 'row_heights': [3.0, 2.0]}
    layout = SubplotLayout(config=config)
    
    # From YAML file
    layout = SubplotLayout(yaml_file='my_layout.yaml')
    """
    
    def __init__(self, 
                 fig_size_inches: Optional[Tuple[float, float]] = None,
                 rows: Optional[int] = None,
                 cols: Optional[int] = None,
                 row_heights: Optional[List[float]] = None,
                 col_widths: Optional[List[float]] = None,
                 wspace: Optional[List[float]] = None,
                 hspace: Optional[List[float]] = None,
                 margins: Optional[Dict[str, float]] = None,
                 config: Optional[Dict] = None,
                 yaml_file: Optional[Union[str, Path]] = None):
        
        # Initialize with defaults
        self.fig_size_inches = None
        self.rows = None
        self.cols = None
        self.row_heights = []
        self.col_widths = []
        self.wspace = []
        self.hspace = []
        self.margins = {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75}
        self.subplot_info = None
        
        # Handle different initialization methods
        if yaml_file is not None:
            self._load_from_yaml(yaml_file)
        elif config is not None:
            self._load_from_dict(config)
        elif fig_size_inches is not None and rows is not None and cols is not None:
            self._load_from_parameters(fig_size_inches, rows, cols, row_heights, col_widths, wspace, hspace, margins)
        else:
            raise ValueError("Must provide either yaml_file, config, or fig_size_inches+rows+cols")
    
    def _load_from_yaml(self, yaml_file: Union[str, Path]):
        """Load configuration from YAML file."""
        yaml_path = Path(yaml_file)
        if not yaml_path.exists():
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")
        
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self._load_from_dict(config)
    
    def _load_from_dict(self, config: Dict):
        """Load configuration from dictionary."""
        # Check if this is a row-based configuration (row_1, row_2, etc.)
        # Only use row-based format if there's no 'rows' or 'cols' key (backward compatibility)
        row_keys = [k for k in config.keys() if k.startswith('row_')]
        has_traditional_keys = 'rows' in config or 'cols' in config
        
        if row_keys and not has_traditional_keys:
            # This is a row-based configuration
            self.fig_size_inches = tuple(config.get('fig_size', config.get('fig_size_inches', (10, 8))))
            self.subplot_info = config  # Store the entire config as subplot_info
            self.rows = len(row_keys)
            # Set default values for other attributes
            self.cols = None  # Will be determined from row configs
            self.row_heights = []
            self.col_widths = []
            self.wspace = []
            self.hspace = []
            self.margins = config.get('margins', {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75})
            return
        
        # Handle different dictionary formats
        if 'fig_size' in config:
            self.fig_size_inches = tuple(config['fig_size'])
        elif 'fig_size_inches' in config:
            self.fig_size_inches = tuple(config['fig_size_inches'])
        else:
            raise ValueError("Configuration must contain 'fig_size' or 'fig_size_inches'")
        
        self.rows = config.get('rows', 1)
        self.cols = config.get('cols', 1)
        
        # Set default values
        self.row_heights = config.get('row_heights', [2.0] * self.rows)
        self.col_widths = config.get('col_widths', [2.0] * self.cols)
        self.wspace = config.get('wspace', [0.5] * (self.rows - 1) if self.rows > 1 else [])
        self.hspace = config.get('hspace', [0.5] * (self.cols - 1) if self.cols > 1 else [])
        self.margins = config.get('margins', self.margins)
        
        # Handle complex subplot_info format
        self.subplot_info = config.get('subplot_info', None)
    
    
    def _load_from_parameters(self, fig_size_inches: Tuple[float, float], rows: int, cols: int,
                             row_heights: Optional[List[float]] = None,
                             col_widths: Optional[List[float]] = None,
                             wspace: Optional[List[float]] = None,
                             hspace: Optional[List[float]] = None,
                             margins: Optional[Dict[str, float]] = None):
        """Load configuration from direct parameters."""
        self.fig_size_inches = tuple(fig_size_inches)
        self.rows = rows
        self.cols = cols
        
        # Set row heights
        if row_heights is not None:
            if len(row_heights) != rows:
                raise ValueError(f"row_heights must have {rows} elements, got {len(row_heights)}")
            self.row_heights = row_heights
        else:
            self.row_heights = [2.0] * rows
        
        # Set column widths
        if col_widths is not None:
            if len(col_widths) != cols:
                raise ValueError(f"col_widths must have {cols} elements, got {len(col_widths)}")
            self.col_widths = col_widths
        else:
            self.col_widths = [2.0] * cols
        
        # Set vertical spacing (between rows)
        if wspace is not None:
            if rows > 1 and len(wspace) != rows - 1:
                raise ValueError(f"wspace must have {rows - 1} elements, got {len(wspace)}")
            self.wspace = wspace
        else:
            self.wspace = [0.5] * (rows - 1) if rows > 1 else []
        
        # Set horizontal spacing (between columns)
        if hspace is not None:
            if cols > 1 and len(hspace) != cols - 1:
                raise ValueError(f"hspace must have {cols - 1} elements, got {len(hspace)}")
            self.hspace = hspace
        else:
            self.hspace = [0.5] * (cols - 1) if cols > 1 else []
        
        # Set margins
        if margins is not None:
            self.margins = margins
    
    def to_dict(self) -> Dict:
        """Convert configuration to a dictionary."""
        result = {
            'fig_size': list(self.fig_size_inches),
            'rows': self.rows,
            'cols': self.cols,
            'row_heights': self.row_heights,
            'col_widths': self.col_widths,
            'wspace': self.wspace,
            'hspace': self.hspace,
            'margins': self.margins
        }
        
        if self.subplot_info is not None:
            result['subplot_info'] = self.subplot_info
        
        return result
    
    def to_yaml(self, yaml_file: Union[str, Path]):
        """Save configuration to YAML file."""
        yaml_path = Path(yaml_file)
        yaml_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(yaml_path, 'w') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, indent=2)
    
    def get_coordinates(self, cols_per_row: Optional[List[int]] = None) -> List[Tuple[float, float, float, float]]:
        """
        Calculate subplot coordinates based on the configuration.
        
        Parameters:
        -----------
        cols_per_row : list, optional
            Number of columns in each row. If None, uses uniform grid.
            If provided, allows different numbers of subplots per row.
        
        Returns:
        --------
        list
            List of tuples, each containing (left, bottom, width, height) coordinates
            in figure-relative units (0-1) for each subplot, ordered row by row.
        """
        # Use subplot_info if available (complex layout)
        if self.subplot_info is not None:
            return _calculate_row_dict_coordinates(self.fig_size_inches, self.subplot_info)
        
        # Use standard layout calculation
        import warnings
        
        fig_width, fig_height = self.fig_size_inches
        
        # Use uniform grid if cols_per_row not provided
        if cols_per_row is None:
            cols_per_row = [self.cols] * self.rows
        
        # Validate list lengths
        if len(self.row_heights) != self.rows:
            raise ValueError(f"row_heights must have {self.rows} elements, got {len(self.row_heights)}")
        if len(cols_per_row) != self.rows:
            raise ValueError(f"cols_per_row must have {self.rows} elements, got {len(cols_per_row)}")
        if self.rows > 1 and len(self.wspace) != self.rows - 1:
            raise ValueError(f"wspace must have {self.rows - 1} elements, got {len(self.wspace)}")
        
        # Calculate total space needed
        total_subplot_height = sum(self.row_heights)
        total_wspace = sum(self.wspace)
        total_margins_height = self.margins["top"] + self.margins["bottom"]
        
        # For width calculation, we need to consider the maximum number of columns
        max_cols = max(cols_per_row)
        if len(self.col_widths) != max_cols:
            raise ValueError(f"col_widths must have {max_cols} elements, got {len(self.col_widths)}")
        
        # Calculate total width needed (using max columns for validation)
        total_subplot_width = sum(self.col_widths)
        total_hspace = sum(self.hspace) if len(self.hspace) > 0 else 0
        total_margins_width = self.margins["left"] + self.margins["right"]
        
        required_width = total_subplot_width + total_hspace + total_margins_width
        required_height = total_subplot_height + total_wspace + total_margins_height
        
        # Warn if layout doesn't fit
        if required_width > fig_width or required_height > fig_height:
            warnings.warn(
                f"Subplot layout requires {required_width:.2f}x{required_height:.2f} inches "
                f"but figure is {fig_width:.2f}x{fig_height:.2f} inches. Subplots may overlap."
            )
        
        # Calculate coordinates
        coordinates = []
        
        # Calculate cumulative positions for rows (from bottom to top)
        row_bottoms = []
        current_bottom = self.margins["bottom"]
        for row in range(self.rows - 1, -1, -1):  # Start from bottom row
            row_bottoms.insert(0, current_bottom)  # Insert at beginning
            current_bottom += self.row_heights[row]
            if row > 0:  # Add spacing if not the top row
                current_bottom += self.wspace[row - 1]
        
        # Generate coordinates for each subplot
        for row in range(self.rows):
            num_cols_in_row = cols_per_row[row]
            
            # Calculate column positions for this row
            col_lefts = []
            current_left = self.margins["left"]
            for col in range(num_cols_in_row):
                col_lefts.append(current_left)
                current_left += self.col_widths[col]
                if col < num_cols_in_row - 1:  # Add spacing if not the last column
                    current_left += self.hspace[col] if col < len(self.hspace) else 0
            
            # Generate coordinates for subplots in this row
            for col in range(num_cols_in_row):
                left_inches = col_lefts[col]
                bottom_inches = row_bottoms[row]
                width_inches = self.col_widths[col]
                height_inches = self.row_heights[row]
                
                # Convert to figure-relative coordinates (0-1)
                left_rel = left_inches / fig_width
                bottom_rel = bottom_inches / fig_height
                width_rel = width_inches / fig_width
                height_rel = height_inches / fig_height
                
                coordinates.append((left_rel, bottom_rel, width_rel, height_rel))
        
        return coordinates


def generate_subplot_coordinates_from_dict(config: Dict) -> List[Tuple[float, float, float, float]]:
    """
    Generate subplot coordinates from a dictionary configuration.
    
    This function provides a clean interface for generating subplot coordinates
    directly from a dictionary without needing to create a SubplotLayout object.
    
    Parameters:
    -----------
    config : dict
        Configuration dictionary. Can use either the row-based format (row_1, row_2, etc.)
        or the standard format with rows, cols, etc.
    
    Returns:
    --------
    list
        List of tuples, each containing (left, bottom, width, height) coordinates
        in figure-relative units (0-1) for each subplot
    
    Examples:
    ---------
    # Row-based configuration
    layout_dict = {
        "fig_size": (7, 2),
        "row_1": {
            "size": (1.3, 1.3), 
            "hspace": 0.45,
            "wspace": 0.50,
            "margins": {"left": 0.40, "right": 0.0, "top": 0.0, "bottom": 0.50},
            "cols": 4
        }
    }
    coords = generate_subplot_coordinates_from_dict(layout_dict)
    
    # Standard configuration
    layout_dict = {
        "fig_size_inches": (10, 8),
        "rows": 2,
        "cols": 3,
        "row_heights": [3.0, 2.0],
        "col_widths": [2.5, 2.5, 2.5]
    }
    coords = generate_subplot_coordinates_from_dict(layout_dict)
    """
    layout = SubplotLayout(config=config)
    return layout.get_coordinates()


def _calculate_row_dict_coordinates(fig_size_inches, subplot_info):
    """
    Calculate coordinates using row-based dictionary interface.
    
    Parameters:
    -----------
    fig_size_inches : tuple
        Figure size as (width, height) in inches
    subplot_info : dict
        Row-based configuration dictionary
        
    Returns:
    --------
    list
        List of tuples, each containing (left, bottom, width, height) coordinates
        in figure-relative units (0-1) for each subplot
    """
    import warnings
    
    fig_width, fig_height = fig_size_inches
    
    # Parse row information
    rows = []
    row_keys = sorted([k for k in subplot_info.keys() if k.startswith('row_')])
    
    if not row_keys:
        raise ValueError("subplot_info must contain at least one 'row_X' key")
    
    for row_key in row_keys:
        row_data = subplot_info[row_key]
        
        # Validate required fields
        if 'cols' not in row_data or 'size' not in row_data:
            raise ValueError(f"{row_key} must contain 'cols' and 'size' fields")
        
        # Extract row information
        cols = row_data['cols']
        size = row_data['size']
        hspace = row_data.get('hspace', 0.3)
        wspace = row_data.get('wspace', 0.3)
        margins = row_data.get('margins', {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75})
        
        if not isinstance(size, (tuple, list)) or len(size) != 2:
            raise ValueError(f"{row_key} 'size' must be a tuple/list of (width, height)")
        
        rows.append({
            'cols': cols,
            'width': size[0],
            'height': size[1],
            'hspace': hspace,
            'wspace': wspace,
            'margins': margins
        })
    
    # Calculate total space needed
    total_height = sum(row['height'] for row in rows)
    total_wspace = sum(row['wspace'] for row in rows[:-1])  # No wspace after last row
    total_margins_height = rows[0]['margins']['top'] + rows[-1]['margins']['bottom']
    
    required_height = total_height + total_wspace + total_margins_height
    
    # Warn if layout doesn't fit
    if required_height > fig_height:
        warnings.warn(
            f"Subplot layout requires {required_height:.2f} inches height "
            f"but figure is {fig_height:.2f} inches. Subplots may overlap."
        )
    
    # Calculate coordinates
    coordinates = []
    
    # Calculate cumulative positions for rows (from bottom to top)
    row_bottoms = []
    current_bottom = rows[-1]['margins']['bottom']  # Start from bottom row margin
    
    for row_idx in range(len(rows) - 1, -1, -1):  # Start from bottom row
        row_bottoms.insert(0, current_bottom)  # Insert at beginning
        current_bottom += rows[row_idx]['height']
        if row_idx > 0:  # Add spacing if not the top row
            current_bottom += rows[row_idx - 1]['wspace']
    
    # Generate coordinates for each subplot
    for row_idx, row in enumerate(rows):
        num_cols_in_row = row['cols']
        row_height = row['height']
        subplot_width = row['width']
        hspace = row['hspace']
        
        # Calculate column positions for this row
        col_lefts = []
        current_left = row['margins']['left']
        
        for col in range(num_cols_in_row):
            col_lefts.append(current_left)
            current_left += subplot_width
            if col < num_cols_in_row - 1:  # Add spacing if not the last column
                current_left += hspace
        
        # Generate coordinates for subplots in this row
        for col in range(num_cols_in_row):
            left_inches = col_lefts[col]
            bottom_inches = row_bottoms[row_idx]
            width_inches = subplot_width
            height_inches = row_height
            
            # Convert to figure-relative coordinates (0-1)
            left_rel = left_inches / fig_width
            bottom_rel = bottom_inches / fig_height
            width_rel = width_inches / fig_width
            height_rel = height_inches / fig_height
            
            coordinates.append((left_rel, bottom_rel, width_rel, height_rel))
    
    return coordinates


def create_merged_layout(fig_size_inches, layouts, merge_direction='horizontal', spacing=0.1):
    """
    Create a merged layout from multiple subplot layout configurations.
    
    This is a convenience function that combines multiple SubplotLayout
    objects into a single coordinate list.
    
    Parameters:
    -----------
    fig_size_inches : tuple
        Figure size as (width, height) in inches
    layouts : list of SubplotLayout
        List of SubplotLayout objects to merge
    merge_direction : str, optional
        Direction to merge layouts: 'horizontal' or 'vertical' (default: 'horizontal')
    spacing : float, optional
        Spacing between merged layouts in inches (default: 0.1)
    
    Returns:
    --------
    list
        Merged list of tuples containing (left, bottom, width, height) coordinates
        in figure-relative units (0-1)
    
    Examples:
    ---------
    # Create two layouts
    layout1 = SubplotLayout(fig_size_inches=(7, 4), rows=2, cols=2)
    layout2 = SubplotLayout(fig_size_inches=(7, 4), rows=2, cols=3)
    
    # Merge them horizontally
    merged_coords = create_merged_layout(
        fig_size_inches=(14, 4),
        layouts=[layout1, layout2],
        merge_direction='horizontal',
        spacing=0.2
    )
    """
    coordinate_lists = [calculate_subplot_coordinates(layout) for layout in layouts]
    
    if not coordinate_lists:
        return []
    
    if len(coordinate_lists) == 1:
        return coordinate_lists[0]
    
    # Convert spacing from inches to relative units
    if merge_direction == 'horizontal':
        spacing_rel = spacing / 7.0  # Convert to relative width
    else:  # vertical
        spacing_rel = spacing / 9.0  # Convert to relative height
    
    merged_coords = []
    
    if merge_direction == 'horizontal':
        # Place coordinate lists side by side
        current_left = 0.0
        
        for coord_list in coordinate_lists:
            if not coord_list:
                continue
                
            # Find the maximum width in this coordinate list
            max_right = max(left + width for left, bottom, width, height in coord_list)
            
            # Scale and offset coordinates
            for left, bottom, width, height in coord_list:
                new_left = current_left + left
                merged_coords.append((new_left, bottom, width, height))
            
            # Move to next position
            current_left = max_right + spacing_rel
    
    else:  # vertical
        # Stack coordinate lists on top of each other
        current_bottom = 0.0
        
        for coord_list in coordinate_lists:
            if not coord_list:
                continue
                
            # Find the maximum height in this coordinate list
            max_top = max(bottom + height for left, bottom, width, height in coord_list)
            
            # Scale and offset coordinates
            for left, bottom, width, height in coord_list:
                new_bottom = current_bottom + bottom
                merged_coords.append((left, new_bottom, width, height))
            
            # Move to next position
            current_bottom = max_top + spacing_rel
    
    return merged_coords


def merge_adjacent_subplots(coordinates, merge_pairs):
    """
    Merge adjacent subplots within a coordinate list to create larger subplots.
    
    This function allows you to combine adjacent subplots in a grid to create
    larger subplots, useful for creating complex layouts with varying subplot sizes.
    
    Parameters:
    -----------
    coordinates : list
        List of (left, bottom, width, height) coordinate tuples
    merge_pairs : list of tuples
        List of (index1, index2) pairs to merge. Each pair specifies which
        subplots to combine. The first subplot's coordinates will be expanded
        to encompass both subplots, and the second will be removed.
    
    Returns:
    --------
    list
        Modified coordinate list with merged subplots
    
    Examples:
    ---------
    # In a 3x3 grid (9 subplots), merge subplots 0 and 1 (top row, first two)
    coords = calculate_subplot_coordinates(...)  # 3x3 grid
    merged = merge_adjacent_subplots(coords, [(0, 1)])
    # Result: 8 subplots, with subplot 0 being twice as wide
    
    # Merge multiple pairs
    merged = merge_adjacent_subplots(coords, [(0, 1), (3, 4), (6, 7)])
    # Result: 6 subplots with 3 merged pairs
    
    # Merge a 2x2 block (subplots 0, 1, 3, 4)
    merged = merge_adjacent_subplots(coords, [(0, 1), (0, 3), (1, 4)])
    # Result: 5 subplots with one large 2x2 subplot
    """
    if not coordinates or not merge_pairs:
        return coordinates
    
    # Create a copy to avoid modifying the original
    merged_coords = list(coordinates)
    
    # Sort merge pairs by first index to process in order
    merge_pairs = sorted(merge_pairs, key=lambda x: x[0])
    
    # Track which subplots have been merged (to be removed)
    removed_indices = set()
    
    for idx1, idx2 in merge_pairs:
        # Skip if either subplot is already removed
        if idx1 in removed_indices or idx2 in removed_indices:
            continue
        
        # Skip if indices are out of range
        if idx1 >= len(merged_coords) or idx2 >= len(merged_coords):
            continue
        
        # Get coordinates for both subplots
        left1, bottom1, width1, height1 = merged_coords[idx1]
        left2, bottom2, width2, height2 = merged_coords[idx2]
        
        # Calculate the bounding box that encompasses both subplots
        min_left = min(left1, left2)
        min_bottom = min(bottom1, bottom2)
        max_right = max(left1 + width1, left2 + width2)
        max_top = max(bottom1 + height1, bottom2 + height2)
        
        # Create merged subplot coordinates
        merged_left = min_left
        merged_bottom = min_bottom
        merged_width = max_right - min_left
        merged_height = max_top - min_bottom
        
        # Update the first subplot with merged coordinates
        merged_coords[idx1] = (merged_left, merged_bottom, merged_width, merged_height)
        
        # Mark the second subplot for removal
        removed_indices.add(idx2)
    
    # Remove merged subplots (in reverse order to maintain indices)
    for idx in sorted(removed_indices, reverse=True):
        merged_coords.pop(idx)
    
    return merged_coords


def merge_subplot_blocks(coordinates, block_merges):
    """
    Merge rectangular blocks of subplots within a coordinate list.
    
    This function allows you to merge rectangular blocks of subplots,
    useful for creating complex layouts with large subplots.
    
    Parameters:
    -----------
    coordinates : list
        List of (left, bottom, width, height) coordinate tuples
    block_merges : list of dict
        List of merge specifications. Each dict should contain:
        - 'top_left': index of top-left subplot in the block
        - 'bottom_right': index of bottom-right subplot in the block
        - 'rows': number of rows in the block
        - 'cols': number of columns in the block
    
    Returns:
    --------
    list
        Modified coordinate list with merged blocks
    
    Examples:
    ---------
    # In a 3x3 grid, merge a 2x2 block starting at subplot 0
    coords = calculate_subplot_coordinates(...)  # 3x3 grid
    merged = merge_subplot_blocks(coords, [{
        'top_left': 0,
        'bottom_right': 4,  # subplot 4 is bottom-right of 2x2 block starting at 0
        'rows': 2,
        'cols': 2
    }])
    # Result: 5 subplots with one large 2x2 subplot
    """
    if not coordinates or not block_merges:
        return coordinates
    
    # Create a copy to avoid modifying the original
    merged_coords = list(coordinates)
    
    # Track which subplots have been merged (to be removed)
    removed_indices = set()
    
    for block in block_merges:
        top_left_idx = block['top_left']
        rows = block['rows']
        cols = block['cols']
        
        # Calculate the indices of all subplots in this block
        block_indices = []
        for row in range(rows):
            for col in range(cols):
                # Assuming the grid is row-major (subplots filled left-to-right, top-to-bottom)
                # This is a simplified calculation - you might need to adjust based on your grid layout
                idx = top_left_idx + row * cols + col
                if idx < len(merged_coords):
                    block_indices.append(idx)
        
        if not block_indices:
            continue
        
        # Skip if any subplot in the block is already removed
        if any(idx in removed_indices for idx in block_indices):
            continue
        
        # Get coordinates for all subplots in the block
        block_coords = [merged_coords[idx] for idx in block_indices]
        
        # Calculate the bounding box that encompasses all subplots in the block
        min_left = min(left for left, bottom, width, height in block_coords)
        min_bottom = min(bottom for left, bottom, width, height in block_coords)
        max_right = max(left + width for left, bottom, width, height in block_coords)
        max_top = max(bottom + height for left, bottom, width, height in block_coords)
        
        # Create merged subplot coordinates
        merged_left = min_left
        merged_bottom = min_bottom
        merged_width = max_right - min_left
        merged_height = max_top - min_bottom
        
        # Update the first subplot with merged coordinates
        merged_coords[top_left_idx] = (merged_left, merged_bottom, merged_width, merged_height)
        
        # Mark all other subplots in the block for removal
        for idx in block_indices[1:]:
            removed_indices.add(idx)
    
    # Remove merged subplots (in reverse order to maintain indices)
    for idx in sorted(removed_indices, reverse=True):
        merged_coords.pop(idx)
    
    return merged_coords


def calculate_row_spacing(fig_size_inches, num_sub_plots, figure_width, margins=None, min_spacing=0.1):
    """
    Calculate the required spacing between figures in a row given figure size and count.
    
    This function determines what the horizontal spacing must be between figures in a row
    to fit them all within the given figure size, and warns if it's not possible.
    
    Parameters:
    -----------
    fig_size_inches : tuple
        Figure size as (width, height) in inches
    num_sub_plots : int
        Number of subplots to fit in the row
    figure_width : float
        Width of each individual figure in inches
    margins : dict, optional
        Margins in inches: {'left': float, 'right': float}
        Default: {'left': 0.75, 'right': 0.75}
    min_spacing : float, optional
        Minimum acceptable spacing between figures in inches (default: 0.1)
    
    Returns:
    --------
    float
        Required spacing between figures in inches. Returns None if not possible.
    
    Examples:
    ---------
    # Calculate spacing for 3 figures of width 2.5 inches in a 10-inch wide figure
    spacing = calculate_row_spacing(
        fig_size_inches=(10, 6),
        num_sub_plots=3,
        figure_width=2.5
    )
    # Returns: 0.5 (inches between each figure)
    
    # With custom margins
    spacing = calculate_row_spacing(
        fig_size_inches=(12, 8),
        num_sub_plots=4,
        figure_width=2.0,
        margins={'left': 1.0, 'right': 1.0}
    )
    """
    import warnings
    
    if num_sub_plots <= 0:
        raise ValueError("num_figures must be positive")
    
    if figure_width <= 0:
        raise ValueError("figure_width must be positive")
    
    if min_spacing < 0:
        raise ValueError("min_spacing must be non-negative")
    
    # Set default margins if not provided
    if margins is None:
        margins = {'left': 0.4, 'right': 0.0}
    
    fig_width = fig_size_inches[0]
    
    # Calculate total space needed for figures
    total_figure_width = num_sub_plots * figure_width
    
    # Calculate total space needed for margins
    total_margin_width = margins['left'] + margins['right']
    
    # Calculate available space for spacing
    available_space = fig_width - total_figure_width - total_margin_width
    
    # Check if it's possible to fit the figures
    if available_space < 0:
        warnings.warn(
            f"Cannot fit {num_sub_plots} figures of width {figure_width:.2f} inches "
            f"in a figure of width {fig_width:.2f} inches with margins "
            f"left={margins['left']:.2f}, right={margins['right']:.2f}. "
            f"Total required width: {total_figure_width + total_margin_width:.2f} inches."
        )
        return None
    
    # Calculate spacing between figures
    if num_sub_plots == 1:
        # Only one figure, no spacing needed
        spacing = 0.0
    else:
        # Divide available space by number of gaps between figures
        num_gaps = num_sub_plots - 1
        spacing = available_space / num_gaps
        
        # Check if spacing meets minimum requirement (only for multiple figures)
        if spacing < min_spacing:
            warnings.warn(
                f"Calculated spacing {spacing:.3f} inches is less than minimum "
                f"required spacing {min_spacing:.3f} inches. Consider reducing "
                f"figure width, number of figures, or margins."
            )
            return None
    
    return spacing


def convert_coordinates_to_inches(coordinates, fig_size_inches):
    """
    Convert coordinate lists from figure-relative units (0-1) to actual inch measurements.
    
    This function takes subplot coordinates in figure-relative units (0-1) and converts
    them to actual inch measurements based on the figure size. This is useful when you
    need to know the actual physical dimensions of subplots for printing, layout planning,
    or other applications that require inch-based measurements.
    
    Parameters:
    -----------
    coordinates : tuple or list of tuples
        Subplot coordinates as (left, bottom, width, height) in figure-relative units (0-1).
        Can be a single tuple or list of tuples.
    fig_size_inches : tuple
        Figure size as (width, height) in inches
        
    Returns:
    --------
    tuple or list of tuples
        Converted coordinates as (left, bottom, width, height) in inches.
        Returns the same type as input (single tuple or list of tuples).
        
    Examples:
    ---------
    # Convert a single subplot coordinate
    coord = (0.1, 0.2, 0.3, 0.4)  # Relative units
    inch_coord = convert_coordinates_to_inches(coord, fig_size_inches=(10, 8))
    # Result: (1.0, 1.6, 3.0, 3.2) inches
    
    # Convert multiple subplot coordinates
    coords = [(0.1, 0.1, 0.3, 0.3), (0.6, 0.6, 0.3, 0.3)]
    inch_coords = convert_coordinates_to_inches(coords, fig_size_inches=(12, 10))
    # Result: [(1.2, 1.0, 3.6, 3.0), (7.2, 6.0, 3.6, 3.0)] inches
    
    # Calculate actual subplot dimensions
    coord = (0.2, 0.3, 0.4, 0.5)
    inch_coord = convert_coordinates_to_inches(coord, fig_size_inches=(8, 6))
    width_inches, height_inches = inch_coord[2], inch_coord[3]
    print(f"Subplot is {width_inches:.2f} inches wide and {height_inches:.2f} inches tall")
    """
    fig_width, fig_height = fig_size_inches
    
    def convert_single_coordinate(coord):
        """Convert a single coordinate tuple from relative to inch units."""
        left_rel, bottom_rel, width_rel, height_rel = coord
        
        # Convert to inches
        left_inches = left_rel * fig_width
        bottom_inches = bottom_rel * fig_height
        width_inches = width_rel * fig_width
        height_inches = height_rel * fig_height
        
        return (left_inches, bottom_inches, width_inches, height_inches)
    
    # Handle single coordinate or list of coordinates
    if isinstance(coordinates, tuple):
        return convert_single_coordinate(coordinates)
    elif isinstance(coordinates, list):
        return [convert_single_coordinate(coord) for coord in coordinates]
    else:
        raise ValueError("coordinates must be a tuple or list of tuples")


def expand_subplot_coordinates(coordinates, fig_size_inches, margins=None, spacing=None, include_adjacent_spacing=False):
    """
    Expand subplot coordinates to include margins and spacing around them.
    
    This function takes subplot coordinates and expands them to include the margins
    and spacing that would be around them if they were part of a larger figure layout.
    This is useful when you want to insert a figure into a specific subplot position
    and need to know the full area including margins and spacing.
    
    Parameters:
    -----------
    coordinates : tuple or list of tuples
        Subplot coordinates as (left, bottom, width, height) in figure-relative units (0-1).
        Can be a single tuple or list of tuples.
    fig_size_inches : tuple
        Figure size as (width, height) in inches
    margins : dict, optional
        Margins in inches: {'left': float, 'right': float, 'top': float, 'bottom': float}
        Default: {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75}
    spacing : dict, optional
        Spacing parameters. Can be:
        - Simple: {'hspace': float, 'wspace': float} - uniform spacing
        - Per-row: {'hspace': list, 'wspace': list} - per-row/col spacing
        Default: {'hspace': 0.5, 'wspace': 0.5}
    include_adjacent_spacing : bool, optional
        Whether to include spacing from adjacent subplots. If True, includes half
        the spacing on each side. If False, only includes margins.
        Default: True
    
    Returns:
    --------
    tuple or list of tuples
        Expanded coordinates as (left, bottom, width, height) in figure-relative units (0-1).
        Returns the same type as input (single tuple or list of tuples).
    
    Examples:
    ---------
    # Expand a single subplot coordinate
    coord = (0.1, 0.1, 0.3, 0.3)  # Basic subplot
    expanded = expand_subplot_coordinates(
        coord, 
        fig_size_inches=(10, 8),
        margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5},
        spacing={'hspace': 0.3, 'wspace': 0.3}
    )
    # Result: expanded coordinates including margins and spacing
    
    # Expand multiple subplot coordinates
    coords = [(0.1, 0.1, 0.3, 0.3), (0.5, 0.1, 0.3, 0.3)]
    expanded = expand_subplot_coordinates(
        coords,
        fig_size_inches=(10, 8),
        margins={'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}
    )
    # Result: list of expanded coordinates
    
    # Expand without adjacent spacing (margins only)
    expanded = expand_subplot_coordinates(
        coord,
        fig_size_inches=(10, 8),
        include_adjacent_spacing=False
    )
    # Result: coordinates expanded only by margins
    """
    import warnings
    
    # Set default values
    if margins is None:
        margins = {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75}
    
    if spacing is None:
        spacing = {'hspace': 0.5, 'wspace': 0.5}
    
    fig_width, fig_height = fig_size_inches
    
    # Convert margins from inches to relative units
    margin_left_rel = margins['left'] / fig_width
    margin_right_rel = margins['right'] / fig_width
    margin_top_rel = margins['top'] / fig_height
    margin_bottom_rel = margins['bottom'] / fig_height
    
    # Handle spacing
    hspace = spacing.get('hspace', 0.5)
    wspace = spacing.get('wspace', 0.5)
    
    # Convert spacing from inches to relative units
    if isinstance(hspace, list):
        # Use average spacing for horizontal
        hspace_rel = sum(hspace) / len(hspace) / fig_width
    else:
        hspace_rel = hspace / fig_width
    
    if isinstance(wspace, list):
        # Use average spacing for vertical
        wspace_rel = sum(wspace) / len(wspace) / fig_height
    else:
        wspace_rel = wspace / fig_height
    
    # Calculate expansion amounts
    if include_adjacent_spacing:
        # Include half the spacing on each side
        expand_left = margin_left_rel + hspace_rel / 2
        expand_right = margin_right_rel + hspace_rel / 2
        expand_top = margin_top_rel + wspace_rel / 2
        expand_bottom = margin_bottom_rel + wspace_rel / 2
    else:
        # Only include margins
        expand_left = margin_left_rel
        expand_right = margin_right_rel
        expand_top = margin_top_rel
        expand_bottom = margin_bottom_rel
    
    def expand_single_coordinate(coord):
        """Expand a single coordinate tuple."""
        left, bottom, width, height = coord
        
        # Calculate expanded coordinates
        expanded_left = max(0.0, left - expand_left)
        expanded_bottom = max(0.0, bottom - expand_bottom)
        expanded_width = min(1.0 - expanded_left, width + expand_left + expand_right)
        expanded_height = min(1.0 - expanded_bottom, height + expand_bottom + expand_top)
        
        # Ensure coordinates are valid
        if expanded_width <= 0 or expanded_height <= 0:
            warnings.warn(
                f"Expanded coordinates result in zero or negative size: "
                f"width={expanded_width:.4f}, height={expanded_height:.4f}. "
                f"Original: {coord}"
            )
        
        return (expanded_left, expanded_bottom, expanded_width, expanded_height)
    
    # Handle single coordinate or list of coordinates
    if isinstance(coordinates, tuple):
        return expand_single_coordinate(coordinates)
    elif isinstance(coordinates, list):
        return [expand_single_coordinate(coord) for coord in coordinates]
    else:
        raise ValueError("coordinates must be a tuple or list of tuples")


def calculate_subplot_coordinates(layout: SubplotLayout, cols_per_row: Optional[List[int]] = None) -> List[Tuple[float, float, float, float]]:
    """
    Calculate subplot coordinates from a SubplotLayout configuration.
    
    This is a convenience wrapper function that calls the get_coordinates method
    on a SubplotLayout object.
    
    Parameters:
    -----------
    layout : SubplotLayout
        SubplotLayout object containing the configuration
    cols_per_row : list, optional
        Number of columns in each row. If None, uses uniform grid.
        If provided, allows different numbers of subplots per row.
    
    Returns:
    --------
    list
        List of tuples, each containing (left, bottom, width, height) coordinates
        in figure-relative units (0-1) for each subplot, ordered row by row.
    
    Examples:
    ---------
    # From SubplotLayout object
    layout = SubplotLayout(fig_size_inches=(10, 8), rows=2, cols=3)
    layout.row_heights = [3.0, 2.0]
    layout.col_widths = [2.5, 2.5, 2.5]
    layout.wspace = [0.5]
    layout.hspace = [0.3, 0.3]
    
    coords = calculate_subplot_coordinates(layout)
    # Returns: [(0.075, 0.54375, 0.25, 0.375), (0.3375, 0.54375, 0.25, 0.375), ...]
    """
    return layout.get_coordinates(cols_per_row)
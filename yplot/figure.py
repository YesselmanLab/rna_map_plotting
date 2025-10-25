class SubplotLayoutConfig:
    """
    Configuration class for flexible subplot layout with per-row/column customization.
    
    This class allows you to specify different sizes, spacing, and margins for each
    row and column independently.
    
    Parameters:
    -----------
    fig_size_inches : tuple
        Figure size as (width, height) in inches
    rows : int
        Number of rows in the subplot grid
    cols : int
        Number of columns in the subplot grid
    
    Attributes:
    -----------
    row_heights : list of float
        Height in inches for each row. Default: [2.0] * rows
    col_widths : list of float
        Width in inches for each column. Default: [2.0] * cols
    wspace : list of float
        Vertical spacing in inches between rows (length = rows-1).
        wspace[i] is the space between row i and row i+1. Default: [0.5] * (rows-1)
    hspace : list of float
        Horizontal spacing in inches between columns (length = cols-1).
        hspace[i] is the space between column i and column i+1. Default: [0.5] * (cols-1)
    margins : dict
        Margins in inches: {'left': float, 'right': float, 'top': float, 'bottom': float}
        Default: {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75}
    
    Examples:
    ---------
    # Create a 2x3 layout with custom row heights
    layout = SubplotLayoutConfig((10, 8), rows=2, cols=3)
    layout.row_heights = [3.0, 2.0]  # First row taller than second
    layout.col_widths = [2.5, 2.5, 2.5]  # All columns same width
    layout.wspace = [0.8]  # Larger spacing between rows
    
    # Get coordinates
    coords = layout.get_coordinates()
    """
    
    def __init__(self, fig_size_inches, rows, cols):
        self.fig_size_inches = tuple(fig_size_inches)
        self.rows = rows
        self.cols = cols
        
        # Default values - uniform sizes and spacing
        self.row_heights = [2.0] * rows
        self.col_widths = [2.0] * cols
        self.wspace = [0.5] * (rows - 1) if rows > 1 else []
        self.hspace = [0.5] * (cols - 1) if cols > 1 else []
        self.margins = {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75}
    
    def set_uniform_row_height(self, height):
        """Set the same height for all rows."""
        self.row_heights = [height] * self.rows
        return self
    
    def set_uniform_col_width(self, width):
        """Set the same width for all columns."""
        self.col_widths = [width] * self.cols
        return self
    
    def set_uniform_wspace(self, spacing):
        """Set uniform vertical spacing between all rows."""
        self.wspace = [spacing] * (self.rows - 1) if self.rows > 1 else []
        return self
    
    def set_uniform_hspace(self, spacing):
        """Set uniform horizontal spacing between all columns."""
        self.hspace = [spacing] * (self.cols - 1) if self.cols > 1 else []
        return self
    
    def get_coordinates(self):
        """
        Calculate subplot coordinates based on the configuration.
        
        Returns:
        --------
        list
            List of tuples, each containing (left, bottom, width, height) coordinates
            in figure-relative units (0-1) for each subplot, ordered row by row.
        """
        import warnings
        
        fig_width, fig_height = self.fig_size_inches
        
        # Validate list lengths
        if len(self.row_heights) != self.rows:
            raise ValueError(f"row_heights must have {self.rows} elements, got {len(self.row_heights)}")
        if len(self.col_widths) != self.cols:
            raise ValueError(f"col_widths must have {self.cols} elements, got {len(self.col_widths)}")
        if self.rows > 1 and len(self.wspace) != self.rows - 1:
            raise ValueError(f"wspace must have {self.rows - 1} elements, got {len(self.wspace)}")
        if self.cols > 1 and len(self.hspace) != self.cols - 1:
            raise ValueError(f"hspace must have {self.cols - 1} elements, got {len(self.hspace)}")
        
        # Calculate total space needed
        total_subplot_width = sum(self.col_widths)
        total_subplot_height = sum(self.row_heights)
        total_hspace = sum(self.hspace)
        total_wspace = sum(self.wspace)
        total_margins_width = self.margins["left"] + self.margins["right"]
        total_margins_height = self.margins["top"] + self.margins["bottom"]
        
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
        
        # Calculate cumulative positions for columns (from left to right)
        col_lefts = []
        current_left = self.margins["left"]
        for col in range(self.cols):
            col_lefts.append(current_left)
            current_left += self.col_widths[col]
            if col < self.cols - 1:  # Add spacing if not the last column
                current_left += self.hspace[col]
        
        # Generate coordinates for each subplot
        for row in range(self.rows):
            for col in range(self.cols):
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
    
    def to_dict(self):
        """Convert configuration to a dictionary."""
        return {
            'fig_size': self.fig_size_inches,
            'rows': self.rows,
            'cols': self.cols,
            'row_heights': self.row_heights,
            'col_widths': self.col_widths,
            'wspace': self.wspace,
            'hspace': self.hspace,
            'margins': self.margins
        }
    
    @classmethod
    def from_dict(cls, config):
        """Create a SubplotLayoutConfig from a dictionary."""
        layout = cls(
            config['fig_size'],
            config['rows'],
            config['cols']
        )
        layout.row_heights = config.get('row_heights', layout.row_heights)
        layout.col_widths = config.get('col_widths', layout.col_widths)
        layout.wspace = config.get('wspace', layout.wspace)
        layout.hspace = config.get('hspace', layout.hspace)
        layout.margins = config.get('margins', layout.margins)
        return layout


def calculate_subplot_coordinates(
    fig_size_inches, subplot_layout, subplot_size_inches, spacing
):
    """
    Calculate subplot coordinates for matplotlib subplots with exact subplot sizes.
    
    Supports both uniform sizing (backward compatible) and per-row customization.

    Parameters:
    -----------
    fig_size_inches : tuple
        Figure size as (width, height) in inches
    subplot_layout : tuple
        Number of subplots as (rows, columns)
    subplot_size_inches : tuple or dict
        Subplot sizes. Can be:
        - tuple: (width, height) - uniform size for all subplots
        - dict: {'row_heights': list, 'col_widths': list} - per-row/col sizes
          * row_heights: list of height in inches for each row
          * col_widths: list of width in inches for each column
    spacing : dict
        Spacing parameters. Can be:
        - Simple (uniform): {'hspace': float, 'wspace': float, 'margins': dict}
          * hspace: horizontal spacing between subplots in inches
          * wspace: vertical spacing between subplots in inches
          * margins: {'left': float, 'right': float, 'top': float, 'bottom': float}
        - Per-row: {'hspace': list, 'wspace': list, 'margins': dict}
          * hspace: list of horizontal spacing in inches (length = cols-1)
          * wspace: list of vertical spacing in inches (length = rows-1)
          * margins: same as above

    Returns:
    --------
    list
        List of tuples, each containing (left, bottom, width, height) coordinates
        in figure-relative units (0-1) for each subplot

    Examples:
    ---------
    # Uniform sizing (backward compatible)
    coords = calculate_subplot_coordinates(
        fig_size_inches=(10, 6),
        subplot_layout=(2, 3),
        subplot_size_inches=(2.5, 2.0),
        spacing={'hspace': 0.5, 'wspace': 0.5, 
                 'margins': {'left': 0.75, 'right': 0.75, 'top': 0.75, 'bottom': 0.75}}
    )
    
    # Per-row customization
    coords = calculate_subplot_coordinates(
        fig_size_inches=(10, 8),
        subplot_layout=(3, 2),
        subplot_size_inches={'row_heights': [3.0, 2.0, 1.5], 'col_widths': [3.0, 3.0]},
        spacing={'hspace': [0.5], 'wspace': [0.5, 0.8],
                 'margins': {'left': 0.5, 'right': 0.5, 'top': 0.5, 'bottom': 0.5}}
    )

    Raises:
    -------
    Warning if subplots won't fit in the specified figure size
    """
    rows, cols = subplot_layout
    
    # Create layout config
    layout = SubplotLayoutConfig(fig_size_inches, rows, cols)
    
    # Handle subplot_size_inches - can be tuple or dict
    if isinstance(subplot_size_inches, dict):
        # Per-row/col specification
        if 'row_heights' in subplot_size_inches:
            layout.row_heights = subplot_size_inches['row_heights']
        if 'col_widths' in subplot_size_inches:
            layout.col_widths = subplot_size_inches['col_widths']
    else:
        # Uniform specification (backward compatible)
        subplot_width, subplot_height = subplot_size_inches
        layout.set_uniform_row_height(subplot_height)
        layout.set_uniform_col_width(subplot_width)
    
    # Handle spacing - can be uniform or per-row/col
    if 'hspace' in spacing:
        if isinstance(spacing['hspace'], list):
            layout.hspace = spacing['hspace']
        else:
            layout.set_uniform_hspace(spacing['hspace'])
    
    if 'wspace' in spacing:
        if isinstance(spacing['wspace'], list):
            layout.wspace = spacing['wspace']
        else:
            layout.set_uniform_wspace(spacing['wspace'])
    
    if 'margins' in spacing:
        layout.margins = spacing['margins']
    
    return layout.get_coordinates()
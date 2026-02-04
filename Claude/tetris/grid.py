"""
Grid class managing the Tetris playing field.
"""

from constants import GRID_WIDTH, GRID_HEIGHT


class Grid:
    """Manages the 10x20 Tetris grid, piece placement, and row clearing."""
    
    def __init__(self):
        """Initialize an empty grid."""
        self.width = GRID_WIDTH
        self.height = GRID_HEIGHT
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def is_valid_position(self, blocks):
        """
        Check if the given block positions are valid.
        
        Args:
            blocks: List of (x, y) tuples representing block positions
            
        Returns:
            True if all positions are valid, False otherwise
        """
        for x, y in blocks:
            # Check boundaries
            if x < 0 or x >= self.width or y >= self.height:
                return False
            
            # Check collision with existing blocks (ignore y < 0 for spawning)
            if y >= 0 and self.grid[y][x] is not None:
                return False
        
        return True
    
    def place_piece(self, blocks, color):
        """
        Place a piece on the grid.
        
        Args:
            blocks: List of (x, y) tuples representing block positions
            color: RGB color tuple for the piece
        """
        for x, y in blocks:
            if 0 <= y < self.height:
                self.grid[y][x] = color
    
    def clear_full_rows(self):
        """
        Clear all full rows and return the number cleared.
        
        Returns:
            Number of rows cleared
        """
        rows_cleared = 0
        y = self.height - 1
        
        while y >= 0:
            if all(self.grid[y][x] is not None for x in range(self.width)):
                # Remove the full row
                del self.grid[y]
                # Add empty row at top
                self.grid.insert(0, [None for _ in range(self.width)])
                rows_cleared += 1
                # Don't decrement y, check this row again
            else:
                y -= 1
        
        return rows_cleared
    
    def is_game_over(self, blocks):
        """
        Check if the game is over (new piece collides immediately).
        
        Args:
            blocks: List of (x, y) tuples for the newly spawned piece
            
        Returns:
            True if game over, False otherwise
        """
        for x, y in blocks:
            if y >= 0 and self.grid[y][x] is not None:
                return True
        return False
    
    def get_cell(self, x, y):
        """
        Get the color at a specific grid position.
        
        Args:
            x: Column index
            y: Row index
            
        Returns:
            Color tuple or None if empty
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def reset(self):
        """Clear the entire grid."""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]

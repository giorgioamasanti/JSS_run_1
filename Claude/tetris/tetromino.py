"""
Tetromino class managing individual pieces and their behavior.
"""

import random
from constants import SHAPES, COLORS


class Tetromino:
    """Represents a Tetris piece with position, shape, and rotation."""
    
    def __init__(self, shape_type=None):
        """
        Initialize a tetromino.
        
        Args:
            shape_type: Type of piece ('I', 'O', 'T', 'S', 'Z', 'J', 'L')
                       If None, randomly selected
        """
        if shape_type is None:
            shape_type = random.choice(list(SHAPES.keys()))
        
        self.shape_type = shape_type
        self.color = COLORS[shape_type]
        self.rotation_index = 0
        self.x = 3  # Starting x position (centered)
        self.y = 0  # Starting y position (top)
        
    def get_blocks(self):
        """
        Get current block positions relative to tetromino position.
        
        Returns:
            List of (x, y) tuples representing block positions
        """
        shape = SHAPES[self.shape_type][self.rotation_index]
        return [(self.x + dx, self.y + dy) for dx, dy in shape]
    
    def rotate(self):
        """Rotate the piece clockwise."""
        rotations = SHAPES[self.shape_type]
        self.rotation_index = (self.rotation_index + 1) % len(rotations)
    
    def rotate_back(self):
        """Rotate the piece counter-clockwise (undo rotation)."""
        rotations = SHAPES[self.shape_type]
        self.rotation_index = (self.rotation_index - 1) % len(rotations)
    
    def move(self, dx, dy):
        """
        Move the piece by the given offset.
        
        Args:
            dx: Change in x position
            dy: Change in y position
        """
        self.x += dx
        self.y += dy
    
    def copy(self):
        """Create a copy of this tetromino."""
        new_piece = Tetromino(self.shape_type)
        new_piece.rotation_index = self.rotation_index
        new_piece.x = self.x
        new_piece.y = self.y
        return new_piece

from settings import *

class Tetromino:
    def __init__(self, shape_key):
        self.shape_key = shape_key
        self.rotations = SHAPES[shape_key]
        self.color = SHAPE_COLORS[shape_key]
        self.rotation_index = 0
        self.blocks = self.rotations[self.rotation_index]
        
        # Spawn position (Center top)
        self.x = GRID_WIDTH // 2
        self.y = 1  # Start slightly down to avoid immediate ceiling clipping

    def rotate(self):
        """Advances to the next rotation state."""
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)
        self.blocks = self.rotations[self.rotation_index]

    def undo_rotate(self):
        """Reverts rotation (used if a rotation results in collision)."""
        self.rotation_index = (self.rotation_index - 1) % len(self.rotations)
        self.blocks = self.rotations[self.rotation_index]

    def get_positions(self):
        """Returns the absolute grid coordinates of the piece's blocks."""
        positions = []
        for block in self.blocks:
            positions.append((self.x + block[0], self.y + block[1]))
        return positions

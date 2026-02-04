import random
import os
from settings import *
from tetromino import Tetromino

class Game:
    def __init__(self):
        self.grid = [[(0, 0, 0) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.score = 0
        self.high_score = self.load_high_score()
        self.state = "START" # START, PLAYING, PAUSED, GAME_OVER
        
        # Randomizer History for "No 3x" rule
        self.recent_shapes = [None, None]
        
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()

    def get_new_piece(self):
        """Generates a piece ensuring the same shape doesn't appear 3 times in a row."""
        keys = list(SHAPES.keys())
        
        while True:
            choice = random.choice(keys)
            # Check if this choice matches the last two
            if choice == self.recent_shapes[0] and choice == self.recent_shapes[1]:
                continue # Re-roll
            
            # Update history
            self.recent_shapes.pop(0)
            self.recent_shapes.append(choice)
            return Tetromino(choice)

    def check_collision(self, piece=None):
        """Checks if the current piece (or specific piece) is in an invalid position."""
        if piece is None:
            piece = self.current_piece
            
        for x, y in piece.get_positions():
            # Check boundaries
            if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
                return True
            # Check hitting other pieces (ignore if y < 0, meaning above screen)
            if y >= 0 and self.grid[y][x] != (0,0,0):
                return True
        return False

    def lock_piece(self):
        """Locks current piece into the grid."""
        for x, y in self.current_piece.get_positions():
            if y >= 0:
                self.grid[y][x] = self.current_piece.color
        
        self.clear_rows()
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()
        
        # Check immediate loss
        if self.check_collision():
            self.state = "GAME_OVER"
            self.update_high_score()

    def clear_rows(self):
        """Checks for full rows, removes them, and moves blocks down."""
        lines_cleared = 0
        # Create a new grid excluding full rows
        new_grid = [row for row in self.grid if (0,0,0) in row]
        lines_cleared = GRID_HEIGHT - len(new_grid)
        
        # Add fresh empty rows at the top
        for _ in range(lines_cleared):
            new_grid.insert(0, [(0, 0, 0) for _ in range(GRID_WIDTH)])
            
        self.grid = new_grid
        
        # Scoring: 100, 300, 500, 800
        scores = [0, 100, 300, 500, 800]
        self.score += scores[lines_cleared]

    def move(self, dx, dy):
        """Moves the piece if valid."""
        self.current_piece.x += dx
        self.current_piece.y += dy
        if self.check_collision():
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            return False # Move failed
        return True # Move successful

    def rotate(self):
        old_index = self.current_piece.rotation_index
        self.current_piece.rotate()
        if self.check_collision():
            self.current_piece.undo_rotate()

    def load_high_score(self):
        if not os.path.exists("highscore.txt"):
            return 0
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))

    def reset(self):
        self.__init__()
        self.state = "PLAYING"

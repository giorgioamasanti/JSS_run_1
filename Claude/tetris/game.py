"""
Game class managing Tetris game logic and state.
"""

import random
from tetromino import Tetromino
from grid import Grid
from constants import SCORE_PER_ROW, INITIAL_FALL_SPEED


class Game:
    """Manages game state, logic, and piece generation."""
    
    def __init__(self):
        """Initialize the game."""
        self.grid = Grid()
        self.current_piece = None
        self.score = 0
        self.high_score = 0
        self.game_state = "ready"  # ready, playing, paused, game_over
        self.fall_speed = INITIAL_FALL_SPEED
        self.last_two_pieces = []  # Track last 2 pieces to prevent 3 consecutive
        
    def start_game(self):
        """Start a new game."""
        self.grid.reset()
        self.score = 0
        self.game_state = "playing"
        self.fall_speed = INITIAL_FALL_SPEED
        self.last_two_pieces = []
        self.spawn_new_piece()
    
    def pause_game(self):
        """Pause the game."""
        if self.game_state == "playing":
            self.game_state = "paused"
    
    def resume_game(self):
        """Resume the game."""
        if self.game_state == "paused":
            self.game_state = "playing"
    
    def reset_game(self):
        """Reset to ready state."""
        self.grid.reset()
        self.current_piece = None
        self.score = 0
        self.game_state = "ready"
        self.fall_speed = INITIAL_FALL_SPEED
        self.last_two_pieces = []
    
    def spawn_new_piece(self):
        """
        Spawn a new tetromino piece.
        Ensures the same piece doesn't appear 3 times consecutively.
        """
        # Get available shapes
        available_shapes = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
        
        # If last two pieces were the same, exclude that shape
        if len(self.last_two_pieces) >= 2 and \
           self.last_two_pieces[-1] == self.last_two_pieces[-2]:
            available_shapes = [s for s in available_shapes 
                              if s != self.last_two_pieces[-1]]
        
        # Select random shape
        shape_type = random.choice(available_shapes)
        self.current_piece = Tetromino(shape_type)
        
        # Track piece history
        self.last_two_pieces.append(shape_type)
        if len(self.last_two_pieces) > 2:
            self.last_two_pieces.pop(0)
        
        # Check for game over
        if self.grid.is_game_over(self.current_piece.get_blocks()):
            self.game_state = "game_over"
            if self.score > self.high_score:
                self.high_score = self.score
    
    def move_piece(self, dx, dy):
        """
        Attempt to move the current piece.
        
        Args:
            dx: Change in x position
            dy: Change in y position
            
        Returns:
            True if move was successful, False otherwise
        """
        if self.current_piece is None or self.game_state != "playing":
            return False
        
        self.current_piece.move(dx, dy)
        
        if not self.grid.is_valid_position(self.current_piece.get_blocks()):
            self.current_piece.move(-dx, -dy)
            return False
        
        return True
    
    def rotate_piece(self):
        """
        Attempt to rotate the current piece.
        
        Returns:
            True if rotation was successful, False otherwise
        """
        if self.current_piece is None or self.game_state != "playing":
            return False
        
        self.current_piece.rotate()
        
        if not self.grid.is_valid_position(self.current_piece.get_blocks()):
            self.current_piece.rotate_back()
            return False
        
        return True
    
    def drop_piece(self):
        """
        Drop the piece one row down.
        
        Returns:
            True if piece moved, False if it locked in place
        """
        if not self.move_piece(0, 1):
            # Piece can't move down, lock it in place
            self.lock_piece()
            return False
        return True
    
    def hard_drop(self):
        """Drop the piece all the way down instantly."""
        if self.current_piece is None or self.game_state != "playing":
            return
        
        while self.move_piece(0, 1):
            pass
        
        self.lock_piece()
    
    def lock_piece(self):
        """Lock the current piece into the grid and spawn a new one."""
        if self.current_piece is None:
            return
        
        self.grid.place_piece(self.current_piece.get_blocks(), 
                             self.current_piece.color)
        
        # Clear full rows and update score
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.score += SCORE_PER_ROW * rows_cleared
        
        # Spawn new piece
        self.spawn_new_piece()
    
    def get_game_state(self):
        """Get current game state information."""
        return {
            'state': self.game_state,
            'score': self.score,
            'high_score': self.high_score,
        }

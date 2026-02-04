"""
Renderer class handling all pygame display and UI elements.
"""

import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT,
    BLACK, WHITE, GRAY, LIGHT_GRAY, DARK_GRAY
)


class Renderer:
    """Handles all rendering operations for the Tetris game."""
    
    def __init__(self):
        """Initialize pygame and create the display window."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        
        # Control panel dimensions
        self.panel_x = GRID_WIDTH * CELL_SIZE + 20
        self.panel_y = 20
    
    def draw_grid(self, grid, current_piece):
        """
        Draw the Tetris grid and current piece.
        
        Args:
            grid: Grid object containing the playing field
            current_piece: Current falling Tetromino or None
        """
        # Draw grid background
        grid_surface = pygame.Surface((GRID_WIDTH * CELL_SIZE, 
                                      GRID_HEIGHT * CELL_SIZE))
        grid_surface.fill(BLACK)
        
        # Draw locked blocks
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = grid.get_cell(x, y)
                if color is not None:
                    self._draw_block(grid_surface, x, y, color)
        
        # Draw current piece
        if current_piece is not None:
            for x, y in current_piece.get_blocks():
                if y >= 0:  # Only draw visible blocks
                    self._draw_block(grid_surface, x, y, current_piece.color)
        
        # Draw grid lines
        for x in range(GRID_WIDTH + 1):
            pygame.draw.line(grid_surface, DARK_GRAY,
                           (x * CELL_SIZE, 0),
                           (x * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
        for y in range(GRID_HEIGHT + 1):
            pygame.draw.line(grid_surface, DARK_GRAY,
                           (0, y * CELL_SIZE),
                           (GRID_WIDTH * CELL_SIZE, y * CELL_SIZE))
        
        # Draw border
        pygame.draw.rect(grid_surface, WHITE,
                        (0, 0, GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE), 2)
        
        self.screen.blit(grid_surface, (10, 50))
    
    def _draw_block(self, surface, x, y, color):
        """
        Draw a single tetromino block.
        
        Args:
            surface: Surface to draw on
            x, y: Grid coordinates
            color: RGB color tuple
        """
        rect = pygame.Rect(x * CELL_SIZE + 1, y * CELL_SIZE + 1,
                          CELL_SIZE - 2, CELL_SIZE - 2)
        pygame.draw.rect(surface, color, rect)
        
        # Add highlight for 3D effect
        highlight = tuple(min(c + 40, 255) for c in color)
        pygame.draw.line(surface, highlight,
                        (rect.left, rect.top),
                        (rect.right, rect.top), 2)
        pygame.draw.line(surface, highlight,
                        (rect.left, rect.top),
                        (rect.left, rect.bottom), 2)
    
    def draw_control_panel(self, game_state):
        """
        Draw the control panel with score, state, and buttons.
        
        Args:
            game_state: Dictionary with game state information
        """
        # Title
        title = self.title_font.render("TETRIS", True, WHITE)
        self.screen.blit(title, (self.panel_x, self.panel_y))
        
        # Score
        y_offset = self.panel_y + 60
        score_text = self.font.render(f"Score: {game_state['score']}", True, WHITE)
        self.screen.blit(score_text, (self.panel_x, y_offset))
        
        y_offset += 40
        high_score_text = self.font.render(f"High: {game_state['high_score']}", 
                                          True, WHITE)
        self.screen.blit(high_score_text, (self.panel_x, y_offset))
        
        # Game state
        y_offset += 60
        state_text = self.font.render(f"State: {game_state['state'].upper()}", 
                                     True, WHITE)
        self.screen.blit(state_text, (self.panel_x, y_offset))
        
        # Controls
        y_offset += 80
        controls_title = self.font.render("Controls:", True, WHITE)
        self.screen.blit(controls_title, (self.panel_x, y_offset))
        
        y_offset += 35
        controls = [
            "← → : Move",
            "↑ : Rotate",
            "↓ : Soft Drop",
            "SPACE : Hard Drop",
            "",
            "S : Start",
            "P : Pause",
            "R : Reset"
        ]
        
        for line in controls:
            text = self.small_font.render(line, True, LIGHT_GRAY)
            self.screen.blit(text, (self.panel_x, y_offset))
            y_offset += 28
    
    def draw_game_over(self):
        """Draw game over overlay."""
        overlay = pygame.Surface((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (10, 50))
        
        # Game over text
        game_over_text = self.title_font.render("GAME OVER", True, WHITE)
        text_rect = game_over_text.get_rect(
            center=(10 + GRID_WIDTH * CELL_SIZE // 2, 
                   50 + GRID_HEIGHT * CELL_SIZE // 2 - 30))
        self.screen.blit(game_over_text, text_rect)
        
        restart_text = self.font.render("Press R to restart", True, LIGHT_GRAY)
        restart_rect = restart_text.get_rect(
            center=(10 + GRID_WIDTH * CELL_SIZE // 2,
                   50 + GRID_HEIGHT * CELL_SIZE // 2 + 20))
        self.screen.blit(restart_text, restart_rect)
    
    def render(self, game):
        """
        Main render function.
        
        Args:
            game: Game object to render
        """
        self.screen.fill(BLACK)
        
        # Draw grid and current piece
        self.draw_grid(game.grid, game.current_piece)
        
        # Draw control panel
        self.draw_control_panel(game.get_game_state())
        
        # Draw game over overlay if needed
        if game.game_state == "game_over":
            self.draw_game_over()
        
        pygame.display.flip()
    
    def tick(self, fps):
        """
        Control frame rate.
        
        Args:
            fps: Frames per second
        """
        self.clock.tick(fps)
    
    def quit(self):
        """Clean up pygame."""
        pygame.quit()

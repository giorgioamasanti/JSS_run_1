import os

# Define the file contents
settings_code = r'''import pygame

# --- Dimensions ---
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
PANEL_WIDTH = 200
SCREEN_WIDTH = (GRID_WIDTH * BLOCK_SIZE) + PANEL_WIDTH
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE

# --- Colors (R, G, B) ---
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (220, 20, 60)
GREEN = (50, 205, 50)
BLUE = (65, 105, 225)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 215, 0)
ORANGE = (255, 165, 0)
DARK_GRAY = (40, 40, 40)

# --- Game Stats ---
FPS = 60
START_SPEED = 500  # Milliseconds per fall step

# --- Shape Definitions ---
SHAPES = {
    'T': [
        [(0,0), (-1,0), (1,0), (0,-1)],
        [(0,0), (0,-1), (0,1), (1,0)],
        [(0,0), (-1,0), (1,0), (0,1)],
        [(0,0), (0,-1), (0,1), (-1,0)]
    ],
    'S': [
        [(0,0), (-1,0), (0,-1), (1,-1)],
        [(0,0), (0,-1), (1,0), (1,1)]
    ],
    'Z': [
        [(0,0), (1,0), (0,-1), (-1,-1)],
        [(0,0), (0,1), (1,0), (1,-1)]
    ],
    'J': [
        [(0,0), (-1,0), (1,0), (-1,-1)],
        [(0,0), (0,-1), (0,1), (1,-1)],
        [(0,0), (-1,0), (1,0), (1,1)],
        [(0,0), (0,-1), (0,1), (-1,1)]
    ],
    'L': [
        [(0,0), (-1,0), (1,0), (1,-1)],
        [(0,0), (0,-1), (0,1), (1,1)],
        [(0,0), (-1,0), (1,0), (-1,1)],
        [(0,0), (0,-1), (0,1), (-1,-1)]
    ],
    'I': [
        [(0,0), (-1,0), (1,0), (2,0)],
        [(0,0), (0,-1), (0,1), (0,2)]
    ],
    'O': [
        [(0,0), (1,0), (0,1), (1,1)]
    ]
}

SHAPE_COLORS = {
    'T': MAGENTA, 'S': GREEN, 'Z': RED, 
    'J': BLUE, 'L': ORANGE, 'I': CYAN, 'O': YELLOW
}
'''

tetromino_code = r'''from settings import *

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
'''

game_logic_code = r'''import random
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
'''

main_code = r'''import pygame
import sys
from settings import *
from game_logic import Game

# --- Rendering Helpers ---
def draw_grid(surface, grid):
    # Draw background grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, GRAY, rect, 1) # Grid lines
            
            # Draw locked blocks
            if grid[y][x] != (0,0,0):
                pygame.draw.rect(surface, grid[y][x], rect)

def draw_piece(surface, piece):
    for x, y in piece.get_positions():
        rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(surface, piece.color, rect)
        pygame.draw.rect(surface, GRAY, rect, 1) # Outline

def draw_panel(surface, font, game):
    panel_x = GRID_WIDTH * BLOCK_SIZE + 20
    
    # Texts
    texts = [
        f"Score: {game.score}",
        f"High: {game.high_score}",
        "",
        "Next:",
    ]
    
    # Render Stat Text
    for i, line in enumerate(texts):
        text_surf = font.render(line, True, WHITE)
        surface.blit(text_surf, (panel_x, 20 + i * 40))

    # Draw Next Piece Preview
    # Create a mini offset to draw the next piece in the panel area
    preview_x_offset = panel_x + 30
    preview_y_offset = 180
    
    for block in game.next_piece.blocks:
        bx = preview_x_offset + (block[0] * BLOCK_SIZE)
        by = preview_y_offset + (block[1] * BLOCK_SIZE)
        rect = pygame.Rect(bx, by, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(surface, game.next_piece.color, rect)
        pygame.draw.rect(surface, GRAY, rect, 1)

    # Controls Instructions
    controls = [
        "CONTROLS:",
        "Arrows: Move/Rot",
        "Space: Hard Drop",
        "P: Pause",
        "R: Reset",
        "Enter: Start"
    ]
    
    y_start = 350
    for i, line in enumerate(controls):
        size = 20 if i > 0 else 25
        c_font = pygame.font.SysFont('arial', size)
        text_surf = c_font.render(line, True, WHITE if i == 0 else (200,200,200))
        surface.blit(text_surf, (panel_x, y_start + i * 30))

    # Game State Overlay
    if game.state != "PLAYING":
        center_msg = "PRESS ENTER" if game.state == "START" else game.state
        msg_surf = font.render(center_msg, True, WHITE)
        # Draw a semi-transparent box behind text
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0,0,0,128))
        surface.blit(s, (0,0))
        surface.blit(msg_surf, (SCREEN_WIDTH//2 - msg_surf.get_width()//2, SCREEN_HEIGHT//2))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Python Tetris")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 30)
    
    game = Game()
    fall_time = 0
    fall_speed = START_SPEED

    while True:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if game.state == "PLAYING":
                    if event.key == pygame.K_LEFT:
                        game.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        game.move(0, 1) # Soft drop
                    elif event.key == pygame.K_UP:
                        game.rotate()
                    elif event.key == pygame.K_SPACE:
                        # Hard Drop
                        while game.move(0, 1): pass
                        game.lock_piece()
                    elif event.key == pygame.K_p:
                        game.state = "PAUSED"
                    elif event.key == pygame.K_r:
                        game.reset()
                
                elif game.state in ["START", "GAME_OVER", "PAUSED"]:
                    if event.key == pygame.K_RETURN:
                        if game.state == "GAME_OVER":
                            game.reset()
                        game.state = "PLAYING"
                    elif event.key == pygame.K_r:
                         game.reset()

        # 2. Game Loop / Logic
        if game.state == "PLAYING":
            fall_time += clock.get_rawtime()
            # Increase difficulty check could go here (reduce fall_speed based on score)
            
            if fall_time >= fall_speed:
                if not game.move(0, 1): # Try moving down
                    game.lock_piece()   # If failed, lock it
                fall_time = 0

        # 3. Rendering
        screen.fill(BLACK)
        
        # Draw Play Area Background
        pygame.draw.rect(screen, DARK_GRAY, (0, 0, GRID_WIDTH*BLOCK_SIZE, GRID_HEIGHT*BLOCK_SIZE))
        
        draw_grid(screen, game.grid)
        
        if game.state != "START":
            draw_piece(screen, game.current_piece)
            
        draw_panel(screen, font, game)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
'''

# --- File Generation Logic ---
def create_project():
    folder_name = "TetrisProject"
    
    # Create the directory
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created directory: {folder_name}")
    else:
        print(f"Directory {folder_name} already exists. Updating files...")

    # Map filenames to content
    files = {
        "settings.py": settings_code,
        "tetromino.py": tetromino_code,
        "game_logic.py": game_logic_code,
        "main.py": main_code
    }

    # Write files
    for filename, content in files.items():
        path = os.path.join(folder_name, filename)
        with open(path, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"Created file: {filename}")

    print("\nSuccess! The game is ready.")
    print(f"Navigate to the '{folder_name}' folder and run 'main.py'.")

if __name__ == "__main__":
    create_project()
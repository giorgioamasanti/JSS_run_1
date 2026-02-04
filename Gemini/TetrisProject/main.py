import pygame
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

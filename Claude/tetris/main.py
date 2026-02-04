"""
Main entry point for Tetris game.
"""

import pygame
from game import Game
from renderer import Renderer
from constants import FAST_FALL_SPEED


def main():
    """Main game loop."""
    game = Game()
    renderer = Renderer()
    
    # Game loop timing
    fall_timer = 0
    fast_drop = False
    
    running = True
    while running:
        dt = renderer.clock.get_time()  # Delta time in milliseconds
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                # Game controls
                if event.key == pygame.K_s:
                    if game.game_state == "ready":
                        game.start_game()
                    elif game.game_state == "game_over":
                        game.start_game()
                
                elif event.key == pygame.K_p:
                    if game.game_state == "playing":
                        game.pause_game()
                    elif game.game_state == "paused":
                        game.resume_game()
                
                elif event.key == pygame.K_r:
                    game.reset_game()
                
                # Piece controls (only when playing)
                if game.game_state == "playing":
                    if event.key == pygame.K_LEFT:
                        game.move_piece(-1, 0)
                    
                    elif event.key == pygame.K_RIGHT:
                        game.move_piece(1, 0)
                    
                    elif event.key == pygame.K_UP:
                        game.rotate_piece()
                    
                    elif event.key == pygame.K_DOWN:
                        fast_drop = True
                    
                    elif event.key == pygame.K_SPACE:
                        game.hard_drop()
                        fall_timer = 0  # Reset fall timer
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    fast_drop = False
        
        # Auto-drop logic
        if game.game_state == "playing":
            fall_timer += dt
            
            # Determine fall speed
            current_speed = FAST_FALL_SPEED if fast_drop else game.fall_speed
            
            if fall_timer >= current_speed:
                game.drop_piece()
                fall_timer = 0
        
        # Render
        renderer.render(game)
        renderer.tick(60)  # 60 FPS
    
    renderer.quit()


if __name__ == "__main__":
    main()

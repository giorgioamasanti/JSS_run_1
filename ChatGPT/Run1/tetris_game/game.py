
import pygame, random
from config import *
from grid import Grid
from tetromino import Tetromino, SHAPES

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = Grid()
        self.score = 0
        self.game_over = False
        self.last_fall = pygame.time.get_ticks()
        self.current_piece = self.new_piece()
        self.font = pygame.font.SysFont(None, 30)

    def new_piece(self):
        return Tetromino(random.choice(list(SHAPES.keys())))

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.grid.valid_position(self.current_piece, dx=-1):
                    self.current_piece.x -= 1
                elif event.key == pygame.K_RIGHT and self.grid.valid_position(self.current_piece, dx=1):
                    self.current_piece.x += 1
                elif event.key == pygame.K_DOWN and self.grid.valid_position(self.current_piece, dy=1):
                    self.current_piece.y += 1
                elif event.key == pygame.K_UP:
                    old_shape = self.current_piece.shape
                    self.current_piece.rotate()
                    if not self.grid.valid_position(self.current_piece):
                        self.current_piece.shape = old_shape

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_fall > FALL_DELAY:
            if self.grid.valid_position(self.current_piece, dy=1):
                self.current_piece.y += 1
            else:
                self.grid.lock_piece(self.current_piece)
                cleared = self.grid.clear_lines()
                self.score += cleared * 100
                self.current_piece = self.new_piece()
                if not self.grid.valid_position(self.current_piece):
                    self.game_over = True
            self.last_fall = now

    def draw_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        COLORS[self.current_piece.color],
                        ((self.current_piece.x + x)*TILE_SIZE,
                         (self.current_piece.y + y)*TILE_SIZE,
                         TILE_SIZE, TILE_SIZE)
                    )

    def draw_ui(self):
        score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))
        self.screen.blit(score_text, (350, 50))

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_input()
            if not self.game_over:
                self.update()
            self.screen.fill((0,0,0))
            self.grid.draw(self.screen)
            self.draw_piece()
            self.draw_ui()
            pygame.display.flip()

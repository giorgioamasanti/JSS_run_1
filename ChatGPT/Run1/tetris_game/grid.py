
import pygame
from config import GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, COLORS

class Grid:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    def draw(self, surface):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(
                    surface,
                    COLORS[self.grid[y][x]],
                    (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                )
                pygame.draw.rect(
                    surface,
                    (50,50,50),
                    (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    1
                )

    def valid_position(self, tetromino, dx=0, dy=0):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx = tetromino.x + x + dx
                    ny = tetromino.y + y + dy
                    if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT:
                        return False
                    if ny >= 0 and self.grid[ny][nx]:
                        return False
        return True

    def lock_piece(self, tetromino):
        for y, row in enumerate(tetromino.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[tetromino.y + y][tetromino.x + x] = tetromino.color

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        cleared = GRID_HEIGHT - len(new_grid)
        for _ in range(cleared):
            new_grid.insert(0, [0]*GRID_WIDTH)
        self.grid = new_grid
        return cleared

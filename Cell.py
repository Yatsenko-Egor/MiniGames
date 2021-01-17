import pygame
from AssetManager import assetManager


class CellSprite(pygame.sprite.Sprite):
    def __init__(self, condition, x, y, *groups):
        super().__init__(groups)
        self.condition = condition
        self.update()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mines_around = 0

    def update(self):
        if self.condition == -1 or self.condition == -2:
            self.image = assetManager.load_image('Minesweeper/default_cell.png')
        elif self.condition == 12 or self.condition == 13:
            self.image = assetManager.load_image('Minesweeper/flag.png')
        elif self.condition == 14:
            self.image = assetManager.load_image('Minesweeper/bomb_cell.png', (255, 255, 255))
        elif self.condition == 15:
            self.image = assetManager.load_image('Minesweeper/boom.png')
        elif self.condition == 1:
            self.image = pygame.Surface((29, 29))
            self.image.fill(pygame.Color((180, 180, 180)))
            if self.mines_around:
                self.draw_number(self.mines_around)
        elif self.condition == 16:
            self.image = assetManager.load_image('Minesweeper/not_flag.png')

    def draw_number(self, mines_count):
        number = {1: (0, 0, 255), 2: (0, 255, 0), 3: (255, 0, 0), 4: (0, 33, 55),
                  5: (104, 28, 35), 6: (0, 255, 255), 7: (1, 21, 62), 8: (60, 60, 60)}
        font = pygame.font.Font(None, 50)
        text = font.render(str(mines_count), True, number[mines_count])
        text_x = self.rect.width // 2 - text.get_width() // 2
        text_y = self.rect.height // 2 - text.get_height() // 2
        self.image.blit(text, (text_x, text_y))


class Cells(pygame.sprite.Group):
    def __init__(self, count_cells, row_number):
        super().__init__()
        self.CELL_SIZE = 30
        self.count_cells = count_cells
        self.row_number = row_number
        self.create_cells()

    def create_cells(self):
        y = self.row_number * self.CELL_SIZE + 40
        for i in range(self.count_cells):
            x = i * self.CELL_SIZE
            cell = CellSprite(-1, x, y)
            cell.row = self.row_number
            cell.column = i
            self.add(cell)
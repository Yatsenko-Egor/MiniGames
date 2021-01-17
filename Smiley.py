import pygame
from AssetManager import assetManager


class SmileySprite(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.state = 2
        self.update()
        self.rect = self.image.get_rect()
        self.rect.x = (width - 120 - 40) // 2 + 60
        self.rect.y = 0

    def update(self):
        if self.state == 2:
            self.image = assetManager.load_image('Minesweeper/default_smiley.png', (255, 255, 255))
        elif self.state == 1:
            self.image = assetManager.load_image('Minesweeper/victory_smiley.png', (255, 255, 255))
        else:
            self.image = assetManager.load_image('Minesweeper/loss_smiley.png', (255, 255, 255))


class Smiley(pygame.sprite.GroupSingle):
    def __init__(self, width):
        super().__init__(SmileySprite(width))
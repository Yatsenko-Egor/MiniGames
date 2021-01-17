import pygame
from AssetManager import assetManager

class GrassSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = assetManager.load_image('grass.png')
        self.rect = self.image.get_rect()


class Field(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        for x in range(0, 576, 25):
            for y in range(0, 576, 25):
                cell = GrassSprite()
                cell.rect.x = x
                cell.rect.y = y
                self.add(cell)
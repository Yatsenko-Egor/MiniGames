import pygame
from AssetManager import assetManager
from random import randrange


class AppleSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = assetManager.load_image('Snake/apple.png', (255, 255, 255))
        self.rect = self.image.get_rect()
        self.change_coordinates()

    def change_coordinates(self):
        self.rect.x = randrange(0, 575, 25)
        self.rect.y = randrange(0, 575, 25)


class Apple(pygame.sprite.GroupSingle):
    def __init__(self):
        super().__init__(AppleSprite())
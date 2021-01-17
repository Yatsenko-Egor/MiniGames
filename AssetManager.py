import os
import sys
import pygame


class AssetManager:
    def __init__(self):
        self.assets = {}

    def load_image(self, name, colorkey=None):
        if (name, colorkey) in self.assets:
            return self.assets[(name, colorkey)]

        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        self.assets[(name, colorkey)] = image
        return self.assets[(name, colorkey)]


assetManager = AssetManager()
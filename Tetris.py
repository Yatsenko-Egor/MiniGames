import pygame
import os
from Board import Board
from random import *

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 750, 750
FPS = 60
SPEED = 25
BOARD_SIZE = (WINDOW_WIDTH // 5, WINDOW_HEIGHT // 5)


class Tetris(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.all_sprites = pygame.sprite.Group()
        self.size = 50
        self.x_pos = WINDOW_WIDTH // 2 - self.size // 2
        self.y_pos = 0
        self.total = 1
        self.flag = True
        self.map = []
        self.b = []
        self.figures = ['s', 'z', 'l', 't', 'j', 'o', 'i']

    def render(self, screen):
        if self.flag == True:
            self.what_figure = self.get_figure()
            self.flag = False
        if self.what_figure == 's':
            self.draw_s(screen)
        elif self.what_figure == 'z':
            self.draw_z(screen)
        elif self.what_figure == 'l':
            self.draw_l(screen)
        elif self.what_figure == 't':
            self.draw_t(screen)
        elif self.what_figure == 'j':
            self.draw_j(screen)
        elif self.what_figure == 'o':
            self.draw_o(screen)
        elif self.what_figure == 'i':
            self.draw_i(screen)

    def new_coords(self):
        self.x_pos = WINDOW_WIDTH // 2 - self.size // 2
        self.y_pos = 0
        self.flag = True

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def get_figure(self):
        self.a = choice(self.figures)
        return self.a

    def get_size(self):
        return self.size

    def get_position(self):
        return self.x_pos, self.y_pos

    def set_position(self, position):
        self.x_pos, self.y_pos = position
        
    def is_free_left(self, x):
        if x >= SPEED:
            return True

    def is_free_right(self, x):
        if x <= WINDOW_WIDTH - self.size - SPEED:
            return True

    def is_free_down(self, y):
        if y <= WINDOW_HEIGHT - self.size - 7:
            return True

    def is_free_down_low(self, y):
        if y <= WINDOW_HEIGHT - self.size - 2:
            return True

    def draw_s(self, screen):
        self.s_types = {
            1: 's_1.xcf',
            2: 's_2.xcf',
            3: 's_3.xcf',
            4: 's_4.xcf'
        }
        filename = self.s_types[self.total]
        s = pygame.sprite.Sprite()
        s.image = self.load_image(filename)
        s.rect = s.image.get_rect()
        self.all_sprites.add(s)
        self.load_image(filename)
        s.rect.x = self.x_pos
        s.rect.y = self.y_pos

    def draw_z(self, screen):
        self.z_types = {
            1: 'z_1.xcf',
            2: 'z_2.xcf',
            3: 'z_3.xcf',
            4: 'z_4.xcf'
        }
        filename = self.z_types[self.total]
        z = pygame.sprite.Sprite()
        z.image = self.load_image(filename)
        z.rect = z.image.get_rect()
        self.all_sprites.add(z)
        self.load_image(filename)
        z.rect.x = self.x_pos
        z.rect.y = self.y_pos

    def draw_j(self, screen):
        self.j_types = {
            1: 'j_1.xcf',
            2: 'j_2.xcf',
            3: 'j_3.xcf',
            4: 'j_4.xcf'
        }
        filename = self.j_types[self.total]
        j = pygame.sprite.Sprite()
        j.image = self.load_image(filename)
        j.rect = j.image.get_rect()
        self.all_sprites.add(j)
        self.load_image(filename)
        j.rect.x = self.x_pos
        j.rect.y = self.y_pos

    def draw_t(self, screen):
        self.t_types = {
            1: 't_1.xcf',
            2: 't_2.xcf',
            3: 't_3.xcf',
            4: 't_4.xcf'
        }
        filename = self.t_types[self.total]
        t = pygame.sprite.Sprite()
        t.image = self.load_image(filename)
        t.rect = t.image.get_rect()
        self.all_sprites.add(t)
        self.load_image(filename)
        t.rect.x = self.x_pos
        t.rect.y = self.y_pos

    def draw_l(self, screen):
        self.l_types = {
            1: 'l_1.xcf',
            2: 'l_2.xcf',
            3: 'l_3.xcf',
            4: 'l_4.xcf'
        }
        filename = self.l_types[self.total]
        l = pygame.sprite.Sprite()
        l.image = self.load_image(filename)
        l.rect = l.image.get_rect()
        self.all_sprites.add(l)
        self.load_image(filename)
        l.rect.x = self.x_pos
        l.rect.y = self.y_pos

    def draw_o(self, screen):
        filename = 'o.xcf'
        self.all_sprites = pygame.sprite.Group()
        o = pygame.sprite.Sprite()
        o.image = self.load_image(filename)
        o.rect = o.image.get_rect()
        self.all_sprites.add(o)
        self.load_image(filename)
        o.rect.x = self.x_pos
        o.rect.y = self.y_pos

    def draw_i(self, screen):
        self.i_types = {
            1: 'i_1.xcf',
            2: 'i_2.xcf',
        }
        filename = self.i_types[self.total]
        i = pygame.sprite.Sprite()
        i.image = self.load_image(filename)
        i.rect = i.image.get_rect()
        self.all_sprites.add(i)
        self.load_image(filename)
        i.rect.x = self.x_pos
        i.rect.y = self.y_pos

    def get_all_sprites(self):
        return self.all_sprites


class Move:
    def __init__(self, tetris):
        self.tetris = tetris

    def render(self, screen):
        self.tetris.render(screen)

    def update_figure(self):
        self.next_x, self.next_y = self.tetris.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if self.tetris.is_free_left(self.next_x):
                    self.next_x -= SPEED
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if self.tetris.is_free_right(self.next_x):
                self.next_x += SPEED
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if self.tetris.is_free_down(self.next_y):
                self.next_y += 10
            else:
                self.next_y += WINDOW_WIDTH - self.tetris.get_size() - self.next_y
        if self.tetris.is_free_down_low(self.next_y):
            self.next_y += 4
        else:
            self.next_y += WINDOW_WIDTH - self.tetris.get_size() - self.next_y
        self.tetris.set_position((self.next_x, self.next_y))
        if self.next_y == WINDOW_WIDTH - self.tetris.get_size():
            self.tetris.new_coords()


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    tetris = Tetris()
    all_sprites = tetris.get_all_sprites()
    board = Board(BOARD_SIZE[0], BOARD_SIZE[1])
    move = Move(tetris)
    running = True
    while running:
        move.update_figure()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(pygame.Color('gray'))
        board.render(screen)
        move.render(screen)
        all_sprites.draw(screen)
        move.update_figure()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
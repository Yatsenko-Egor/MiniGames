import pygame
from random import *

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 750, 750
FPS = 30
SPEED = 25


class Tetris:
    def __init__(self):
        self.size = 50
        self.x_pos = WINDOW_WIDTH // 2
        self.y_pos = 0
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
        self.x_pos = WINDOW_WIDTH // 2
        self.y_pos = 0
        self.flag = True

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
        pygame.draw.polygon(screen, pygame.Color('red'),
                            [(self.x_pos, self.y_pos),
                             (self.x_pos + self.size * 2, self.y_pos),
                             (self.x_pos + self.size * 2, self.size + self.y_pos),
                             (self.x_pos + self.size, self.size + self.y_pos),
                             (self.x_pos + self.size, self.size * 2 + self.y_pos),
                             (self.x_pos - self.size, self.size * 2 + self.y_pos),
                             (self.x_pos - self.size, self.size + self.y_pos),
                             (self.x_pos, self.size + self.y_pos)])

    def draw_z(self, screen):
        pygame.draw.polygon(screen, pygame.Color('orange'),
                            [(self.x_pos - self.size, self.y_pos),
                             (self.x_pos + self.size, self.y_pos),
                             (self.x_pos + self.size, self.size + self.y_pos),
                             (self.x_pos + self.size * 2, self.size + self.y_pos),
                             (self.x_pos + self.size * 2, self.size * 2 + self.y_pos),
                             (self.x_pos, self.size * 2 + self.y_pos),
                             (self.x_pos, self.size + self.y_pos),
                             (self.x_pos - self.size, self.size + self.y_pos)])

    def draw_j(self, screen):
        pygame.draw.polygon(screen, pygame.Color('pink'),
                            [(self.x_pos, self.y_pos),
                             (self.x_pos + self.size, self.y_pos),
                             (self.x_pos + self.size * 2, self.y_pos),
                             (self.x_pos + self.size * 2, self.size + self.y_pos),
                             (self.x_pos + self.size, self.size + self.y_pos),
                             (self.x_pos + self.size, self.size * 3 + self.y_pos),
                             (self.x_pos, self.size * 3 + self.y_pos)])

    def draw_t(self, screen):
        pygame.draw.polygon(screen, pygame.Color('blue'),
                            [(self.x_pos - self.size, self.y_pos),
                             (self.x_pos + self.size * 2, self.y_pos),
                             (self.x_pos + self.size * 2, self.size + self.y_pos),
                             (self.x_pos + self.size * 2, self.size + self.y_pos),
                             (self.x_pos + self.size, self.size + self.y_pos),
                             (self.x_pos + self.size, self.size * 2 + self.y_pos),
                             (self.x_pos, self.size * 2 + self.y_pos),
                             (self.x_pos, self.size + self.y_pos),
                             (self.x_pos - self.size, self.size + self.y_pos)])

    def draw_l(self, screen):
        pygame.draw.polygon(screen, pygame.Color('yellow'),
                            [(self.x_pos, self.y_pos),
                             (self.x_pos - self.size * 2, self.y_pos),
                             (self.x_pos - self.size * 2, self.size + self.y_pos),
                             (self.x_pos - self.size, self.size + self.y_pos),
                             (self.x_pos - self.size, self.size * 3 + self.y_pos),
                             (self.x_pos, self.size * 3 + self.y_pos)])

    def draw_o(self, screen):
        pygame.draw.rect(screen, pygame.Color('green'),
                         (self.x_pos - self.size, self.y_pos,
                          self.size * 2, self.size * 2), 0)

    def draw_i(self, screen):
        pygame.draw.rect(screen, pygame.Color('purple'),
                         (self.x_pos - self.size, self.y_pos,
                          self.size, self.size * 4), 0)


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
    move = Move(tetris)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        move.update_figure()
        screen.fill(pygame.Color('gray'))
        move.render(screen)
        move.update_figure()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
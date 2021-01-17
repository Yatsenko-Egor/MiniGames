import pygame
from copy import deepcopy
from random import choice, randrange

RES = 750, 940
WIDTH, HEIGHT = 10, 20
FPS = 60
TILE = 45
GAME_RES = WIDTH * TILE, HEIGHT * TILE


class Tetris():
    def __init__(self, speed):
        pygame.init()
        self.screen = pygame.display.set_mode(RES)
        self.game_sc = pygame.Surface(GAME_RES)
        self.clock = pygame.time.Clock()
        self.grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(WIDTH) for y in range(HEIGHT)]
        self.figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                            [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                            [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                            [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                            [(0, 0), (0, -1), (0, 1), (-1, -1)],
                            [(0, 0), (0, -1), (0, 1), (1, -1)],
                            [(0, 0), (0, -1), (0, 1), (-1, 0)]]
        self.figures = [[pygame.Rect(x + WIDTH // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in self.figures_pos]
        self.figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
        self.field = [[0 for _ in range(WIDTH)] for j in range(HEIGHT)]
        self.speed_count = 0
        self.speed = speed
        self.speed_limit = 2000
        self.bg = pygame.image.load('data/Tetris/img/fon_for_game.jpg').convert()
        self.game_bg = pygame.image.load('data/Tetris/img/fon_for_tetris.jpg').convert()
        self.main_font = pygame.font.Font('data/Tetris/font/font.ttf', 65)
        self.font = pygame.font.Font('data/Tetris/font/font.ttf', 45)
        self.title_record = self.font.render('рекорд:', True, pygame.Color('cyan'))
        self.title_score = self.font.render('очки:', True, pygame.Color('darkgreen'))
        self.title_tetris = self.main_font.render('ТЕТРИС', True, pygame.Color('darkorange'))
        self.get_color = lambda: (randrange(10, 245), randrange(10, 245), randrange(10, 245))
        self.figure, self.next_figure = deepcopy(choice(self.figures)), deepcopy(choice(self.figures))
        self.color, self.next_color = self.get_color(), self.get_color()
        self.score, self.lines = 0, 0
        self.scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
        self.start()

    def check_borders(self, i):
        if self.figure[i].x < 0 or self.figure[i].x > WIDTH - 1:
            return False
        elif self.figure[i].y > HEIGHT - 1 or self.field[self.figure[i].y][self.figure[i].x]:
            return False
        return True

    def what_record(self):
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')

    def give_record(self, record, score):
        rec = max(int(record), score)
        with open('data/Tetris/record', 'w') as f:
            f.write(str(rec))

    def draw_next_figure(self):
        for i in range(4):
            self.figure_rect.x = self.next_figure[i].x * TILE + 380
            self.figure_rect.y = self.next_figure[i].y * TILE + 185
            pygame.draw.rect(self.screen, self.next_color, self.figure_rect)

    def draw_figure(self):
        for i in range(4):
            self.figure_rect.x = self.figure[i].x * TILE
            self.figure_rect.y = self.figure[i].y * TILE
            pygame.draw.rect(self.game_sc, self.color, self.figure_rect)

    def rotate_figure(self, i):
        x = self.figure[i].y - self.center.y
        y = self.figure[i].x - self.center.x
        self.figure[i].x = self.center.x - x
        self.figure[i].y = self.center.y + y

    def end_of_play(self):
        for i in self.grid:
            pygame.draw.rect(self.game_sc, self.get_color(), i)
            self.screen.blit(self.game_sc, (20, 20))
            pygame.display.flip()
            self.clock.tick(200)

    def draw_text(self):
        self.screen.blit(self.title_tetris, (478, -10))
        self.screen.blit(self.title_score, (535, 780))
        self.screen.blit(self.font.render(str(self.score), True, pygame.Color('white')), (550, 840))
        self.screen.blit(self.title_record, (525, 650))
        self.screen.blit(self.font.render(self.record, True, pygame.Color('orange')), (550, 710))

    def start(self):
        running = True
        while running:
            self.record = self.what_record()
            dx = 0
            rotate = False
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.game_sc, (20, 20))
            self.game_sc.blit(self.game_bg, (0, 0))
            for i in range(self.lines):
                pygame.time.wait(200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return ''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_DOWN:
                        self.speed_limit = 100
                    elif event.key == pygame.K_UP:
                        rotate = True
            self.figure_old = deepcopy(self.figure)
            for i in range(4):
                self.figure[i].x += dx
                if not self.check_borders(i):
                    self.figure = deepcopy(self.figure_old)
                    break
            self.speed_count += self.speed
            if self.speed_count > self.speed_limit:
                self.speed_count = 0
                self.figure_old = deepcopy(self.figure)
                for i in range(4):
                    self.figure[i].y += 1
                    if not self.check_borders(i):
                        for i in range(4):
                            self.field[self.figure_old[i].y][self.figure_old[i].x] = self.color
                        self.figure, self.color = self.next_figure, self.next_color
                        self.next_figure, self.next_color = deepcopy(choice(self.figures)), self.get_color()
                        self.speed_limit = 2000
                        break
            self.center = self.figure[0]
            self.figure_old = deepcopy(self.figure)
            if rotate:
                for i in range(4):
                    self.rotate_figure(i)
                    if not self.check_borders(i):
                        self.figure = deepcopy(self.figure_old)
                        break
            self.line = HEIGHT - 1
            self.lines = 0
            for row in range(HEIGHT - 1, -1, -1):
                count = 0
                for i in range(WIDTH):
                    if self.field[row][i]:
                        count += 1
                    self.field[self.line][i] = self.field[row][i]
                if count < WIDTH:
                    self.line -= 1
                else:
                    self.speed += 3
                    self.lines += 1
            self.score += self.scores[self.lines]
            for i in self.grid:
                pygame.draw.rect(self.game_sc, (40, 40, 40), i, 1)
            self.draw_figure()
            for y, raw in enumerate(self.field):
                for x, col in enumerate(raw):
                    if col:
                        self.figure_rect.x, self.figure_rect.y = x * TILE, y * TILE
                        pygame.draw.rect(self.game_sc, col, self.figure_rect)
            self.draw_next_figure()
            self.draw_text()
            for i in range(WIDTH):
                if self.field[0][i]:
                    self.give_record(self.record, self.score)
                    self.field = [[0 for i in range(WIDTH)] for j in range(HEIGHT)]
                    self.speed_count = 0
                    self.speed = 60
                    self.speed_limit = 2000
                    self.score = 0
                    self.end_of_play()
            pygame.display.flip()
            self.clock.tick(FPS)

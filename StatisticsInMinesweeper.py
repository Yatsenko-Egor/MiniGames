import pygame
import sqlite3


class StatisticsInMinesweeper:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Статистика')
        self.width = 250
        self.height = 200
        self.size = self.width, self.height
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(pygame.Color((180, 180, 180)))
        self.indent_in_left_column = self.width / 4
        self.indent_in_right_column = self.width / 2 + self.width / 4
        self.complexity = ['Профессионал', 'Любитель', 'Новичок']
        self.font = pygame.font.SysFont('Calibri', 18)
        self.start()

    def render(self):
        self.draw_table()
        self.draw_text()

    def draw_table(self):
        for row in range(4):
            pygame.draw.rect(self.screen, 'black', ((0, self.height / 4 * row), (self.width, 50)), width=2)
        pygame.draw.line(self.screen, 'black', (self.width / 2, 0), (self.width / 2, self.height), width=2)

    def draw_text(self):
        self.draw_title()
        self.draw_statistics()

    def draw_title(self):
        indent_in_title = self.height / 8
        title_1 = self.font.render('Сложность', True, (0, 0, 0))
        title_1_x = self.indent_in_left_column - title_1.get_width() / 2
        title_1_y = indent_in_title - title_1.get_height() / 2
        self.screen.blit(title_1, (title_1_x, title_1_y))

        title_2 = self.font.render('Лучшее время', True, (0, 0, 0))
        title_2_x = self.indent_in_right_column - title_2.get_width() / 2
        title_2_y = indent_in_title - title_2.get_height() / 2
        self.screen.blit(title_2, (title_2_x, title_2_y))

    def draw_statistics(self):
        results = self.get_results()
        for row in range(1, 4):
            indent_in_row = self.height / 4 * row + self.height / 8
            complexity = self.font.render(self.complexity[row - 1], True, (0, 0, 0))
            complexity_x = self.indent_in_left_column - complexity.get_width() / 2
            complexity_y = indent_in_row - complexity.get_height() / 2
            self.screen.blit(complexity, (complexity_x, complexity_y))
            if results[row - 1][0] == 0:
                result = self.font.render('Нет', True, (0, 0, 0))
            else:
                result = self.font.render(str(results[row - 1][0] / 10), True, (0, 0, 0))
            result_x = self.indent_in_right_column - result.get_width() / 2
            result_y = indent_in_row - result.get_height() / 2
            self.screen.blit(result, (result_x, result_y))

    def get_results(self):
        database = sqlite3.connect('data/database.sql')
        cursor = database.cursor()
        results = cursor.execute('''SELECT time from statistics_in_minesweeper''').fetchall()
        database.close()
        return results

    def start(self):
        fps = 60
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.render()
            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()
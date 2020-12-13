from Board import Board
import random
import pygame


class Minesweeper(Board):
    def __init__(self, width, height, mines_count, left=10, top=10, cell_size=30):
        super().__init__(width, height, left, top, cell_size, -1)
        self.MINE = 10
        self.MINE_COLOR = pygame.Color('red')
        self.DEFAULT_COLOR = pygame.Color('black')
        self.TEXT_COLOR = pygame.Color('green')
        self.generate_mines(mines_count)

    def open_cell(self, cell_coords):
        row, col = cell_coords
        if not self.can_open_cell(cell_coords):
            return
        neighbors = self.get_neighbors(row, col)
        mines_count = 0
        for pos in neighbors:
            i, j = pos
            if self.board[i][j] == self.MINE:
                mines_count += 1
        self.board[row][col] = mines_count
        if mines_count == 0:
            for i in neighbors:
                self.open_cell(i)


    def can_open_cell(self, cell_coords):
        i, j = cell_coords
        cell_value = self.board[i][j]
        return cell_value == self.default_value

    def draw_text(self, screen, value, rect):
        font_rect = rect.copy()
        font = pygame.font.Font(None, 30)
        text = font.render(str(value), True, self.TEXT_COLOR)
        font_rect.x = rect.x + self.cell_size // 2 - text.get_width() // 2
        font_rect.y = rect.y + self.cell_size // 2 - text.get_height() // 2
        screen.blit(text, font_rect)

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                x, y = self.get_cell_position(i, j)
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                cell_value = self.board[i][j]
                if cell_value == self.MINE:
                    pygame.draw.rect(screen, self.MINE_COLOR, rect)
                elif cell_value == self.default_value:
                    pygame.draw.rect(screen, self.DEFAULT_COLOR, rect)
                else:
                    self.draw_text(screen, cell_value, rect)
                pygame.draw.rect(screen, self.border_color, rect, width=self.border_width)

    def generate_mines(self, mines_count):
        mines_pos_list = self.get_random_mines_list(mines_count)
        for i, j in mines_pos_list:
            self.board[i][j] = self.MINE

    def get_random_mines_list(self, mines_count):
        mines_pos_list = set()
        if mines_count > self.width * self.height:
            raise Exception("mines_count can't be more than cell count")

        while len(mines_pos_list) < mines_count:
            i = random.randrange(0, self.height)
            j = random.randrange(0, self.width)
            mines_pos_list.add((i, j))
        return mines_pos_list

    def on_click(self, cell_coords):
        self.open_cell(cell_coords)


board = Minesweeper(10, 10, 20)
board.set_view(100, 100, 50)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('')
    width, height = 800, 800
    size = width, height
    screen = pygame.display.set_mode(size)
    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill(pygame.Color('black'))
        board.render(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
